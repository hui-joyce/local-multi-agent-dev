# Scripts

Command-line reference for the three utilities in this directory. For what they are for and when you would run them, see the [repository README](../README.md).

All three load `.env` before importing anything that could reach the network.

## `update_security_notes.py`

Downloads Apple Security Notes into `data/security_notes/ios-<version>.json`. This is one of the two setup steps that need network access. During analysis the pipeline reads only the cache and never goes online, so an advisory that was never cached simply produces no matches.

```bash
python3 scripts/update_security_notes.py 26.4.1 26.4.2   # several versions in one call
python3 scripts/update_security_notes.py 17.1 --archive
python3 scripts/update_security_notes.py 26.4.2 --force
python3 scripts/update_security_notes.py --list
```

| Argument | Purpose |
|---|---|
| `versions` | One or more iOS versions. Accepts several per invocation |
| `--archive` | Fall back to the Internet Archive for releases Apple has removed from its index. Slower and third-party, acquisition only |
| `--force` | Re-download versions already in the cache |
| `--list` | Print cached versions and the cache path, then exit |

The cache is committed to the repository, so a fresh clone can match components against Apple's advisories with no setup. `SECURITY_NOTES_DIR` overrides the location.

## `qdrant.py`

Populates and inspects the embedded Qdrant database. Retrieval is optional: both domain graphs run normally when the collections are empty.

```bash
python3 scripts/qdrant.py load --file notes.md --domain shared
python3 scripts/qdrant.py load --dir ./knowledge_base --domain software_dev --chunk-size 512 --overlap 100
python3 scripts/qdrant.py load --file chunks.jsonl --domain shared
python3 scripts/qdrant.py inspect --sample 10
```

### `load`

| Argument | Default | Purpose |
|---|---|---|
| `--file` | | Single file to load. Mutually exclusive with `--dir` |
| `--dir` | | Directory to walk. Mutually exclusive with `--file` |
| `--domain` | required | One of `software_dev`, `reverse_engineering`, `shared` |
| `--chunk-size` | `512` | Chunk size in words. Plain text only |
| `--overlap` | `100` | Word overlap between chunks. Plain text only |
| `--extensions` | `.md,.markdown,.txt,.jsonl` | Which extensions `--dir` picks up |

Chunking depends on the file type. Markdown splits on headers, so `--chunk-size` and `--overlap` are ignored. Plain text splits by word count. Each JSONL line is treated as a pre-chunked record with `text` and optional `metadata`.

Every chunk carries `source_file`, `chunk_index`, `total_chunks`, and `file_type` metadata.

### `inspect`

| Argument | Default | Purpose |
|---|---|---|
| `--sample` | `5` | Documents to preview per collection |

Collections live under `RAG_DB_PATH` (default `~/.local/share/qdrant`), one per domain: `agents_software_dev`, `agents_reverse_engineering`, `agents_shared`.

> Embedded Qdrant allows only one process at a time. Stop `langgraph dev` before loading or inspecting data.

## `automation.py`

Drives the four-stage Jenkins firmware pipeline. Each stage is a separate build step so it can fail and retry independently. See [../docs/jenkins_setup.md](../docs/jenkins_setup.md) for the job configuration.

```bash
python3 scripts/automation.py check
python3 scripts/automation.py download
python3 scripts/automation.py analyze
python3 scripts/automation.py cleanup
```

| Stage | Purpose | Notable exit |
|---|---|---|
| `check` | Detect a build newer than `last_known_builds.json` | `2` when there is nothing new, which skips the rest of the job |
| `download` | Fetch the new build plus a release to diff against, and cache both advisories | `2` when no comparison pair can be resolved |
| `analyze` | Run the orchestration graph over each firmware pair | `1` when no pair produced a report |
| `cleanup` | Prune superseded IPSWs to conserve disk | |

Exit codes are the contract with Jenkins: `0` success, `1` error, `2` nothing to do. State passes through `.jenkins_pipeline/`, so no plugins beyond the suggested set are required.

A build is recorded as seen only once `analyze` has processed it. A run that fails to download or analyse is retried on the next pass rather than skipped for good.

`analyze` calls the same `OrchestrationRuntime.run()` entry point as the chat UI and the API. It passes the firmware pair as resolved state instead of requiring the model to parse it from a sentence, but it is a driver, not a second implementation.

Relevant environment variables: `PIPELINE_DEVICES`, `PIPELINE_DEVICE_FAMILY`, `PIPELINE_KEEP_PER_DEVICE`, `PIPELINE_DOWNLOAD_TIMEOUT`, `PIPELINE_STALE_PARTIAL_DAYS`. All are documented in [../.env.example](../.env.example).
