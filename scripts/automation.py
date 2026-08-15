from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from dotenv import load_dotenv

load_dotenv(PROJECT_ROOT / ".env")

# Section: shared config

from ipsw_service.cli import IpswCliRunner, build_download_args
from ipsw_service.ipsw_api import FirmwareCatalogService, release_key
from ipsw_service.security_notes_service import cache_path
from langgraph_orchestration.graphs.reverse_engineering import (
    FEATURE_ANALYSIS_RECURSION_LIMIT,
)
from langgraph_orchestration.runtime import OrchestrationRuntime

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NOTHING_TO_DO = 2

STATE_DIR = PROJECT_ROOT / ".jenkins_pipeline"
KNOWN_BUILDS_FILE = STATE_DIR / "last_known_builds.json"
NEW_FIRMWARE_FILE = STATE_DIR / "new_firmware.json"
DOWNLOAD_PLAN_FILE = STATE_DIR / "download_plan.json"
RUN_RESULTS_FILE = STATE_DIR / "run_results.json"
REPORTS_DIR = STATE_DIR / "reports"

DOWNLOAD_DIR = PROJECT_ROOT / ".ipsw_downloads"
EXTRACT_DIR = PROJECT_ROOT / ".ipsw_extracted"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts" / "firmware_diff"

DOWNLOAD_TIMEOUT = int(os.getenv("PIPELINE_DOWNLOAD_TIMEOUT", str(4 * 60 * 60)))

IPSW_NAME_RE = re.compile(
    r"^(?P<device>[A-Za-z]+\d+,\d+)"
    r"_(?P<version>\d+(?:\.\d+)+)"
    r"_(?P<build>[A-Za-z0-9]+)_Restore\.ipsw$"
)


def pinned_devices() -> list[str]:
    raw = os.getenv("PIPELINE_DEVICES", "").strip()
    return [device for device in re.split(r"[;\s]+", raw) if device]


def device_family() -> str:
    return os.getenv("PIPELINE_DEVICE_FAMILY", "iPhone").strip() or "iPhone"


def managed_devices() -> list[str]:
    devices = list(pinned_devices())
    for device in read_json(KNOWN_BUILDS_FILE, {}):
        if device not in devices:
            devices.append(device)
    return devices


def stale_partial_days() -> int:
    """Age of stale ``.ipsw.download`` files in days before they are deleted during cleanup"""
    try:
        return max(0, int(os.getenv("PIPELINE_STALE_PARTIAL_DAYS", "7")))
    except ValueError:
        return 7


def keep_per_device() -> int:
    """Minimum 1 IPSW to retain per device during cleanup"""
    try:
        return max(1, int(os.getenv("PIPELINE_KEEP_PER_DEVICE", "1")))
    except ValueError:
        return 1


def ipsw_filename(device: str, version: str, build: str) -> str:
    return f"{device}_{version}_{build}_Restore.ipsw"


def parse_ipsw_name(name: str) -> dict[str, str] | None:
    match = IPSW_NAME_RE.match(name)
    return match.groupdict() if match else None


def local_ipsws(device: str | None = None) -> list[dict]:
    found: list[dict] = []
    if not DOWNLOAD_DIR.is_dir():
        return found
    for path in DOWNLOAD_DIR.iterdir():
        parsed = parse_ipsw_name(path.name)
        if parsed and path.is_file() and (device is None or parsed["device"] == device):
            found.append({**parsed, "path": path})
    found.sort(key=lambda entry: release_key(entry["version"], entry["build"]), reverse=True)
    return found


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def banner(title: str) -> None:
    print("=" * 64)
    print(f"  {title}")
    print("=" * 64)


def gigabytes(num_bytes: int) -> str:
    return f"{num_bytes / (1024**3):.1f} GB"


# Stage 1: check for new firmware
# Queries api.ipsw.me and compares against last_known_builds.json


def _select_devices(catalog: FirmwareCatalogService) -> list[str]:
    pinned = pinned_devices()
    if pinned:
        print(f"  Pinned to {len(pinned)} device(s): {', '.join(pinned)}\n")
        return pinned

    family = device_family()
    newest = catalog.resolve_newest_device(family)
    if newest is None:
        print(f"  Could not auto-detect a {family} device from api.ipsw.me\n")
        return []
    print(f"  Auto-detected newest {family}: {newest}\n")
    return [newest]


