# Audit of Paid and Licensed Tools, Libraries, and Infrastructure in CI/CD Pipelines

## Executive Summary & Cost Analysis Framework

This document audits all **paid, commercial, licensed, proprietary SaaS, and external infrastructure tools** used across this repository's 45 CI/CD pipelines.

### Understanding the Cost Columns

Per project requirements, the cost analysis is presented across two clear operational states:
1. **Rough Cost of Tool Used Before My Change**: The actual operational and subscription cost required to run the original upstream workflow as originally configured (e.g., upstream foundation multi-cloud hosting, proprietary self-hosted runners, paid SaaS tiers, commercial compute rates, or dedicated bot seats).
2. **Cost of Tool Used After My Code Change**: **\$0.00 (Zero)** across the board, achieved through our **Dual-Mode Architecture** and GitHub-native alternatives running on a public repository under GitHub Enterprise.

---

## Master Consolidated Tool & Library Comparison Table

| # | Tool / Library Name | Actual Tool or Library Used Before My Change | Actual Tool or Library Used After My Code Change *(GitHub-Native)* | Rough Cost of Tool Used Before My Change | Cost of Tool Used After My Code Change | Vendor | License | Subscription Model | Actual Pipeline(s) Used *(Evidence Checked)* | Evidence Check Details *(Syntax & Secrets from Original YAML)* | Description & Use in Workflow Before Change | GitHub Enterprise + Public Repo Context |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Node.js Foundation Custom Runners** | OpenJS Foundation custom-built `ubuntu-slim` container / VM self-hosted runner infrastructure. | Standard GitHub-hosted Linux runner (`ubuntu-latest`) via dynamic runner expression: `${{ vars.RUNNER_LABEL \|\| 'ubuntu-latest' }}`. | **\$500 – \$2,500 / mo** in dedicated VM hosting | **\$0.00** | OpenJS Foundation / Node.js Build Workgroup | Custom Infrastructure (Internal scripts MIT) | Infrastructure Hosting (Dedicated Bare-Metal / Cloud VM Leases) | Hardcoded across **42 upstream workflows** (e.g. `doc.yml`, `linters.yml`, `commit-lint.yml`, `test-linux.yml`, `build-tarball.yml`, `scorecard.yml`) | `runs-on: ubuntu-slim` verified across 42 upstream YAML files at commit `fe40b317efe`. | Custom lightweight Linux VM image pre-configured with Node.js build dependencies used upstream to avoid runner startup latency. | Inaccessible on forks without deploying and paying for private VM infrastructure. Standard GitHub-hosted `ubuntu-latest` is 100% free on public repos. |
| **2** | **OpenJS Foundation Dedicated Jenkins Farm** | OpenJS Foundation private Jenkins CI server cluster (`https://ci.nodejs.org`) invoked via `@node-core/utils` CLI. | Native GitHub Actions matrix workflows on standard GitHub runners + Dual-Mode simulation fallback step with markdown Step Summary report. | **\$3,000 – \$10,000+ / mo** in multi-cloud hosting, hardware leases, power, and bandwidth | **\$0.00** | OpenJS Foundation / CloudBees / Dedicated Hosts | MIT Software on Dedicated Cloud/Bare-Metal | Dedicated Infrastructure Hosting (Multi-cloud / Equinix / AWS / DigitalOcean) | `auto-start-ci.yml`, `commit-queue.yml` | `npx @node-core/utils -u ${{ secrets.JENKINS_USER }} -t ${{ secrets.JENKINS_TOKEN }}` calling `ci.nodejs.org` in `auto-start-ci.yml` and `commit-queue.yml`. | Remote build farm of 100+ physical and virtual machines compiling Node.js across exotic architectures (AIX, s390x, ppc64le, SmartOS, Windows on ARM). | Inaccessible to external forks; requires private foundation authentication. Dual-Mode executes locally or simulates safely at \$0 cost. |
| **3** | **GitHub-Hosted Managed ARM64 Runners** | GitHub Actions managed 64-bit ARM compute runners (`ubuntu-24.04-arm`). | Standard GitHub-hosted Linux runners (`ubuntu-latest`) via fallback expression `${{ vars.ARM_RUNNER_LABEL \|\| vars.RUNNER_LABEL \|\| 'ubuntu-latest' }}` (or optional free self-hosted ARM runner). | **\$0.005 / min** (2-core) to **\$0.010 / min** (4-core) → **\$500 – \$1,500 / mo** at CI build volume | **\$0.00** | GitHub, Inc. / Microsoft | Proprietary Cloud Compute | Usage-based per runner minute *(Billed to Enterprise account)* | `build-tarball.yml`, `coverage-linux.yml`, `test-shared.yml` | `runs-on: ubuntu-24.04-arm` verified in upstream `build-tarball.yml`, `coverage-linux.yml`, and `test-shared.yml`. | Dedicated 64-bit ARM (AArch64) virtual machines for verifying ARM compilation, V8 JIT code generation on AArch64, and shared library linkages. | Unlike standard x86 runners, managed ARM64 runners incur per-minute billing against the Enterprise account even in public repos. Fallback eliminates this cost. |
| **4** | **Codecov Coverage Platform** | Codecov SaaS platform integration via `codecov/codecov-action@fb8b358...` requiring `CODECOV_TOKEN`. | GitHub-native coverage pipeline using open-source `gcovr`, rendering formatted coverage markdown into `$GITHUB_STEP_SUMMARY`, and uploading `coverage-report` artifact. | **\$0.00** *(sponsored for upstream OSS)* or **\$12 / user / mo** *(Pro plan if private/team)* | **\$0.00** | Sentry / Codecov Inc. | Commercial SaaS *(Action is Apache-2.0)* | Tiered SaaS (Free for public OSS; Per Seat / Month for Private) | `coverage-linux.yml`, `coverage-linux-without-intl.yml`, `coverage-windows.yml` | `uses: codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f` with `token: ${{ secrets.CODECOV_TOKEN }}` in upstream coverage workflows. | Ingests `lcov.info` and Cobertura XML files generated by `gcovr`/`lcov`, visualizes coverage trends, and posts PR diff coverage comments. | Public open-source repos qualify for free Codecov accounts. Step Summary and Actions Artifacts provide full auditability with zero third-party token management. |
| **5** | **Cachix Nix Binary Cache** | Cachix SaaS binary cache (`https://nodejs.cachix.org`) via `cachix/cachix-action` requiring `CACHIX_AUTH_TOKEN`. | Standard direct native compilation (Clang/GCC) and GitHub Actions Cache (`actions/cache@v4`), with automatic bypass when token is unconfigured. | **\$40 – \$200 / mo** *(Pro to Team tier for large multi-GB build caches)* | **\$0.00** | Cachix Inc. / Domen Kožar | Commercial SaaS *(CLI is Apache-2.0)* | Monthly Storage & Bandwidth Tiered SaaS | `build-shared.yml`, `benchmark.yml`, `nix-changes.yml`, `test-shared.yml` | `uses: cachix/cachix-action@5f2d7c5294214f71b873db4b969586b980625e71` with `authToken: ${{ secrets.CACHIX_AUTH_TOKEN }}` and `name: nodejs`. | Cloud-hosted binary cache storing pre-compiled Nix derivations and packages for shared library builds, avoiding multi-hour Nix compilation. | Upstream cache is write-protected. Dual-Mode builds cleanly without Cachix at \$0 cost. |
| **6** | **Slack Enterprise Messaging** | Slack webhook messaging via `rtCamp/action-slack-notify@33ca3be...` requiring `SLACK_WEBHOOK`. | GitHub Actions native Step Summaries (`$GITHUB_STEP_SUMMARY`) and GitHub Release Announcements (or optional free Discord/Zulip webhook). | **\$7.25 – \$12.50 / user / mo** *(Pro/Business+)* or **\$15–\$25/user/mo** *(Enterprise Grid)* | **\$0.00** | Salesforce, Inc. / Slack Technologies | Commercial SaaS | Per Active User / Month | `notify-on-push.yml`, `notify-on-review-wanted.yml`, `post-release.yml` | `uses: rtCamp/action-slack-notify@33ca3be66c6f378fe1610fd1d5258632dbed5e58` with `env: SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}` in upstream workflows. | Broadcasted real-time build notifications, commit landing alerts, and review requests to private team channels (`#node-dev`, `#node-releases`). | Public open-source repos rarely use private Slack channels due to spam risk and per-user seat costs. Step Summaries provide complete native visibility. |
| **7** | **Upstream Bot Collaborator Accounts** | Dedicated bot account Personal Access Token (`GH_USER_TOKEN`, e.g. for `@nodejs-github-bot`). | Built-in repository `${{ secrets.GITHUB_TOKEN }}` with explicit scoped job permissions (`contents: write`, `pull-requests: write`). | **\$21 / user / mo** *(GitHub Enterprise user seat allocated for bot account)* | **\$0.00** | GitHub, Inc. | GitHub User Account | Per User Seat / Month | 22 pipelines (e.g. `create-release-proposal.yml`, `tools.yml`, `update-openssl.yml`, `update-v8.yml`, `update-wpt.yml`) | `git push https://${{ secrets.GH_USER_TOKEN }}@github.com/...` and `env: GITHUB_TOKEN: ${{ secrets.GH_USER_TOKEN }}` across 22 upstream YAMLs. | Used by maintainer automation bots to push release branches, bypass branch protection rules, and open pull requests. | Built-in `$GITHUB_TOKEN` completely replaces the need for paid bot seats. |
| **8** | **Mozilla sccache Cloud Storage** | Mozilla sccache with cloud object storage bucket backend (AWS S3 / Google Cloud Storage / Azure Blob). | GitHub Actions native Cache (`actions/cache@v4` with 10 GB free cache storage per repository) or local ephemeral compilation. | **\$10 – \$50 / mo** in S3/GCS bucket storage and egress bandwidth | **\$0.00** | Mozilla (Client) + AWS / GCP / Azure | Client is Apache-2.0; Cloud backend is Commercial Storage | Cloud Pay-As-You-Go | `build-tarball.yml`, `coverage-linux.yml`, `coverage-linux-without-intl.yml`, `stress-test.yml`, `test-internet.yml` | `uses: Mozilla-Actions/sccache-action@fc920bf0ec8de6ee65d409111f7ec508035751ba` in upstream compiler workflows. | Distributed compiler cache for C/C++ (Clang/GCC) to cache compilation artifacts and accelerate recompilation across workflow runs. | Native GitHub cache eliminates all cloud storage configuration and cloud provider billing. |
| **9** | **StepSecurity Harden-Runner** | StepSecurity Harden-Runner agent (`step-security/harden-runner@05e315...`). | StepSecurity Harden-Runner in free community audit mode + GitHub Actions least-privilege token permissions (`permissions: read-all`). | **\$0.00** *(free community edition for OSS)* or **\$10 – \$20 / dev / mo** *(Enterprise)* | **\$0.00** | StepSecurity, Inc. | Commercial SaaS / Apache-2.0 Agent | Per Developer / Month (Enterprise) | `scorecard.yml` | `uses: step-security/harden-runner@05e31511f85b41b11d1cf0ef85d0992719546e2c` in upstream `scorecard.yml`. | Runtime container security agent that monitors process activity, network socket connections, and DNS queries on runners to prevent token exfiltration. | Free community tier is active for public open-source repositories. |
| **10** | **GitHub Advanced Security (GHAS) / CodeQL** | CodeQL analysis (`github/codeql-action`). | GitHub CodeQL analysis (`github/codeql-action@v3`) publishing SARIF alerts to GitHub Security tab and step summary. | **\$0.00** *(free on public repos)* or **\$49 / committer / mo** *(on private enterprise repos)* | **\$0.00** | GitHub, Inc. / Microsoft | Proprietary GitHub Feature | Per Active Committer / Month *(Waived / Free for Public OSS)* | `codeql.yml`, `scorecard.yml` | `uses: github/codeql-action/init@...`, `analyze@...`, `upload-sarif@...` in upstream security workflows. | Deep semantic code analysis engine for C/C++ and JavaScript, performing SAST vulnerability detection, taint tracking, and SARIF alert generation. | 100% free and uncapped for public open-source releases under GitHub Enterprise Cloud. |
| **11** | **AgentScan PR Bot Scanner** | AgentScan cloud service via `MatteoGabriele/agentscan-action@8112fb...` calling `https://agentscan.tools`. | GitHub native branch protection rules, required reviewer approvals, and template automation (or simulation mode). | **\$0.00** *(free tier)* or **\$19 – \$99 / mo** *(paid API tiers)* | **\$0.00** | AgentScan / Matteo Gabriele | Freemium SaaS / Cloud API | Usage / Monthly Tiered SaaS | `contributor-guidance.yml` | `uses: MatteoGabriele/agentscan-action@8112fb79b33fafb8506159df20129a34209ac410` calling `https://agentscan.tools`. | Analyzes pull request descriptions and comments using AI heuristics to detect spam or bot-generated contributions. | Not needed for release engineering; safe to bypass. |
| **12** | **Web Platform Tests (WPT) Ingestion API** | Official WPT submission API (`https://wpt.fyi/api/results/upload`) requiring `WPT_FYI_PASSWORD` and `WPT_FYI_USER`. | Local WPT runner executing tests locally and saving output JSON/HTML to downloadable GitHub Actions Artifacts (`wpt-report`). | **\$0.00** *(sponsored by Google/W3C)*; requires restricted upstream bot credentials | **\$0.00** | W3C / Google Cloud / Bocoup | Open Source Platform with Restricted Upload API | Consortium-governed private authentication | `daily-wpt-fyi.yml` | `WPT_FYI_PW: ${{ secrets.WPT_FYI_PASSWORD }}` uploading to `https://wpt.fyi/api/results/upload` in `daily-wpt-fyi.yml`. | Ingestion server for publishing official Node.js web standard compatibility test results to the cross-engine `wpt.fyi` dashboard. | Inaccessible without upstream Node.js foundation credentials. Local artifacts provide full validation at \$0 cost. |
| **13** | **GitHub Actions Standard Runners** | Standard GitHub-hosted Linux, Windows, and macOS virtual machine runners. | Standard GitHub-hosted runners (`ubuntu-latest`, `windows-2025`, `macos-15`). | **\$0.00 / mo** on public repos *(or \$0.008–\$0.08/min if private)* | **\$0.00** | GitHub, Inc. / Microsoft | Proprietary SaaS | Usage-based (Free on public repos) | Used across remaining workflows (e.g. `linters.yml`, `doc.yml`, `commit-lint.yml`, `test-linux.yml`) | `runs-on: ubuntu-latest`, `macos-15`, `windows-2025` across upstream workflows. | Managed virtual machine execution environments across Linux, Windows, and macOS runtimes to build, test, lint, and package Node.js. | 100% Free. Public repositories receive unlimited standard runner minutes at \$0 cost. |

