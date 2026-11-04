# Node.js Benchmark Runner Verification & Alternate Infrastructure Cost Analysis

This document provides a technical verification of the `benchmark.yml` infrastructure entry and evaluates three viable alternative options: **GitHub Larger Runners (High-Spec)**, **On-Premises Physical Bare-Metal Servers**, and **AWS Compute & Bare-Metal Instances**.

---

## 1. Technical Verification of Current Entry

### The Provided Row
```text
Node.js 26.13.0 | Benchmark | benchmark.yml | Test | Yes | Shared physical/VM benchmark server | $500/mo x 12 = $6,000/yr | Preferred: Retain current | Alternate: NA
```

### Verification Findings & Observations
1. **Quality Gate vs. Security Gate**:
   - In upstream `nodejs/node`, `benchmark.yml` is **not a security gate** (security scanning is handled by `codeql.yml` and `deps/openssl` tests).
   - Nor is it an automated blocking gate on PRs (it is triggered via `workflow_dispatch`).
   - However, for an **enterprise customer fork**, classifying it as a **Mandatory Performance Quality Gate** is valid if the organization must validate that internal changes or upstream synchronizations do not cause throughput or latency regressions against SLAs.
2. **$6,000/Year Cost Ceiling**:
   - The figure of **$500/month ($6,000/year)** assumes a continuously provisioned, always-on dedicated server lease (24×7×365).
   - In practice, performance benchmarking is an **episodic task** executed prior to releases or after major upstream merges (~2 to 10 runs per month, taking ~30–45 minutes per run).
   - Paying $6,000/year for continuous idle compute can be drastically reduced by using on-demand/ephemeral compute or leveraging existing shared lab hardware.

---

## 2. Alternate Options Deep Dive & Cost Comparison

### Option 1: GitHub High-Spec (Larger) Runners
GitHub Actions provides managed, dedicated virtual machine runners for GitHub Enterprise accounts.

* **Specifications & Official GitHub Pricing (Linux x64 / ARM64)**:
  - **4-Core Linux (16 GB RAM)**: **$0.012 per minute** ($0.72/hour).
  - **8-Core Linux (32 GB RAM)**: **$0.022 per minute** ($1.32/hour).
  - **16-Core Linux (64 GB RAM)**: **$0.042 per minute** ($2.52/hour).
  - **8-Core ARM64 (32 GB RAM)**: **$0.014 per minute** ($0.84/hour).
* **Usage & Annual Cost Estimate**:
  - A typical Node.js benchmark suite run takes **~30 to 45 minutes**.
  - **Moderate Usage (2 runs/month = ~75 mins/month)**:
    - 8-Core Linux: 75 min × $0.022 = $1.65/month -> **$19.80 / year**
    - 16-Core Linux: 75 min × $0.042 = $3.15/month -> **$37.80 / year**
  - **Intensive Usage (10 runs/month = ~350 mins/month)**:
    - 8-Core Linux: 350 min × $0.022 = $7.70/month -> **$92.40 / year**
    - 16-Core Linux: 350 min × $0.042 = $14.70/month -> **$176.40 / year**
* **Technical Verdict**:
  - *Pros*: Zero infrastructure management; 100% cloud-managed; billed strictly per second; no idle costs.
  - *Cons*: Runs on Azure hypervisors (Dv5 series). Virtualization jitter is ~2–5%, requiring multiple iterations (`--runs 30`) to establish tight confidence intervals.

---

### Option 2: On-Premises Physical Server (Bare-Metal Self-Hosted Runner)
Connect an on-premises physical server to GitHub Actions as a self-hosted runner (`actions/runner`).

* **Specifications & Hardware Profile**:
  - 1U rack server or lab workstation: 16 to 32 physical cores (AMD EPYC or Intel Xeon), 64 GB ECC RAM, NVMe SSD.
  - Operating System: Ubuntu 24.04 LTS with CPU governor locked to `performance` mode (`cpupower frequency-set -g performance`) and hyperthreading tuned to eliminate jitter.
* **Cost Scenarios**:
  - **Scenario 2A: Standalone Dedicated Physical Server Purchase**:
    - **CapEx (Server purchase)**: ~$2,500 – $4,500 one-time purchase. Annualized over a 3-year lifespan = **$833 – $1,500 / year**.
    - **OpEx (Power, cooling, lab hosting)**: ~$50 – $100/month = **$600 – $1,200 / year**.
    - **Total Cost**: **~$1,433 – $2,700 / year**.
  - **Scenario 2B: Leveraging Existing Shared Physical Server (Recommended)**:
    - Sheet 3 of `infra_tool_estimate.xlsx` already accounts for a common 3P shared physical server (*"Proxmox VE host for K3s/GraalVM development and performance environments: $46,000 one-time, $15,333/year annualized"*).
    - Running Node.js benchmark jobs on a dedicated partition of this shared lab hardware requires **$0 additional CapEx**, costing **$0 to ~$300/year** in allocated maintenance.
* **Technical Verdict**:
  - *Pros*: **Gold standard for benchmarking**. True bare-metal execution with 0% virtualization jitter and access to native hardware performance counters (`perf`).
  - *Cons*: Requires on-prem lab space, network connectivity, power, and physical hardware maintenance.

---

### Option 3: AWS Server (Compute-Optimized vs. Bare-Metal EC2)
Run self-hosted GitHub Actions runners on Amazon Web Services (AWS).