def stage_check() -> int:
    banner("Stage 1: Check for New Firmware")

    catalog = FirmwareCatalogService()
    devices = _select_devices(catalog)
    if not devices:
        print("  ERROR: no device to check")
        return EXIT_ERROR

    known = read_json(KNOWN_BUILDS_FILE, {})
    detected: list[dict] = []
    unreachable: list[str] = []

    for device in devices:
        latest = catalog.resolve_latest_ipsw(device)
        if latest is None:
            unreachable.append(device)
            print(f"  [SKIP] {device}: no IPSW data returned by api.ipsw.me")
            continue

        seen = known.get(device) or {}
        release = f"{latest['version']} ({latest['build']})"
        if seen.get("build") == latest["build"]:
            print(f"  [SEEN] {device}: {release} already analysed")
            continue

        previously = f", was {seen['version']} ({seen['build']})" if seen else ", first run"
        released = latest["released"] or "unknown"
        print(f"  [NEW]  {device}: {release} released {released}{previously}")
        detected.append(latest)

    write_json(NEW_FIRMWARE_FILE, detected)

    # Every device failing is a network or API problem, not an empty result.
    if unreachable and len(unreachable) == len(devices):
        print("\n  ERROR: api.ipsw.me returned no data for any monitored device")
        return EXIT_ERROR

    if not detected:
        print("\n  No new firmware -- skipping download, analysis and cleanup")
        return EXIT_NOTHING_TO_DO

    print(f"\n  {len(detected)} new release(s) queued for download")
    return EXIT_OK


# Stage 2: download firmware


def _download(runner: IpswCliRunner, device: str, version: str, build: str) -> Path | None:
    expected = DOWNLOAD_DIR / ipsw_filename(device, version, build)
    args = build_download_args(
        device=device,
        build=build,
        output_dir=str(DOWNLOAD_DIR),
        resume_all=True,
    )
    result = runner.run_with_sudo_fallback(args, timeout=DOWNLOAD_TIMEOUT)
    if not result.success:
        print(f"    FAIL: {result.stderr or result.stdout or 'ipsw download failed'}")
        return None

    if expected.is_file():
        return expected
    # use build ID to find the downloaded file in case the filename is not as expected
    for entry in local_ipsws(device):
        if entry["build"] == build:
            return entry["path"]
    print(f"    FAIL: download reported success but {expected.name} is not on disk")
    return None


def _local_baseline(device: str, version: str, build: str = "") -> dict | None:
    """Newest already-downloaded IPSW for *device* older than *version*/*build*"""
    current = release_key(version, build)
    for entry in local_ipsws(device):
        if release_key(entry["version"], entry["build"]) < current:
            return entry
    return None


def _cache_advisories(plan: list[dict]) -> None:
    """Fetch Apple Security Notes for the firmware versions in this run"""
    from update_security_notes import _RELEASES_INDEX_URL, _http_get, update_version

    wanted = sorted(
        {entry[key] for entry in plan for key in ("version", "old_version") if entry.get(key)}
    )
    missing = [v for v in wanted if not cache_path(v).exists()]
    if not missing:
        print(f"\n  Security Notes: already cached for {', '.join(wanted) or 'nothing'}")
        return

    print(f"\n  Security Notes: fetching {', '.join(missing)}")
    index_html = _http_get(_RELEASES_INDEX_URL)
    if not index_html:
        print("    index unreachable; triage will run without advisory matching")
        return
    for version in missing:
        try:
            update_version(version, index_html, force=False, use_archive=False)
        except Exception as exc:
            print(f"    {version}: {type(exc).__name__}: {exc}")