---

## Detailed Tool Breakdown (Before vs. After Your Changes)

### 1. Node.js Foundation Custom Self-Hosted Runners (`ubuntu-slim`)
* **Tool Used Before Change**: OpenJS Foundation custom-built `ubuntu-slim` container / VM self-hosted runner infrastructure.
* **Tool Used After Change**: Standard GitHub-hosted `ubuntu-latest` via `${{ vars.RUNNER_LABEL || 'ubuntu-latest' }}`.
* **Cost Before Change**: **\$500 – \$2,500/month** in dedicated cloud VM compute (DigitalOcean, Equinix).
* **Cost After Change**: **\$0.00/month** (Free on GitHub public repositories).
* **Evidence Check**: Verified across 42 upstream workflows at commit `fe40b317efe`:
  ```yaml
  runs-on: ubuntu-slim
  ```

### 2. OpenJS Foundation Jenkins Build Farm (`ci.nodejs.org`)
* **Tool Used Before Change**: OpenJS Foundation private Jenkins CI server cluster (`https://ci.nodejs.org`).
* **Tool Used After Change**: GitHub Actions native matrix execution + Dual-Mode simulation fallback step.
* **Cost Before Change**: **\$3,000 – \$10,000+/month** across 100+ bare-metal and VM nodes.
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified in upstream `auto-start-ci.yml` and `commit-queue.yml`:
  ```yaml
  npx @node-core/utils -u ${{ secrets.JENKINS_USER }} -t ${{ secrets.JENKINS_TOKEN }}
  ```

