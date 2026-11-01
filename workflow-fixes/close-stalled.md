# Workflow Modernization: Close Stalled Issues and PRs (`close-stalled.yml`)

## Section 1: Overview & Purpose

The `close-stalled.yml` workflow automatically cleans up stale and abandoned pull requests and issues labeled `stalled` in the Node.js repository. In upstream `nodejs/node`, it runs on a daily schedule (`0 0 * * *`) using `actions/stale`, closing items that have had the `stalled` label for 30 or more days with an explanatory notification message.

### Upstream Issues & Fork Failure Points
1. **Hardcoded Upstream Repository Check**: `if: github.repository == 'nodejs/node'` prevented the workflow from executing on forks or non-enterprise mirrors.
2. **Proprietary Runner**: Hardcoded `runs-on: ubuntu-slim`, which does not exist in standard GitHub-hosted runner pools.
3. **Lack of Manual Dispatch (`workflow_dispatch`)**: The workflow only ran on cron schedule, making testing and validation impossible on demand.
4. **Risk of Accidental Bulk Closure**: Running directly in live mode on a fork without a dry-run mechanism could accidentally close open issues or PRs without prior review.

---

## Section 2: Dual-Mode Architecture & Changes Summary

The modernized workflow introduces a flexible **Dual-Mode Architecture**:

```mermaid
flowchart TD
    Trigger["Trigger: schedule or workflow_dispatch"] --> ModeResolution{"Resolve Mode<br/>(auto / native / original)"}
    
    ModeResolution -->|dry_run=true OR mode=native<br/>(100% Free / Fork-Friendly)| NativeFlow["Active GitHub-Native Flow<br/>- Query issues & PRs labeled 'stalled' via gh CLI<br/>- Run actions/stale with debug-only: true<br/>- Render Step Summary Table<br/>- Upload close-stalled-report artifact"]
    
    ModeResolution -->|dry_run=false & mode=original<br/>(Upstream Behavior)| OriginalFlow["Original Live Mutation Flow<br/>- Run actions/stale with debug-only: false<br/>- Close eligible issues & PRs with CLOSE_MESSAGE"]
    
    NativeFlow --> Finish["Clean Pipeline Completion"]
    OriginalFlow --> Finish
```

### Key Changes
1. **Added `workflow_dispatch` Trigger**: Supports `mode` (`auto`, `native`, `original`), `dry_run` (boolean), `days_before_close` (number), and `operations_per_run` (number).
2. **Dynamic Repository Guard**: Changed `if: github.repository == 'nodejs/node'` to `github.repository == 'nodejs/node' || github.repository_owner == 'sajuptpm' || github.event_name == 'workflow_dispatch' || vars.ENABLE_CLOSE_STALLED == 'true'`.
3. **Dynamic Runners**: Replaced `ubuntu-slim` with `${{ vars.RUNNER_LABEL || 'ubuntu-latest' }}`.
4. **Active GitHub-Native Mode**: Queries items via `gh` CLI, runs `actions/stale` with `debug-only: true`, emits a Markdown summary table, and uploads `close-stalled-report.md`.
5. **Zero Skipped Jobs Policy**: Job `stale` runs, generates reports, and cleanly completes in all environments.

---

## Section 3: Existing Solutions vs. Free Alternatives Analysis

| Feature | Upstream Original Mode | Active GitHub-Native Alternative |
| :--- | :--- | :--- |
| **Execution Safety** | Live closures only (irreversible) | Safe dry-run audit (`debug-only: true`) |
| **Trigger Mechanism** | Scheduled Cron only (`0 0 * * *`) | Scheduled Cron + `workflow_dispatch` (with inputs) |
| **Runner Image** | `ubuntu-slim` | `${{ vars.RUNNER_LABEL \|\| 'ubuntu-latest' }}` |
| **Reporting** | Actions debug logs only | `$GITHUB_STEP_SUMMARY` table + `close-stalled-report` artifact |
| **Dependencies** | GitHub API only | 100% Free, zero third-party dependencies |

---

## Section 4: Configuration & Data Requirements

### Repository Secrets
No proprietary secrets required (`$GITHUB_TOKEN` is used automatically).

### Repository Variables
| Variable Name | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `RUNNER_LABEL` | Optional | `ubuntu-latest` | Default runner label for jobs |
| `ENABLE_CLOSE_STALLED` | Optional | `false` | Enable scheduled runs on non-upstream forks |
| `CLOSE_STALLED_MODE` | Optional | `auto` | Global mode override (`auto`, `native`, `original`) |

### Permissions
| Scope | Level | Purpose |
| :--- | :--- | :--- |
| `contents` | `read` | Read repository contents |
| `issues` | `write` | Query and close stale issues |
| `pull-requests` | `write` | Query and close stale PRs |

---

## Section 5: Live Test Verification Details

*(Pending live GitHub Actions dispatch execution — will be populated with exact run details immediately following dispatch).*

---

## Section 6: How to Test Later

### 1. GitHub CLI (`gh`)
```bash
# Run safe dry-run audit
gh workflow run close-stalled.yml --ref main -f dry_run=true -f mode=native

# Test with a shorter 7-day threshold in dry-run mode
gh workflow run close-stalled.yml --ref main -f dry_run=true -f mode=native -f days_before_close=7
```

### 2. Python Dispatch Script (`workflow-fixes/test-dispatch-close-stalled.py`)
```python
import os, requests

TOKEN = os.environ.get("GH_TOKEN")
REPO = "sajuptpm/node"
url = f"https://api.github.com/repos/{REPO}/actions/workflows/close-stalled.yml/dispatches"
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
payload = {
    "ref": "main",
    "inputs": {
        "dry_run": "true",
        "mode": "native",
        "days_before_close": "30"
    }
}
resp = requests.post(url, headers=headers, json=payload)
print(f"Status: {resp.status_code}")
```

---

## Section 7: Step-by-Step GitHub UI Manual Verification Guide

1. Navigate to the repository: `https://github.com/<owner>/node`.
2. Click the **Actions** tab.
3. In the left workflow sidebar, click **Close stalled issues and PRs**.
4. Click the **Run workflow** dropdown button on the right.
5. In the input dialog:
   - **Use workflow from**: Select `main`.
   - **Execution mode**: Select `native`.
   - **Audit stalled issues and PRs without actually closing them**: Ensure checked (`true`).
   - **Days before closing stalled items**: Enter `30` (or leave default).
6. Click the green **Run workflow** button.
7. Refresh the page and click the newly started run.
8. Verify:
   - Job `Process Stalled Issues & PRs` completes with status `success` (`✓`) in ~10 seconds.
   - The **Summary** tab displays the **Close Stalled Issues & PRs Audit Summary** table.
   - The artifact `close-stalled-report` is generated and available for download.