def stage_download() -> int:
    banner("Stage 2: Download Firmware")

    releases = read_json(NEW_FIRMWARE_FILE, [])
    if not releases:
        print("  No detected releases -- nothing to download")
        return EXIT_NOTHING_TO_DO

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    runner = IpswCliRunner(cwd=str(DOWNLOAD_DIR))
    catalog = FirmwareCatalogService()
    plan: list[dict] = []
    failed: list[str] = []

    for release in releases:
        device, version, build = release["device"], release["version"], release["build"]
        print(f"\n  {device} {version} ({build})")

        new_ipsw = _download(runner, device, version, build)
        if new_ipsw is None:
            failed.append(f"{device} {version}")
            continue
        print(f"    OK: {new_ipsw.name} ({gigabytes(new_ipsw.stat().st_size)})")

        baseline = _local_baseline(device, version, build)
        gap = ""
        if baseline:
            print(f"    Baseline already on disk: {baseline['path'].name}")
        else:
            previous = catalog.resolve_previous_ipsw(device, version, build)
            if previous is None:
                if catalog.list_ipsw_firmwares(device):
                    gap = "none"
                    print("    No earlier release in the catalog -- establishing baseline only")
                else:
                    gap = "unresolved"
                    print("    FAIL: catalog unreachable, cannot resolve a predecessor")
            else:
                print(f"    Fetching baseline {previous['version']} ({previous['build']})")
                old_path = _download(runner, device, previous["version"], previous["build"])
                if old_path is None:
                    gap = "unresolved"
                    print("    FAIL: baseline download failed")
                else:
                    baseline = {
                        "version": previous["version"],
                        "build": previous["build"],
                        "path": old_path,
                    }

        entry = {
            "device": device,
            "version": version,
            "build": build,
            "new_ipsw": str(new_ipsw),
            "old_ipsw": str(baseline["path"]) if baseline else None,
            "old_version": baseline["version"] if baseline else None,
            "old_build": baseline["build"] if baseline else None,
            "baseline_gap": gap,
        }
        plan.append(entry)
        if baseline:
            print(f"    Diff pair: {baseline['version']} -> {version}")

    write_json(DOWNLOAD_PLAN_FILE, plan)
    if plan:
        _cache_advisories(plan)

    analysable = sum(1 for entry in plan if entry["old_ipsw"])
    print(f"\n  Ready: {len(plan)} device(s), {analysable} with a diff pair")
    if failed:
        print(f"  Failed (retried next run): {', '.join(failed)}")
    return EXIT_OK if plan else EXIT_ERROR


# Stage 3: diff and analyse


def _prompt(entry: dict) -> str:
    """Request text mirroring an interactive firmware-diff prompt"""
    return (
        "1) Download Version 1 and Version 2 firmware artifacts.\n"
        "2) Extract dyld_shared_cache and kernelcache from both artifacts.\n"
        "Perform baseline comparison and feature inference.\n"
        f"Version 1: {Path(entry['old_ipsw']).name}\n"
        f"Version 2: {Path(entry['new_ipsw']).name}\n"
        "Perform a deep, static-only inspection of two provided dyld_shared_cache "
        "artifacts and produce an analysis of newly introduced classes and related changes.\n\n"
    )


def _seed(entry: dict) -> dict[str, str]:
    targets = [
        {"device": entry["device"], "version": entry["old_version"], "build": entry["old_build"]},
        {"device": entry["device"], "version": entry["version"], "build": entry["build"]},
    ]
    return {
        "parsed_firmware_targets": json.dumps(targets),
        "confirmed_local_ipsws": json.dumps(sorted([entry["old_ipsw"], entry["new_ipsw"]])),
        "diff_pair_old": entry["old_ipsw"],
        "diff_pair_new": entry["new_ipsw"],
    }


def _artifact_run_dir(intermediate: dict[str, str]) -> Path | None:
    """Locate ``artifacts/firmware_diff/<run id>/`` for the completed run"""
    for raw in (
        intermediate.get("firmware_raw_diff_dir"),
        intermediate.get("firmware_diff_report_path"),
    ):
        if not raw:
            continue
        parts = Path(raw).parts
        if "firmware_diff" in parts:
            index = parts.index("firmware_diff")
            if index + 1 < len(parts):
                return ARTIFACTS_DIR / parts[index + 1]
    return None


def _collect_reports(run_dir: Path) -> None:
    """Copy Jenkins artifacts for archiving"""
    destination = REPORTS_DIR / run_dir.name
    destination.mkdir(parents=True, exist_ok=True)
    feature_analysis = run_dir / "feature_analysis"
    if feature_analysis.is_dir():
        shutil.copytree(feature_analysis, destination / "feature_analysis", dirs_exist_ok=True)
    report = run_dir / "report.json"
    if report.is_file():
        shutil.copy2(report, destination / "report.json")