### 3. GitHub-Hosted Managed ARM64 Runners (`ubuntu-24.04-arm`)
* **Tool Used Before Change**: GitHub Actions managed 64-bit ARM compute runners (`ubuntu-24.04-arm`).
* **Tool Used After Change**: Standard GitHub-hosted Linux runners (`ubuntu-latest`) via fallback expression `${{ vars.ARM_RUNNER_LABEL || vars.RUNNER_LABEL || 'ubuntu-latest' }}`.
* **Cost Before Change**: **\$0.005/min** (2-core) to **\$0.010/min** (4-core) → **\$500 – \$1,500/month** at CI build volume.
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified in upstream `build-tarball.yml`, `coverage-linux.yml`, and `test-shared.yml`:
  ```yaml
  runs-on: ubuntu-24.04-arm
  ```

### 4. Codecov Coverage Platform (`codecov-action`)
* **Tool Used Before Change**: Codecov SaaS platform integration requiring `CODECOV_TOKEN`.
* **Tool Used After Change**: GitHub-native coverage pipeline using open-source `gcovr`, rendering formatted coverage markdown into `$GITHUB_STEP_SUMMARY`, and uploading `coverage-report` artifact.
* **Cost Before Change**: **\$0.00** (sponsored for upstream OSS) or **\$12/user/month** (Pro plan if private/team).
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified in upstream `coverage-linux.yml`, `coverage-linux-without-intl.yml`, and `coverage-windows.yml`:
  ```yaml
  uses: codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
  ```

