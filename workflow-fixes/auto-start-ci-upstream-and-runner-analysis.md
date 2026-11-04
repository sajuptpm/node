# Auto Start CI: Architecture, Upstream Operations & Runner Guide

## Executive Summary & Direct Q&A

| Question | Short Answer | Details / Section |
| :--- | :--- | :--- |
| **What does this pipeline do?** | Automated queue manager & test dispatcher | Scans approved, conflict-free PRs with label `request-ci`, checks Jenkins cluster capacity, and triggers broad cross-platform tests. (See [Section 1](#1-what-this-pipeline-does)) |
| **How does upstream run it?** | 5-minute cron on GitHub Actions | Dispatches to the OpenJS Jenkins cluster (`ci.nodejs.org`) via `@node-core/utils`. (See [Section 2](#2-how-upstream-operates--funds-it)) |
| **How much is upstream paying?** | **$0.00 / year** | Zero software subscriptions. Hardware and compute (AIX, z/OS, ARM, macOS, Windows) are 100% donated/sponsored. (See [Section 2.2](#22-in-kind-hardware--cloud-sponsorships)) |
| **Should I do any big modification for Local Jenkins?** | **NO** (Minimal changes: < 10 lines) | Change repo guard, add 2 GitHub secrets (`JENKINS_USER`, `JENKINS_TOKEN`), set `.ncurc.json` URL, and create 1 Jenkins job. (See [Section 3.1](#31-scenario-a-running-on-local-jenkins)) |
| **Should I do any big modification for Customer Self-Hosted Runners?** | **NO** (Even simpler: removes Jenkins) | Tag the runner `runs-on: [self-hosted, customer-lab]` and trigger native GitHub Actions tests on PR label. (See [Section 3.2](#32-scenario-b-running-on-customer-specific-self-hosted-runners)) |
| **What is the $1,200 in the planning table?** | Theoretical planning reserve | A $100/mo reserve *only* if rare enterprise mainframes (AIX cloud) are contractually demanded. For standard Linux/Win/macOS/ARM64, cost is **$0.00**. (See [Section 5](#5-explanation-of-the-1200-planning-table-entry)) |

---

## 1. What This Pipeline Does

The `auto-start-ci.yml` pipeline functions as an **automated queue controller and test dispatcher**. 

In high-volume open-source projects like Node.js (which receive dozens of PRs and hundreds of commits every week), executing full cross-platform builds and test suites on every single commit push would quickly overwhelm physical and cloud infrastructure. Instead, the project requires collaborator approval before triggering comprehensive testing.

```mermaid
sequenceDiagram
    autonumber
    actor Contributor as Developer / PR
    actor Reviewer as Node.js Collaborator
    participant GHA as GitHub Actions (auto-start-ci)
    participant Cluster as Jenkins / Runner Farm
    
    Contributor->>GHA: Opens Pull Request
    Reviewer->>GHA: Approves PR & adds label: "request-ci"
    loop Every 5 Minutes
        GHA->>GHA: Job 1: Query approved, mergeable PRs with "request-ci"
    end
    GHA->>Cluster: Check health & queue capacity (< 15 jobs)
    alt Capacity Available
        GHA->>GHA: Remove label "request-ci"
        GHA->>Cluster: Dispatch test jobs (Linux, Win, macOS, AIX, etc.)
        Cluster-->>GHA: Report Build Status
    else Capacity Full or Unhealthy
        GHA->>GHA: Keep "request-ci" label and retry on next 5-min cycle
    end
```

### Step-by-Step Technical Flow:
1. **Queue Inspection (`get-prs-for-ci`)**:
   - Runs every 5 minutes (`cron: 3/5 * * * *`) on a lightweight GitHub-hosted runner (`ubuntu-latest` / `ubuntu-slim`).
   - Uses the GitHub CLI (`gh pr list`) to query open pull requests matching:
     - State is approved (`review:approved`).
     - Labeled with `request-ci` or `resume-ci`.
     - Git merge status is conflict-free (`mergeable == "MERGEABLE"`).
   - Batches matching PR numbers (up to `AUTO_START_CI_BATCH_SIZE`, default 5).

2. **Cluster Health & Workload Throttling (`start-ci`)**:
   - For each matching PR, executes `tools/actions/start-ci.sh`.
   - Probes the build cluster via `@node-core/utils` (`ncu-ci available` and `ncu-ci workload`).
   - If the queue exceeds `MAX_WORKLOAD` (default 15 active jobs) or the cluster is offline, the workflow gracefully defers execution to the next cycle without modifying labels.

3. **Execution & State Management**:
   - Removes the `request-ci` / `resume-ci` label to prevent duplicate triggers.
   - Dispatches the test job (`ncu-ci run --check-for-duplicates "$pr"`).
   - If the trigger fails, applies `request-ci-failed` and automatically posts a formatted error log comment directly on the PR.

---

## 2. How Upstream Operates & Funds It

### 2.1 Zero Commercial Subscriptions
The upstream Node.js project and the OpenJS Foundation pay **$0.00** in commercial software subscriptions for this workflow:
- **GitHub Actions**: Standard runners are provided completely free with unlimited minutes for public open-source projects under GitHub's Open Source program.
- **Jenkins Controller & Software**: Uses the free, open-source Community Edition of Jenkins (no CloudBees or paid licenses).
- **Tooling**: `@node-core/utils` is an in-house open-source tool developed by Node.js maintainers.

### 2.2 In-Kind Hardware & Cloud Sponsorships
The upstream build farm ([`ci.nodejs.org`](https://ci.nodejs.org/)) tests esoteric enterprise platforms across hardware donated by foundation partners:

| Platform / Component | In-Kind Hardware Provider | Model | Upstream Cost |
| :--- | :--- | :--- | :--- |
| **Jenkins Master & Web Controllers** | **DigitalOcean** | Cloud Droplets / VMs | **$0.00** (Sponsored) |
| **IBM AIX & z/OS (s390x) Mainframes** | **IBM** | Dedicated LPARs & mainframes | **$0.00** (Donated) |
| **PowerPC (ppc64le)** | **IBM / Oregon State University (OSU OSL)** | Dedicated hardware | **$0.00** (Donated) |
| **ARM64 Servers** | **Arm & Equinix Metal (Packet)** | Bare-metal compute | **$0.00** (Donated) |
| **macOS Build Farm** | **MacStadium** | Dedicated Mac minis | **$0.00** (Donated) |
| **Windows VM Farm** | **Microsoft Azure** | Cloud compute credits | **$0.00** (Donated) |
| **Enterprise CDN & DDoS** | **Cloudflare** | Enterprise caching | **$0.00** (Donated) |

---

## 3. Runner Implementation Guide: Are Big Modifications Needed?

### Direct Answer: **NO big modifications are needed.**
You do **not** need to rewrite the architecture, redesign test scripts, or license expensive orchestration platforms. The core logic remains intact; you only adjust endpoint URLs and credentials.

---

### 3.1 Scenario A: Running on Local Jenkins

If your team wants to retain the exact upstream Jenkins workflow:

```mermaid
flowchart LR
    GHA["GitHub Actions (Fork)"] -->|".ncurc.json (jenkins_url)"| LocalJenkins["Local Jenkins (Docker/VM)<br/>- Job: node-test-pull-request"]
    LocalJenkins --> OnPremNodes["Local Test Nodes<br/>(Linux / Win / Mac)"]
```

#### What Modifications are Needed? (Very Small — < 10 lines)
1. **Remove Upstream Hardcoded Guard**:
   In `.github/workflows/auto-start-ci.yml`, change:
   ```yaml
   # BEFORE (Upstream only)
   if: github.repository == 'nodejs/node'

   # AFTER (Your Fork)
   if: github.repository == 'your-org/node' || github.event_name == 'workflow_dispatch'
   ```
2. **Configure Your Jenkins Endpoint**:
   Create or edit `.ncurc.json` in the root (or configure via environment variable):
   ```json
   {
     "jenkins_url": "https://jenkins.mycompany.internal"
   }
   ```
3. **Add Repository Secrets in GitHub**:
   - `JENKINS_USER`: Username of an account on your local Jenkins.
   - `JENKINS_TOKEN`: API token generated in Jenkins user settings.
4. **Create One Jenkins Job**:
   - In your local Jenkins, create a job named `node-test-pull-request`.
   - Configure it to take string parameter `PR_ID` and execute:
     ```bash
     ./configure
     make -j$(nproc) test
     ```
* **Effort Required**: ~1 to 2 hours of setup.
* **Software Cost**: **$0.00** (Jenkins Community Edition is 100% free and open-source).

---

### 3.2 Scenario B: Running on Customer-Specific Self-Hosted Runners

If you do not want to maintain a Jenkins server and prefer running directly on **customer-specific self-hosted physical machines or VMs**:

```mermaid
flowchart LR
    GHA["GitHub Actions (Fork)"] -->|"runs-on: [self-hosted, customer-lab]"| Runner["Customer-Specific Self-Hosted Runner<br/>(Physical Server / On-Prem VM)"]
    Runner --> Build["./configure && make -j$(nproc) test"]
```

#### What Modifications are Needed? (Simplification — removes Jenkins entirely)
Instead of dispatching to an external Jenkins API, the workflow dispatches directly to GitHub Actions runners tagged with customer-specific labels.

1. **Option 1: Native Label-Triggered Workflow (Recommended)**
   Add a GitHub Actions workflow `.github/workflows/test-customer-runners.yml`:
   ```yaml
   name: Customer Platform CI
   on:
     pull_request:
       types: [labeled, synchronize]

   jobs:
     test:
       if: contains(github.event.pull_request.labels.*.name, 'request-ci')
       runs-on: [self-hosted, customer-platform]
       steps:
         - uses: actions/checkout@v4
         - name: Build and Test
           run: |
             ./configure
             make -j$(nproc) test
   ```
2. **Option 2: Minimal Modification to `start-ci.sh`**
   If you want to keep the 5-minute queue polling logic in `auto-start-ci.yml`, modify only lines 60–70 in `tools/actions/start-ci.sh`:
   ```bash
   # Replace the ncu-ci Jenkins call with GitHub CLI dispatch:
   gh workflow run test-customer.yml --ref "$pr_branch"
   ```
* **Effort Required**: ~2 to 4 hours (mostly installing the GitHub runner service on the customer machine).
* **Software Cost**: **$0.00** (GitHub self-hosted runner daemon is free and open-source).

---

## 4. Comparison Table: Local Jenkins vs. Self-Hosted Runners

| Evaluation Metric | Option 1: Local Jenkins | Option 2: Self-Hosted GitHub Runners (Preferred) |
| :--- | :--- | :--- |
| **Big Modifications Needed?** | **No** (Set 2 secrets + Jenkins URL) | **No** (Tag runner `[self-hosted]`) |
| **Separate Master VM Needed?** | Yes (Requires Jenkins Master) | **None** (GitHub Actions coordinates everything) |
| **Maintenance Overhead** | Moderate (Maintain Jenkins server/plugins) | **Zero** (Runner auto-updates via GitHub daemon) |
| **Software Licensing Cost** | **$0.00** (Open Source) | **$0.00** (Included with GitHub) |
| **Platform Support** | Any OS (AIX, z/OS, Linux, Win, macOS) | Linux (x64/ARM), Windows, macOS |
| **Suitability for Enterprise Fork** | Best if customer requires esoteric mainframes (AIX) | **Best for standard Linux/Windows/ARM environments** |

---

## 5. Explanation of the $1,200 Planning Table Entry

In the infrastructure estimation table (`workflow-fixes/infra_tool_estimate.xlsx` / `Sheet1`):

| Column | Recorded Value | Engineering Meaning |
| :--- | :--- | :--- |
| **Pipeline** | `Auto Start CI` (`auto-start-ci.yml`) | Automated PR CI trigger |
| **Infra / Tool** | `OpenJS Jenkins Build Farm upstream` | Upstream build cluster |
| **Yearly Cost (Vendor Published)** | **`$0`** | Upstream pays $0; hardware is sponsored |
| **Yearly Cost (Requires Vendor Quote)** | **`$1,200`** | **Theoretical planning reserve** ($100/mo) in case an enterprise customer contractually demanded testing on proprietary cloud mainframes (e.g. IBM AIX cloud instances). |
| **Remarks** | *"remove if only standard Linux/Windows/ARM64 are supported."* | Explicitly instructs that if you only support standard platforms, delete this line ($0). |
| **Preferred Alternate Cost** | **`$0`** | Replaced by customer-specific self-hosted runners or GitHub Actions native runners. |

---

## 6. Conclusion & Recommendation for Downstream Enterprise Forks

1. **Upstream Reality**: Upstream Node.js pays **$0** for subscriptions because GitHub Actions provides free open-source runners and hardware partners donate all physical nodes.
2. **No Big Modifications**: Neither Local Jenkins nor Customer-Specific Self-Hosted Runners require architectural overhauls. 
3. **Best Practice Verdict**:
   - For standard Linux, Windows, macOS, and ARM64 releases: **Use Customer-Specific Self-Hosted GitHub Runners** or native GitHub Actions. This costs **$0.00**, eliminates the Jenkins maintenance burden, and requires under 2 hours of setup.
   - For legacy or mainframe support (AIX): **Use a local Docker Jenkins** container with `@node-core/utils` pointing to your internal URL ($0 software cost).
