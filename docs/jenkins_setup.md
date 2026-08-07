# Jenkins Setup

Set up the Jenkins jobs used for scheduled firmware analysis and continuous integration.

| Job | Jenkinsfile | Purpose | Runtime |
|---|---|---|---|
| `ipsw-firmware-analysis` | `Jenkinsfile` | Detect, download, diff, and analyse new firmware | Hours |
| `ipsw-ci` | `Jenkinsfile.ci` | Run linting, tests, and dependency checks | Minutes |

The jobs are kept separate so routine CI isn't blocked by the much longer firmware analysis pipeline.

## Pipeline Overview

```
Stage 1  check       Detect new firmware and generate new_firmware.json
            |                      
            v  
Stage 2  download    Download IPSWs and generate download_plan.json
            |                     
            v  
Stage 3  analyze     Run the LangGraph analysis pipeline and produce reports
            |                      
            v 
Stage 4  cleanup     Remove superseded IPSWs
```

The analysis stage uses the same `OrchestrationRuntime.run()` entry point as the API and Gradio UI.

### Device Selection

By default, the pipeline automatically selects the newest supported device and compares its latest firmware with the previous release.

Selection follows two rules:

- Prefer the newest flagship model in the selected device family.
- Skip devices that don't have an earlier firmware available.

Set `PIPELINE_DEVICES` to analyse specific devices.

### State 

Processed builds are tracked in `.jenkins_pipeline/last_known_builds.json`.
Only successfully analysed devices (or newly established baselines) are recorded.
If a download or analysis fails, the device is retried on the next scheduled run.

If no previous firmware exists, the device is recorded as a baseline and analysed
when the next release becomes available.

### Disk Usage

The pipeline typically keeps one IPSW per monitored device (about 11 GB). The first run downloads both the current and previous releases.

Interrupted downloads resume automatically. Partial downloads older than
`PIPELINE_STALE_PARTIAL_DAYS` are removed.

## Prerequisites

- macOS on Apple Silicon (MLX inference)
- `ipsw` CLI (`brew install blacktop/tap/ipsw`)
- Project virtual environment
- IDA Pro configured via `IDA_PATH` and `IDA_RPC_SCRIPT_PATH`

## 1. Install Jenkins

```bash
brew install jenkins-lts
brew services start jenkins-lts
```

Open <http://localhost:8080>, unlock with:

```bash
cat ~/.jenkins/secrets/initialAdminPassword
```

Choose **Install suggested plugins** and create the admin user. The suggested plugin set is sufficient.

## 2. Create the Job

