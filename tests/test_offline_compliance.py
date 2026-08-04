from __future__ import annotations

import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

NETWORK_MODULES = {
    "urllib",
    "requests",
    "httpx",
    "aiohttp",
    "http",
    "ftplib",
    "telnetlib",
    "huggingface_hub",
}

ALLOWED = {
    "ipsw_service/ipsw_api.py",
    "langgraph_orchestration/gemini.py",
    "langgraph_orchestration/inference.py",
}


def _imports(path: Path) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            modules.add(node.module.split(".")[0])
    return modules


def test_analysis_path_imports_no_network_library():
    offenders = {}
    for package in ("langgraph_orchestration", "ipsw_service"):
        for path in (PROJECT_ROOT / package).rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            relative = str(path.relative_to(PROJECT_ROOT))
            if relative in ALLOWED:
                continue
            found = _imports(path) & NETWORK_MODULES
            if found:
                offenders[relative] = sorted(found)

    assert not offenders, (
        f"Analysis modules importing network libraries: {offenders}. "
        "Move deliberate data acquisition into scripts/, or add the file to ALLOWED."
    )


def test_security_notes_matching_reads_only_the_local_cache(monkeypatch, tmp_path):
    from ipsw_service import security_notes_service

    monkeypatch.setenv("SECURITY_NOTES_DIR", str(tmp_path))
    security_notes_service.load_cached_components.cache_clear()

    service = security_notes_service.SecurityNotesService.for_version("99.9.9")
    assert not service.has_entries()


def test_decompiler_rpc_is_loopback_only():
    from langgraph_orchestration.tooling import decompiler_tools

    assert decompiler_tools.DECOMPILER_HOST in ("127.0.0.1", "localhost", "::1")


def test_servers_refuse_to_bind_beyond_loopback():
    from langgraph_orchestration.core import enforce_bind_policy

    for host in ("127.0.0.1", "localhost", "::1", ""):
        enforce_bind_policy(host, surface="test")

    for host in ("0.0.0.0", "192.168.1.10", "example.com"):
        with pytest.raises(RuntimeError):
            enforce_bind_policy(host, surface="test")


def test_no_runtime_entry_point_uses_the_cloud_factory():
    entry_points = [
        PROJECT_ROOT / "api.py",
        PROJECT_ROOT / "app.py",
        PROJECT_ROOT / "langgraph_orchestration" / "runtime.py",
        *(PROJECT_ROOT / "scripts" / "pipeline").glob("*.py"),
    ]
    for path in entry_points:
        live = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if "gemini_factory" in line and not line.strip().startswith("#")
        ]
        assert not live, f"{path.name} imports the cloud factory on a live code path"


def test_file_relative_paths_resolve_inside_the_repo():
    from ipsw_service.security_notes_service import cache_dir
    from langgraph_orchestration.inference import models_dir
    from langgraph_orchestration.prompts import _PROMPT_ROOT

    for label, path in (
        ("models_dir()", models_dir()),
        ("_PROMPT_ROOT", _PROMPT_ROOT),
        ("security notes cache_dir()", cache_dir()),
    ):
        resolved = path.resolve()
        assert PROJECT_ROOT in resolved.parents, f"{label} resolves outside the repo: {resolved}"


def test_model_download_is_refused_when_offline(monkeypatch, tmp_path):
    """inference.py is allowlisted because it downloads model weights"""
    import builtins

    from langgraph_orchestration.inference import ensure_downloaded

    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    monkeypatch.setenv("MODELS_DIR", str(tmp_path / "nothing-here"))

    real_import = builtins.__import__

    def refuse_hub(name, *args, **kwargs):
        assert not name.startswith("huggingface_hub"), "reached the network while offline"
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", refuse_hub)

    with pytest.raises(RuntimeError, match="HF_HUB_OFFLINE"):
        ensure_downloaded("mlx-community/Qwen3.5-9B-MLX-4bit", label="language model")


def test_downloading_is_unreachable_from_the_load_path():
    source = (PROJECT_ROOT / "langgraph_orchestration" / "inference.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    callers = set()
    for func in ast.walk(tree):
        if not isinstance(func, ast.FunctionDef):
            continue
        for node in ast.walk(func):
            if isinstance(node, ast.Name) and node.id == "ensure_downloaded":
                callers.add(func.name)

    assert callers <= {"main"}, (
        f"ensure_downloaded is reachable from {sorted(callers - {'main'})}. "
        "Downloading must stay confined to the command line."
    )

    others = {
        path
        for package in ("langgraph_orchestration", "ipsw_service")
        for path in (PROJECT_ROOT / package).rglob("*.py")
        if "__pycache__" not in path.parts
        and path.name != "inference.py"
        and "ensure_downloaded" in path.read_text(encoding="utf-8")
    }
    assert not others, f"ensure_downloaded is used outside inference.py: {sorted(others)}"


def test_local_env_does_not_enable_egress():
    env_file = PROJECT_ROOT / ".env"
    if not env_file.is_file():
        pytest.skip("no .env in this checkout")

    settings = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            settings[key.strip()] = value.strip().strip("\"'")

    tracing = settings.get("LANGSMITH_TRACING", "false").lower()
    assert tracing not in ("1", "true", "yes"), (
        "LANGSMITH_TRACING is on: every graph run sends trace data to "
        "LangChain's cloud. Set it to false to keep the analysis path local."
    )

    assert settings.get("HF_HUB_OFFLINE", "").strip() in ("1", "true", "yes"), (
        "HF_HUB_OFFLINE is not set: huggingface_hub calls its CDN on every "
        "model load to check the cache. Set HF_HUB_OFFLINE=1."
    )


@pytest.mark.parametrize("entry", ["app", "api", "scripts/automation", "scripts/qdrant"])
def test_entry_points_load_env_before_huggingface_hub(entry):
    """Verify `HF_HUB_OFFLINE` is applied before importing `huggingface_hub`"""
    import subprocess
    import sys

    # Entry points are split across branches, and HF_HUB_OFFLINE reaches the
    # process through .env, which is untracked. Skip rather than fail when
    # either is missing from the checkout.
    if not (PROJECT_ROOT / f"{entry}.py").is_file():
        pytest.skip(f"{entry}.py is not in this checkout")
    if not (PROJECT_ROOT / ".env").is_file():
        pytest.skip("no .env in this checkout; HF_HUB_OFFLINE is read from it")

    module = Path(entry).name
    extra_path = str(PROJECT_ROOT / Path(entry).parent) if "/" in entry else ""
    code = (
        "import os, sys; os.environ.pop('HF_HUB_OFFLINE', None); "
        f"sys.path.insert(0, {extra_path!r}) if {extra_path!r} else None; "
        f"__import__({module!r}); "
        "import huggingface_hub.constants as c; print(c.HF_HUB_OFFLINE)"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    assert result.returncode == 0, result.stderr[-800:]
    assert result.stdout.strip().endswith("True"), (
        f"{entry} leaves huggingface_hub with offline=False. "
        "Move load_dotenv() above the third-party imports."
    )
