# Workflow Modernization: Tools and deps update (`tools.yml`)

## Section 1: Overview & Purpose

The `tools.yml` workflow automates routine weekly dependency and tooling updates across 31 individual components in the Node.js source tree (including `amaro`, `acorn`, `brotli`, `c-ares`, `corepack`, `googletest`, `gyp-next`, `libuv`, `llhttp`, `nghttp2`, `simdjson`, `sqlite`, `undici`, `zlib`, etc.). For each tool, a dedicated shell script in `tools/dep_updaters/` evaluates upstream releases, updates local fixtures/headers, tests the changes, and uses `peter-evans/create-pull-request` to open or update a dedicated PR on branch `actions/tools-update-<id>`.

### Failure Root Cause Analysis
In non-enterprise and fork environments, this workflow failed completely (see run [41060368938](https://github.com/sajuptpm/node/actions/runs/41060368938)):
1. **Missing Bot Token**: The step `peter-evans/create-pull-request` required `token: ${{ secrets.GH_USER_TOKEN }}`. When this secret is missing or empty, the action aborts before evaluating whether code changes exist.
2. **Missing Subsystem Script Token**: The step `run: ${{ matrix.run }}` passed `GITHUB_TOKEN: ${{ secrets.GH_USER_TOKEN }}` to dependency update scripts (such as GitHub release queries). In forks without this secret, API calls suffered from anonymous rate limits.
3. **Restricted Workflow Permissions**: Upstream only configured `permissions: contents: read`. Creating update branches and pull requests requires `contents: write` and `pull-requests: write`.
4. **Hardcoded Upstream Repository Check**: The workflow guard restricted execution to `github.repository == 'nodejs/node'`, skipping scheduled execution on all forks.
5. **Runner Concurrency Saturation**: Manual dispatch defaulted to `id: all`, launching 31 matrix jobs concurrently and exhausting runner quotas.

---

## Section 2: Dual-Mode Architecture & Changes Summary

```mermaid
flowchart TD
    Trigger([Trigger: workflow_dispatch or schedule]) --> Runner[Matrix Job: tools-deps-update]
    Runner --> CheckSkip{inputs.id matches matrix.id or 'all'?}
    CheckSkip -->|No| SkipJob[Job finishes cleanly in 1s]
    CheckSkip -->|Yes| Checkout[actions/checkout@v4]
    
    Checkout --> ExecScript[Execute dep updater script via matrix.run]
    ExecScript --> ModeResolve{Resolve Mode & dry_run}
    
    ModeResolve -->|original AND dry_run == false AND has_changes| OriginalMode[peter-evans/create-pull-request]
    ModeResolve -->|native OR dry_run == true| NativeMode[Generate Tool Audit Report & Step Summary]
    
    OriginalMode --> RemotePR[Submit / Update Remote Pull Request]
    NativeMode --> Artifacts[Upload tools-update-<id>-report Artifact]
```

### Key Changes Implemented
- **Dual-Mode Architecture & Safe Dry-Run**: Added execution mode (`auto | native | original`) and `dry_run: true` default. In `native` mode, dependency status and proposed PR metadata are summarized and exported as artifacts without mutating remote Git refs.
- **Token Fallback Hierarchy**: Replaced `${{ secrets.GH_USER_TOKEN }}` with `${{ secrets.GH_USER_TOKEN || secrets.GITHUB_TOKEN }}` across all script executions and pull-request actions.
- **Permission Elevation**: Added `contents: write` and `pull-requests: write`.
- **Sensible Dispatch Defaults & Matrix Parallelism**: Defaulted manual dispatch `id` to `amaro` (fastest dependency to evaluate), added `max-parallel: 4` to prevent runner quota exhaustion, and made repository checks dynamic.
- **Structured Artifacts**: Packaged tool audit reports into `tools-update-<id>-report`.

---

## Section 3: Existing Solutions vs. Free Alternatives Analysis

| Feature | Upstream Original Mode | Active GitHub-Native Alternative |
| :--- | :--- | :--- |
| **Authentication Token** | Requires `secrets.GH_USER_TOKEN` | Falls back to `${{ secrets.GITHUB_TOKEN }}` |
| **Pull Request Creation** | `peter-evans/create-pull-request` | Structured GitHub Step Summary + Downloadable Markdown report |
| **Permissions** | `contents: read` (fails PR creation) | `contents: write`, `pull-requests: write` |
| **Manual Dispatch Target** | Defaults to `all` (31 jobs) | Defaults to `amaro` (single target for fast smoke testing) |
| **Concurrency Control** | Unbounded matrix execution | `max-parallel: 4` to prevent runner saturation |
| **Cost & Licensure** | Enterprise credentials required | 100% Free, GitHub-native |

---

## Section 4: Configuration & Data Requirements

### Repository Secrets
| Secret Name | Required (Original) | Required (Native) | Description |
| :--- | :--- | :--- | :--- |
| `GH_USER_TOKEN` | Yes | No | GitHub PAT with `repo` and `workflow` scopes |

### Repository Variables
| Variable Name | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `RUNNER_LABEL` | No | `ubuntu-latest` | Custom runner image |
| `WORKFLOW_MODE` | No | `auto` | Global mode override (`auto`, `native`, `original`) |
| `ENABLE_TOOLS_UPDATE` | No | `false` | Enable scheduled cron updates on forks |

### Workflow Permissions
| Scope | Configured | Reason |
| :--- | :--- | :--- |
| `contents` | `write` | Required to create update branches and checkout code |
| `pull-requests` | `write` | Required for pull request generation in original mode |

---

## Section 5: Live Test Verification Details

*(Pending live GitHub Actions dispatch execution — will be populated with exact run details immediately following dispatch).*

---

## Section 6: How to Test Later

### 1. GitHub CLI (`gh`)
```bash
# Smoke test tool update for 'amaro' in Native Mode
gh workflow run tools.yml --ref main -f id=amaro -f mode=native -f dry_run=true

# Test a different dependency e.g. 'ada'
gh workflow run tools.yml --ref main -f id=ada -f mode=native -f dry_run=true
```

### 2. Python Dispatch Script (`workflow-fixes/test-dispatch-tools.py`)
```python
import os, requests

TOKEN = os.environ.get("GH_TOKEN")
REPO = "sajuptpm/node"
url = f"https://api.github.com/repos/{REPO}/actions/workflows/tools.yml/dispatches"
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
payload = {
    "ref": "main",
    "inputs": {
        "id": "amaro",
        "mode": "native",
        "dry_run": "true"
    }
}
resp = requests.post(url, headers=headers, json=payload)
print(f"Status: {resp.status_code}")
```

---

## Section 7: Step-by-Step GitHub UI Manual Verification Guide

1. Navigate to your repository: `https://github.com/<owner>/node`.
2. Click the **Actions** tab.
3. In the left workflow sidebar, click **Tools and deps update**.
4. Click the **Run workflow** dropdown button on the right.
5. In the input dialog:
   - **Use workflow from**: Select `main`.
   - **The ID of the job to run**: Select `amaro` (or any tool from the list).
   - **Execution mode**: Select `native`.
   - **Smoke test tool/dep update (dry_run)**: Keep checked (`true`).
6. Click the green **Run workflow** button.
7. Refresh and select the newly created workflow run.
8. Verify:
   - Run finishes with status `success` (`✓`).
   - The job for the selected tool (e.g., `amaro`) runs to completion.
   - The **Summary** tab displays the **Tools & Deps Update: amaro** audit table.
   - The artifact `tools-update-amaro-report` is available for download under Artifacts.