1. **New Item** -> name `ipsw-firmware-analysis` -> **Pipeline** -> OK
2. Under **Pipeline**:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/hui-joyce/local-multi-agent-dev`
   - Branch Specifier: the branch you deploy from, e.g. `*/main`
   - Script Path: `Jenkinsfile`
3. Save

> Jenkins clones the repo to read the `Jenkinsfile`, but every stage runs via
> `dir(PROJECT_DIR)` against the real working tree. Edits to
> `scripts/automation.py` therefore take effect immediately, while edits to the
> `Jenkinsfile` itself need a commit before Jenkins sees them.

## 3. Create the CI Job

Same steps, named `ipsw-ci`, with **Script Path** `Jenkinsfile.ci`.

## 4. Configure

Pipeline behaviour is set in the `Jenkinsfile` `environment` block:

| Variable | Default | Meaning |
|---|---|---|
| `PIPELINE_DEVICES` | *(empty)* | Empty auto-detects the newest device. Set to pin, **space- or semicolon-separated**. Commas are part of an identifier, so they cannot be the delimiter. |
| `PIPELINE_DEVICE_FAMILY` | `iPhone` | Family to auto-detect within (`iPhone`, `iPad`, `AppleTV`, `Watch`). |
| `PIPELINE_KEEP_PER_DEVICE` | `1` | IPSWs retained per device after cleanup. One is enough: the retained IPSW is the next release's baseline. |
| `PIPELINE_DOWNLOAD_TIMEOUT` | `14400` | Per-download timeout in seconds. |
| `PIPELINE_STALE_PARTIAL_DAYS` | `7` | Age at which an abandoned `.ipsw.download` is swept. Recent partials are left alone so an interrupted download can resume. `0` disables the sweep. |

Jenkins environment variables take precedence over `.env`, so `.env` holds
secrets and Jenkins holds pipeline configuration.

A single device is usually enough. Each additional device adds ~11 GB and a full analysis run.

```groovy
PIPELINE_DEVICES = 'iPhone18,1 iPhone17,1'
```

### Sudo for extraction

`ipsw extract` mounts the SystemOS volume via `hdiutil`, which can need root.
Preferred:

```bash
sudo visudo
# add, matching `which ipsw`:
user ALL=(ALL) NOPASSWD: /opt/homebrew/bin/ipsw
```

Otherwise set `IPSW_SUDO_PASSWORD` in `.env`. The runner tries the plain
command first and only escalates on a permission failure.

## 5. First run

Trigger **Build Now** on `ipsw-firmware-analysis`. The first run downloads
the latest firmware and its predecessor, then analyses the pair. 
Expect it to take several hours.

To verify the wiring without downloading anything, run Stage 1 by hand:

```bash
cd /Users/user/Documents/GitHub/local-multi-agent-dev
venv/bin/python scripts/automation.py check; echo "exit=$?"
```

Exit 0 means new firmware was detected, 2 means nothing new, 1 means the API
was unreachable.

## 6. Results

Archived on the build page (small, current run only):

- `.jenkins_pipeline/new_firmware.json` - what was detected
- `.jenkins_pipeline/download_plan.json` - the diff pairs
- `.jenkins_pipeline/run_results.json` - per-device status, latency, run id
- `.jenkins_pipeline/reports/<run id>/` - feature-analysis markdown, `report.json`

Full output remains in `artifacts/firmware_diff/<run id>/` and is not archived
to keep Jenkins builds small.

### Example outputs

**`new_firmware.json`** -- written by every `check` run, whether or not anything
was found. One entry per device whose newest build differs from
`last_known_builds.json`; `[]` when nothing is new, which is the common case.

```json
[
  {
    "device": "iPhone18,1",
    "version": "26.6",
    "build": "23G71",
    "url": "https://updates.cdn-apple.com/2026SummerFCS/fullrestores/140-57285/88580B31-DFDB-4502-884F-DA40EC871038/iPhone18,1_26.6_23G71_Restore.ipsw",
    "released": "2026-07-27T17:38:06Z",
    "signed": true
  }
]
```

`signed` reports whether Apple still signs the build for restore, not whether it
is an official release. Only the current release is normally signed.

**`download_plan.json`** -- one entry per device, written after the IPSWs are on
disk. `old_ipsw` is `null` when no predecessor could be resolved, in which case
the pair is skipped and only a baseline is recorded.

```json
[
  {
    "device": "iPhone18,1",
    "version": "26.6",
    "build": "23G71",
    "new_ipsw": "/path/to/repo/.ipsw_downloads/iPhone18,1_26.6_23G71_Restore.ipsw",
    "old_ipsw": "/path/to/repo/.ipsw_downloads/iPhone18,1_26.5.2_23F84_Restore.ipsw",
    "old_version": "26.5.2",
    "old_build": "23F84",
    "baseline_gap": ""
  }
]
```

`baseline_gap` is `""` on success, `"none"` when the catalog holds no earlier
release for the device, and `"unresolved"` when the catalog was unreachable or
the baseline download failed.

**`run_results.json`** -- one file per `analyze` run, holding a roll-up plus a
per-device record.

```json
{
  "timestamp": "2026-08-05T01:41:07+00:00",
  "pairs_analysed": 1,
  "succeeded": 1,
  "baselines": 0,
  "failed": 0,
  "results": [
    {
      "device": "iPhone18,1",
      "old_version": "26.5.2",
      "new_version": "26.6",
      "new_build": "23G71",
      "status": "analysed",
      "elapsed_seconds": 14812.6,
      "diff_run": "20260805-014107",
      "feature_reports": [
        "artifacts/firmware_diff/20260805-014107/feature_analysis/IOKit_analysis.md",
        "artifacts/firmware_diff/20260805-014107/feature_analysis/WebCore_analysis.md"
      ],
      "output_chars": 48213,
      "agent_chain": ["supervisor", "reverse_engineering"],
      "analysis_notes": {"notes": []}
    }
  ]
}
```

`status` is `analysed`, `baseline` (recorded without a diff, no predecessor
available), or `failed`. A failed record carries `error` instead of the report
fields:

```json
{
  "device": "iPhone18,1",
  "old_version": "26.5.2",
  "new_version": "26.6",
  "new_build": "23G71",
  "status": "failed",
  "elapsed_seconds": 92.4,
  "error": "RuntimeError: pipeline produced no firmware diff report"
}
```

Failed devices stay out of `last_known_builds.json`, so the next run detects the
build again and retries. Pruning is skipped on that run so the predecessor IPSW
survives for the retry.

**`reports/<run id>/`** -- a copy of the analysis output, small enough to archive
on the build page:

```
.jenkins_pipeline/reports/20260805-014107/
  report.json
  feature_analysis/
    00_SUMMARY.md
    IOKit_analysis.md
    WebCore_analysis.md
    ...
```

`00_SUMMARY.md` opens with the counts for the run:

```
# Feature Analysis Summary -- iOS 26.6

- **Total components in diff**: 316  (**HIGH_SIGNAL**: 216, **LOW_SIGNAL**: 100)
- **Analysed** (report written): 38  |  **Apple Security Notes matches**: 12  | ...
```

`Apple Security Notes matches: 0` means no cached advisory was found for the
target version, not that Apple flagged nothing. The scheduled pipeline caches
advisories during `download`; a manual run needs
`python scripts/update_security_notes.py <version>` first.

## Managing Jenkins

```bash
brew services restart jenkins-lts
tail -f /opt/homebrew/var/log/jenkins/output.log
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `ipsw: command not found` | Ensure `/opt/homebrew/bin` is on `PATH`. |
| `hdiutil: attach failed ... permission denied` | Configure passowrdless sudo or `IPSW_SUDO_PASSWORD`. |
| Stage 1 exits 1 | Check connectivity to `api.ipsw.me` and verify `PIPELINE_DEVICES`. |
| Wrong device selected | Pin the device with `PIPELINE_DEVICES`. |
| Build UNSTABLE | Check `run_results.json` and the Stage 3 logs. |
| Same firmware detected repeatedly | Check the Stage 3 logs; the previous analysis likely failed. |
| Pinned device never detected | Separate device identifiers with spaces, not commas. |
| IPSWs are downloaded again | Expected. Existing downlaods are verified before reuse. |
| Build times out | Increase the Jenkins `timeout()`. |
| Disk usage keeps growing | Verify the cleanup stage completed successfully. |