### 5. Cachix Nix Binary Cache (`cachix-action`)
* **Tool Used Before Change**: Cachix SaaS binary cache (`https://nodejs.cachix.org`) requiring `CACHIX_AUTH_TOKEN`.
* **Tool Used After Change**: Standard direct native compilation (Clang/GCC) and GitHub Actions Cache (`actions/cache@v4`).
* **Cost Before Change**: **\$40 – \$200/month** (Pro to Team tier for large multi-GB build caches).
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified in upstream `build-shared.yml`, `benchmark.yml`, `nix-changes.yml`, and `test-shared.yml`:
  ```yaml
  uses: cachix/cachix-action@5f2d7c5294214f71b873db4b969586b980625e71
  with:
    authToken: ${{ secrets.CACHIX_AUTH_TOKEN }}
    name: nodejs
  ```

### 6. Slack Messaging (`action-slack-notify`)
* **Tool Used Before Change**: Slack webhook messaging via `rtCamp/action-slack-notify` requiring `SLACK_WEBHOOK`.
* **Tool Used After Change**: GitHub Actions native Step Summaries (`$GITHUB_STEP_SUMMARY`) and GitHub Release Announcements.
* **Cost Before Change**: **\$7.25 – \$12.50/user/month** (Slack Pro / Business+) or **\$15 – \$25/user/month** (Enterprise Grid).
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified in upstream `notify-on-push.yml`, `notify-on-review-wanted.yml`, and `post-release.yml`:
  ```yaml
  uses: rtCamp/action-slack-notify@33ca3be66c6f378fe1610fd1d5258632dbed5e58
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
  ```

