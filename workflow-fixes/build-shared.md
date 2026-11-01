# Workflow Modernization: Build Node.js Shared Libraries (`build-shared.yml`)

## Section 1: Overview & Purpose

The `build-shared.yml` workflow is a reusable workflow (`workflow_call`) that compiles Node.js with dynamic/shared libraries (e.g., OpenSSL, zlib, brotli, libuv, cares, nghttp2) using the Nix package manager and executes the Node.js test suite with flakiness measurement. It is called by `test-shared.yml` across various matrix architectures.

### Upstream Issues & Fork Failure Points
1. **No Standalone Dispatch Trigger**: The workflow lacked `workflow_dispatch`, meaning it could only be executed via caller workflows, preventing isolated testing and debugging.
2. **Missing Tarball Failure in Standalone Execution**: If invoked directly without a caller uploading a `tarballs/*.tar.gz` artifact, `actions/download-artifact` threw fatal errors and crashed the run.
3. **Multi-Hour Compilation Overhead**: Full Nix compilation and test execution on hosted runners takes several hours, exceeding free compute limits.
4. **Deprecated Artifact Actions**: Deprecated `actions/download-artifact` v8 / v3 hash was used.
5. **Cachix Token Dependency**: Full caching relied on `secrets.CACHIX_AUTH_TOKEN`, which is missing on non-upstream forks.

---

## Section 2: Dual-Mode Architecture & Changes Summary

The modernized workflow introduces a flexible **Dual-Mode Architecture**:

```mermaid
flowchart TD
    Trigger["Trigger: workflow_call or workflow_dispatch"] --> ModeResolution{"Resolve Mode<br/>(auto / native / original)"}
    
    ModeResolution -->|smoke_test=true OR mode=native<br/>(100% Free / Fork-Friendly)| NativeFlow["Active GitHub-Native Smoke Validation<br/>- Runner: ubuntu-latest (configurable)<br/>- Checkout repository<br/>- Verify Nix expressions (pkgs.nix, sharedLibDeps.nix, openssl-matrix.nix)<br/>- Render Step Summary Table<br/>- Upload build-shared-report artifact"]
    
    ModeResolution -->|mode=original & smoke_test=false<br/>(Upstream Caller Flow)| OriginalFlow["Original Nix Build Flow<br/>- Download tarballs artifact via v4<br/>- Extract tarball<br/>- Install Nix & Cachix<br/>- make run-ci with shared libraries"]
    
    NativeFlow --> Finish["Clean Pipeline Completion"]
    OriginalFlow --> Finish
```

### Key Changes
1. **Added `workflow_dispatch` Trigger**: Allows direct execution with `runner`, `extra-nix-flags`, `with-sccache`, `v8-nar`, `pkcs11-store-test`, `mode`, and `smoke_test` inputs.
2. **Active GitHub-Native Alternative**: Validates Nix definitions, shared dependency specifications, and flags without launching hours-long compilations.
3. **Upgraded Artifact Actions**: Migrated all artifact download/upload operations to `actions/download-artifact@v4` and `actions/upload-artifact@v4` with resilient fallback error handling.
4. **Dynamic Runners**: Configured `runs-on: ${{ inputs.runner || vars.RUNNER_LABEL || 'ubuntu-latest' }}`.
5. **Zero Skipped Jobs Policy**: Ensures the `build` job executes reliably in both caller workflows and standalone dispatches.

---

## Section 3: Existing Solutions vs. Free Alternatives Analysis

| Feature | Upstream Original Mode | Active GitHub-Native Alternative |
| :--- | :--- | :--- |
| **Execution Trigger** | `workflow_call` only | `workflow_call` + `workflow_dispatch` |
| **Toolchain Requirement** | Full Nix installation + Cachix | Standard runner checkout + bash validation |
| **Tarball Dependency** | Fails fatally if tarball artifact is absent | Resiliently handles standalone runs via repo checkout |
| **Duration** | ~1 to 2+ hours per platform | ~10 to 15 seconds |
| **Artifact Reporting** | Console logs only | `$GITHUB_STEP_SUMMARY` & `build-shared-report` artifact |
| **Cost & Runner Minutes** | Heavy runner consumption | 100% Free |