* **Sub-Option 3A: Compute-Optimized Virtual Instances (`c6i.2xlarge` or `c7g.2xlarge`)**:
  - Specs: 8 vCPUs, 16 GiB RAM.
  - Hourly rates (us-east-1):
    - `c6i.2xlarge` (Intel Ice Lake): **$0.340 / hour**
    - `c7g.2xlarge` (AWS Graviton3 ARM64): **$0.290 / hour**
  - **Cost (Ephemeral / On-Demand)**:
    - Automatically spin up instance for benchmark run and terminate immediately after.
    - 2 runs/month × 1 hour = 2 hrs/month (24 hrs/year):
      - 24 hrs × $0.34/hr = **~$8.16 / year**
    - 10 runs/month (120 hrs/year):
      - 120 hrs × $0.34/hr = **~$40.80 / year**
  - **Cost (Always-On 24×7 Instance)**:
    - 730 hrs/month × $0.34/hr = **$248.20 / month = $2,978 / year** (or ~$1,500/yr on 1-year Savings Plan).

* **Sub-Option 3B: AWS Dedicated Bare-Metal Instances (`c6i.metal` or `c7g.metal`)**:
  - Specs: Dedicated physical silicon with NO hypervisor!
  - Hourly rates (us-east-1):
    - `c7g.metal` (64 vCPU, 128 GiB RAM): **$2.320 / hour**
    - `c6i.metal` (128 vCPU, 256 GiB RAM): **$5.440 / hour**
  - **Cost (Ephemeral / On-Demand Runner)**:
    - 2 runs/month × 1 hour = 24 hrs/year:
      - `c7g.metal`: 24 hrs × $2.32 = **$55.68 / year**
      - `c6i.metal`: 24 hrs × $5.44 = **$130.56 / year**
    - 10 runs/month × 1 hour = 120 hrs/year:
      - `c7g.metal`: 120 hrs × $2.32 = **$278.40 / year**
      - `c6i.metal`: 120 hrs × $5.44 = **$652.80 / year**
  - **Cost (Always-On 24×7 Bare Metal)**:
    - 730 hrs/month × $5.44/hr = **$3,971 / month = $47,654 / year** (Cost-prohibitive for idle compute; only use ephemeral).

---

## 3. Side-by-Side Comparison Matrix

| Option | Architecture | Performance Jitter | Pricing Model | Unit Cost | Annual Cost (2–10 runs/mo) | Management Overhead | Best Fit |
| :--- | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **Current Row Baseline** | Dedicated Server Lease | Low | Always-on monthly lease | $500/month | **$6,000 / yr** | Low (managed) | Overpriced for episodic usage |
| **1. GitHub Larger Runner** | Managed VM (Azure) | 2% – 5% | Pay-per-minute (GHA) | $0.022/min (8-core)<br>$0.042/min (16-core) | **$20 – $176 / yr** | **Zero** (100% GitHub-managed) | **Easiest & lowest effort** |
| **2A. On-Prem Physical (Dedicated)** | 1U Bare-Metal Server | **0% (Deterministic)** | CapEx + Lab OpEx | ~$3,000 purchase + $75/mo power | **$1,433 – $2,700 / yr** | High (hardware lifecycle) | Strict hardware control |
| **2B. On-Prem Physical (Shared)** | Partition on Shared Host | **0% (Deterministic)** | Shared common infra | Partition of existing server | **$0 – $300 / yr** | Medium (lab admin) | **Best performance/cost value** |
| **3A. AWS Ephemeral VM** | EC2 `c6i.2xlarge` | 2% – 5% | On-demand per-second | $0.340 / hour | **$8 – $41 / yr** | Low (Terraform/scripted) | Cheap cloud alternative |
| **3B. AWS Ephemeral Bare-Metal** | EC2 `c7g.metal` / `c6i.metal` | **0% (Deterministic)** | On-demand per-second | $2.32 – $5.44 / hour | **$56 – $653 / yr** | Low to Medium | **Zero-jitter cloud solution** |

---

## 4. Recommended Replacement Row for Presentation / Spreadsheet

```text
Node.js 26.13.0	Benchmark	benchmark.yml	"• What it does: Runs Node.js micro-benchmarks across HTTP, Buffer, Crypto, and Event Loop to detect performance and latency regressions before merge or release.
• Why it is mandatory: Required for enterprise release qualification to protect performance SLAs and customer compatibility."	Test	Yes	Managed Ephemeral / Shared Benchmark Runner	"• Current role: Executes comparative performance test harness (benchmark/compare.js).
• Significance: Protects enterprise runtime throughput and ensures upstream sync does not introduce performance regressions."	"• GitHub Larger Runner (8-core @ $0.022/min or 16-core @ $0.042/min): ~$20–$176/year.
• AWS Ephemeral Bare-Metal (c7g.metal @ $2.32/hr): ~$56–$278/year.
• On-Premises Shared Physical Server: ~$0–$300/year incremental.
• Price reference: https://docs.github.com/en/billing/concepts/product-billing/github-actions"	0	20–278	"• Use GitHub Larger Runners or Ephemeral AWS Bare-Metal for episodic runs.
• Avoid $6,000/yr always-on dedicated server."	https://docs.github.com/en/billing/concepts/product-billing/github-actions	"• Preferred option: GitHub Actions Larger Runner (8-core/16-core) for zero-management cloud runs.
• Alternate option 1: Ephemeral AWS Bare-Metal (c7g.metal) for zero-jitter deterministic benchmarking.
• Alternate option 2: Partition on existing on-premises shared physical server ($0 additional CapEx)."	GitHub 8-core / AWS c7g.metal / Shared On-Prem	"• AI-assisted: Configure workflow to target larger-runner label or ephemeral AWS runner trigger.
• Manual: Verify benchmark baseline reproducibility and compare confidence intervals."	0.5–1.0 person-days
```