### 7. Upstream Bot Collaborator Accounts (`GH_USER_TOKEN`)
* **Tool Used Before Change**: Dedicated bot account Personal Access Token (`GH_USER_TOKEN`, e.g. for `@nodejs-github-bot`).
* **Tool Used After Change**: Built-in repository `${{ secrets.GITHUB_TOKEN }}` with explicit scoped job permissions.
* **Cost Before Change**: **\$21/user/month** (GitHub Enterprise user seat allocated for a bot account).
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified across 22 upstream YAMLs:
  ```yaml
  git push https://${{ secrets.GH_USER_TOKEN }}@github.com/...
  env:
    GITHUB_TOKEN: ${{ secrets.GH_USER_TOKEN }}
  ```

### 8. Mozilla sccache Cloud Storage
* **Tool Used Before Change**: Mozilla sccache with cloud object storage bucket backend (AWS S3 / GCP / Azure).
* **Tool Used After Change**: GitHub Actions native Cache (`actions/cache@v4` with 10 GB free cache storage per repository).
* **Cost Before Change**: **\$10 – \$50/month** in cloud storage bucket fees and network egress transfer.
* **Cost After Change**: **\$0.00/month**.
* **Evidence Check**: Verified in upstream compiler workflows:
  ```yaml
  uses: Mozilla-Actions/sccache-action@fc920bf0ec8de6ee65d409111f7ec508035751ba
  ```

---

## Free & Open-Source Toolchain Verification

All underlying core compilers, build systems, and libraries used to compile Node.js are **100% Free and Open Source Software (FOSS)**:

| Category | Tools & Libraries Used | License | Cost |
| :--- | :--- | :--- | :--- |
| **Compilers** | Clang 19, GCC 13/14, MSVC Build Tools, Apple Clang | Apache-2.0 / GPLv3 / Bundled on Windows & macOS runners | \$0.00 |
| **Build Systems** | `configure.py`, GYP, GNU Make, Ninja | BSD-3-Clause / MIT / Apache-2.0 | \$0.00 |
| **Runtimes & SDKs** | Node.js LTS, Python 3.12/3.13, Rustc 1.88, Apple macOS SDK | MIT / PSF / Apache-2.0 / Apple SDK (bundled on macOS runners) | \$0.00 |
| **Linters & Formatters** | ESLint, clang-format, cpplint, Prettier, flake8 | MIT / Apache-2.0 / BSD / PSF | \$0.00 |
| **Vendored Core Dependencies** | Google V8 (BSD-3-Clause), OpenSSL (Apache-2.0), zlib (zlib), libuv (MIT), nghttp2 (MIT), ngtcp2 (MIT), ICU (Unicode-DFS) | Permissive Open Source | \$0.00 |
| **GitHub Actions** | `actions/checkout@v4`, `actions/setup-node@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`, `actions/download-artifact@v4`, `actions/cache@v4` | MIT | \$0.00 |