def stage_analyze() -> int:
    banner("Stage 3: LangGraph Firmware Diff and Analysis")

    plan = read_json(DOWNLOAD_PLAN_FILE, [])
    if not plan:
        print("  No download plan -- nothing to analyse")
        return EXIT_NOTHING_TO_DO

    known = read_json(KNOWN_BUILDS_FILE, {})
    results: list[dict] = []
    failures: list[str] = []

    def commit(entry: dict, status: str, run_id: str = "") -> None:
        """Record the build as seen so Stage 1 stops re-detecting it"""
        known[entry["device"]] = {
            "version": entry["version"],
            "build": entry["build"],
            "status": status,
            "diff_run": run_id,
            "recorded_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        write_json(KNOWN_BUILDS_FILE, known)

    pairs = [entry for entry in plan if entry["old_ipsw"]]
    unpaired = [entry for entry in plan if not entry["old_ipsw"]]
    baselines = [entry for entry in unpaired if entry.get("baseline_gap") != "unresolved"]
    unresolved = [entry for entry in unpaired if entry.get("baseline_gap") == "unresolved"]

    for entry in baselines:
        print(f"  [BASELINE] {entry['device']} {entry['version']}: no predecessor to diff")
        commit(entry, "baseline")
        results.append({**_summary(entry), "status": "baseline"})

    for entry in unresolved:
        print(
            f"  [RETRY] {entry['device']} {entry['version']}: predecessor unavailable, not recorded"
        )
        results.append({**_summary(entry), "status": "failed", "error": "predecessor unavailable"})

    if not pairs:
        write_json(RUN_RESULTS_FILE, _run_summary(results, 0))
        if unresolved:
            print("\n  Predecessor unavailable -- nothing recorded as seen, retried next run")
            return EXIT_ERROR
        print("\n  No diff pairs -- baselines recorded for the next release")
        return EXIT_NOTHING_TO_DO

    shutil.rmtree(REPORTS_DIR, ignore_errors=True)

    print("\n  Loading orchestration runtime (MLX model + graph)...")
    runtime = OrchestrationRuntime(recursion_limit=FEATURE_ANALYSIS_RECURSION_LIMIT)
    runtime.ensure_ready()
    print("  Runtime ready")

    for index, entry in enumerate(pairs, 1):
        label = f"{entry['device']} {entry['old_version']} -> {entry['version']}"
        print(f"\n  [{index}/{len(pairs)}] {label}")
        started = time.perf_counter()

        try:
            state = runtime.run(_prompt(entry), seed_intermediate=_seed(entry))
            elapsed = round(time.perf_counter() - started, 1)

            if "reverse_engineering" not in state.execution_domains:
                raise RuntimeError(
                    f"supervisor routed to {state.execution_domains} instead of reverse_engineering"
                )
            run_dir = _artifact_run_dir(state.intermediate_outputs)
            if run_dir is None:
                raise RuntimeError("pipeline produced no firmware diff report")
            _collect_reports(run_dir)

            results.append(
                {
                    **_summary(entry),
                    "status": "analysed",
                    "elapsed_seconds": elapsed,
                    "diff_run": run_dir.name,
                    "feature_reports": sorted(state.feature_analysis_reports),
                    "output_chars": len(state.final_output or ""),
                    "agent_chain": state.agent_chain,
                    "analysis_notes": state.analysis_notes,
                }
            )
            commit(entry, "analysed", run_dir.name)
            print(
                f"    OK in {elapsed}s -- {len(state.feature_analysis_reports)} feature report(s)"
                f" in artifacts/firmware_diff/{run_dir.name}/"
            )

        except Exception as exc:
            elapsed = round(time.perf_counter() - started, 1)
            results.append(
                {
                    **_summary(entry),
                    "status": "failed",
                    "elapsed_seconds": elapsed,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            failures.append(label)
            print(f"    FAILED after {elapsed}s: {type(exc).__name__}: {exc}")

    write_json(RUN_RESULTS_FILE, _run_summary(results, len(pairs)))

    print(f"\n  Analysed {len(pairs) - len(failures)}/{len(pairs)} pair(s)")
    if failures:
        print(f"  Failed (retried next run): {', '.join(failures)}")
    if unresolved:
        print(f"  Predecessor unavailable (retried next run): {len(unresolved)} device(s)")
    return EXIT_ERROR if failures or unresolved else EXIT_OK


def _summary(entry: dict) -> dict:
    return {
        "device": entry["device"],
        "old_version": entry["old_version"],
        "new_version": entry["version"],
        "new_build": entry["build"],
    }


def _run_summary(results: list[dict], pair_count: int) -> dict:
    return {
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
        "pairs_analysed": pair_count,
        "succeeded": sum(1 for item in results if item["status"] == "analysed"),
        "baselines": sum(1 for item in results if item["status"] == "baseline"),
        "failed": sum(1 for item in results if item["status"] == "failed"),
        "results": results,
    }


# Stage 4: prune superseded IPSWs
# Keeps PIPELINE_KEEP_PER_DEVICE builds per managed device


def _extraction_dirs(build: str, protected: set[str]) -> list[Path]:
    if not EXTRACT_DIR.is_dir():
        return []
    return [
        path
        for path in EXTRACT_DIR.iterdir()
        if path.is_dir() and build in path.name and not any(kept in path.name for kept in protected)
    ]


def _sweep_stale_partials(max_age_days: int) -> tuple[int, int]:
    if max_age_days <= 0 or not DOWNLOAD_DIR.is_dir():
        return 0, 0

    cutoff = time.time() - max_age_days * 86400
    removed = 0
    freed = 0
    for path in DOWNLOAD_DIR.glob("*.ipsw.download"):
        if not path.is_file() or path.stat().st_mtime >= cutoff:
            continue
        size = path.stat().st_size
        try:
            path.unlink()
        except OSError as exc:
            print(f"    WARNING: could not remove {path.name}: {exc}")
            continue
        removed += 1
        freed += size
        print(f"    removed abandoned download {path.name} ({gigabytes(size)})")
    return removed, freed


def stage_cleanup() -> int:
    banner("Stage 4: Prune Superseded IPSWs")

    devices = managed_devices()
    keep = keep_per_device()
    stale_days = stale_partial_days()

    removed_files = 0
    removed_dirs = 0
    freed_bytes = 0

    print(f"  Abandoned downloads older than {stale_days} day(s):")
    partials, partial_bytes = _sweep_stale_partials(stale_days)
    if not partials:
        print("    none")
    removed_files += partials
    freed_bytes += partial_bytes

    if not devices:
        print("\n  No pipeline-managed devices on record -- nothing else to prune")
        return EXIT_OK
    print(f"\n  Devices: {', '.join(devices)} (keeping {keep} IPSW each)\n")

    for device in devices:
        entries = local_ipsws(device)  # newest version first
        if len(entries) <= keep:
            count = len(entries)
            print(f"  {device}: {count} IPSW on disk, nothing to prune")
            continue

        retained, superseded = entries[:keep], entries[keep:]
        protected = {entry["build"] for entry in retained}
        print(f"  {device}: keeping {', '.join(entry['path'].name for entry in retained)}")

        for entry in superseded:
            path = entry["path"]
            size = path.stat().st_size
            try:
                path.unlink()
            except OSError as exc:
                print(f"    WARNING: could not remove {path.name}: {exc}")
                continue
            removed_files += 1
            freed_bytes += size
            print(f"    removed {path.name} ({gigabytes(size)})")

            for stale in _extraction_dirs(entry["build"], protected):
                try:
                    shutil.rmtree(stale)
                except OSError as exc:
                    print(f"    WARNING: could not remove {stale.name}/: {exc}")
                    continue
                removed_dirs += 1
                print(f"    removed extraction {stale.name}/")

    print(
        f"\n  Removed {removed_files} file(s) and {removed_dirs} extraction "
        f"directory(ies), freeing {gigabytes(freed_bytes)}"
    )
    return EXIT_OK


# Section: entry point

STAGES = {
    "check": ("Check for New Firmware", stage_check),
    "download": ("Download Firmware", stage_download),
    "analyze": ("Diff and Analyse", stage_analyze),
    "cleanup": ("Prune Superseded IPSWs", stage_cleanup),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Daily firmware pipeline stages, run by Jenkins.",
        epilog="Exit codes: 0 work done, 1 error, 2 nothing to do.",
    )
    parser.add_argument("stage", choices=sorted(STAGES), help="which stage to run")
    args = parser.parse_args(argv)

    title, run = STAGES[args.stage]
    banner(title)
    return run()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
