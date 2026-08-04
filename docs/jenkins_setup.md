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
   - Repository URL: `/Users/user/Documents/GitHub/local-multi-agent-dev`
   - Branch Specifier: the branch you deploy from, e.g. `*/langgraph`
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