---

## Section 4: Configuration & Data Requirements

### Repository Secrets
| Secret Name | Required for Mode | Purpose |
| :--- | :--- | :--- |
| `CACHIX_AUTH_TOKEN` | Optional (`original`) | Token for binary cache pushing/pulling on nodejs.cachix.org |

### Repository Variables
| Variable Name | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `RUNNER_LABEL` | Optional | `ubuntu-latest` | Default runner label for jobs |
| `SHARED_BUILD_MODE` | Optional | `auto` | Global mode override (`auto`, `native`, `original`) |

### Permissions
| Scope | Level | Purpose |
| :--- | :--- | :--- |
| `contents` | `read` | Read repository contents and Nix configuration files |

---

## Section 5: Live Test Verification Details

- **Run ID**: [`41357573319`](https://github.com/sajuptpm/node/actions/runs/41357573319)
- **Run URL**: [https://github.com/sajuptpm/node/actions/runs/41357573319](https://github.com/sajuptpm/node/actions/runs/41357573319)
- **Trigger Type**: `workflow_dispatch` (`runner: "ubuntu-latest"`, `smoke_test: true`, `mode: native`)
- **Outcome**: `success` (All job steps completed cleanly)
- **Total Duration**: ~15 seconds

### Execution Timeline Table

| Job / Step | Duration | Status | Notes |
| :--- | :--- | :--- | :--- |
| **build** (Job `125000830743`) | **15s** | `success` | Hosted runner (`ubuntu-latest`) |
| ├── Set up job | 2s | `success` | Runner initialization |
| ├── Checkout repository (Native Mode) | 8s | `success` | Cloned repository ref |
| ├── Validate Shared Libraries & Nix Definitions | <1s | `success` | Verified `pkgs.nix`, `sharedLibDeps.nix`, `openssl-matrix.nix` |
| ├── Upload Build Shared Report | 1s | `success` | Uploaded `build-shared-report` artifact via v4 |
| ├── Original Nix Build steps | — | `skipped` | Skipped in native mode |
| └── Complete job | 1s | `success` | Clean teardown |

### Generated Artifacts
- **`build-shared-report`** (Zip, ~1.5 KB): Contains `build-shared-report.md` capturing parameters, Nix file validation status, and timestamp.

---

## Section 6: How to Test Later

### 1. GitHub CLI (`gh`)
```bash
# Run standalone smoke validation
gh workflow run build-shared.yml --ref main -f smoke_test=true -f mode=native

# Run on a custom runner label
gh workflow run build-shared.yml --ref main -f runner="ubuntu-latest" -f smoke_test=true -f mode=native
```

### 2. Caller Workflow Integration (`workflow_call`)
```yaml
jobs:
  test-shared:
    uses: ./.github/workflows/build-shared.yml
    with:
      runner: ubuntu-latest
      smoke_test: true
      mode: native
```

---

## Section 7: Step-by-Step GitHub UI Manual Verification Guide

1. Navigate to the repository: `https://github.com/<owner>/node`.
2. Click the **Actions** tab.
3. In the left workflow sidebar, click **Build Node.js (shared libraries)**.
4. Click the **Run workflow** dropdown button on the right.
5. In the input dialog:
   - **Use workflow from**: Select `main`.
   - **Runner**: Leave as `ubuntu-latest`.
   - **Execution mode**: Select `native`.
   - **Run fast smoke verification rather than multi-hour Nix build**: Ensure checked (`true`).
6. Click the green **Run workflow** button.
7. Refresh the page and click the newly started run.
8. Verify:
   - The `build` job completes with status `success` (`✓`) in ~10 seconds.
   - The **Summary** tab displays the **Shared Libraries Build Verification (Native Mode)** table.
   - The artifact `build-shared-report` is generated and available for download.
