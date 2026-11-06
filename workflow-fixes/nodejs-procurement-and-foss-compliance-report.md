# Node.js 26.13.0 CI/CD Infrastructure Assessment: Procurement (POs & Quotes) and FOSS Legal Compliance

## 1. Executive Summary

This document provides a comprehensive operational, financial, and legal compliance assessment for all **109 workflow tool instances** across the 45 GitHub Actions CI/CD workflows of Node.js 26.13.0. 

This assessment is recorded in the `nodejs` sheet of `workflow-fixes/data1.xlsx`, structured across all **44 columns** defined in the standardized `template` schema (matching the depth of `spring_boot` and `angular`).

The assessment serves two organizational objectives:
1. **Procurement & Finance List**: Generating Purchase Orders (POs), requesting formal vendor quotations, and budgeting for required tools, proprietary cloud runners, and infrastructure.
2. **Legal & Compliance List**: Providing our legal counsel with SPDX license identifiers, copyleft/viral source disclosure risks, commercial redistribution rights, and formal legal verdicts for permissible downstream fork distribution.

---

## 2. Dataset Schema & Metrics (`data1.xlsx` -> `nodejs` sheet)

- **Total Rows**: 110 (1 Header Row + 109 Data Rows corresponding to `master_list`).
- **Total Columns**: 44 (Standard schema).
- **Empty / Null Cells**: **0** across all 4,796 cells.
- **Upstream Original Tools**: 102 rows.
- **Recommended Fork Alternates**: 7 rows (mapped directly to upstream original tools).

### Schema Column Mapping (Columns 1 – 44)
1. `Name of Tool/Infra`
2. `Version`
3. `Purpose`
4. `Record Type (Upstream Original Tool / Recommended Fork Alternate)`
5. `Alternate of which too/infra (Mapping to Upstream Original Tool /infra)`
6. `Reason of selecting this tool`
7. `Any usage Limit`
8. `Free/Paid`
9. `Access-restricted, blocked, not publicly accessible, or unavailable for purchase`
10. `License`
11. `SPDX License Identifier`
12. `Copyleft / Viral Source Disclosure Risk`
13. `Commercial Redistribution Rights`
14. `Telemetry & Code Exfiltration Risk`
15. `Attribution / Notice Requirements`
16. `Permissible for Company Fork Release? (Legal Verdict)`
17. `Subscription Models Vailable`
18. `Selected Subscription Model`
19. `Reason of selecting this subscription model`
20. `Category`
21. `Component Name`
22. `workflow name`
23. `workflow yml`
24. `User Limit`
25. `User / Concurrency / Usage Limits`
26. `Token/Key/Secret Based access`
27. `License Suitable for 5 member team and reason`
28. `Subscription Suitable for 5 member team and reason`
29. `Required to Purchase ?`
30. `Why Upstream Uses It`
31. `Access Status in Fork`
32. `Is It Mandatory in Fork? (Yes / No - Can be discarded)`
33. `Suitable for Release from Fork? (Yes/No + Reason)`
34. `Official site`
35. `Purchase Link`
36. `Price Link`
37. `Is it suitable for release from Forked Opensource Model ? Reason`
38. `why it not suitable for release from Forked Opensource Model`
39. `Alternate Options for release from Forked Opensource Model`
40. `Best One alternate Option for release from Forked Opensource Model (with name and version)`
41. `Reason of selecting that Best One alternate Option for release from Forked Opensource Model`
42. `Replaces Upstream Tool (Name of original tool if this is an alternate)`
43. `issues identified in master_list`
44. `List of all evidence verified`

---

## 3. List 1: Purchase Orders (POs) & Vendor Quotes List

> **Excel Filter Strategy**:
> - Filter Column 29 (`Required to Purchase ?`) for text starting with `"Yes"` OR
> - Filter Column 8 (`Free/Paid`) for text containing `"Paid"` OR
> - Filter Column 9 (`Access-restricted...`) for text starting with `"Yes"`.

This list encompasses all proprietary tools, upstream-restricted hardware, cloud storage buckets, and commercial SaaS integrations.

### Comprehensive Procurement Analysis Table

| Tool / Infrastructure | Workflows Affected | Upstream Access Status | Commercial Pricing / Quote Basis | Purchase Order / Quote Requirement | Recommended $0 Alternate for Downstream Fork | Alternate Annual Cost | Development Effort |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shared physical/VM benchmark server** | `benchmark.yml` | **Restricted / Blocked** (Upstream dedicated physical bench host) | Bare-metal server rental: **$250 – $500/month = $3,000 – $6,000/year** | **PO / Vendor Quote Required** if dedicated hardware is mandated to eliminate noisy-neighbor variance. | On-demand GitHub Larger Runner (c7i-equivalent 16-core at $0.0056/min, ~$40.32/yr) or local developer execution. | **$0.00 – $40.32/yr** | 1–2 person-days |
| **OpenJS Jenkins Build Farm upstream** | `auto-start-ci.yml`, `commit-queue.yml` | **Restricted / Blocked** (Requires private `ci.nodejs.org` `JENKINS_TOKEN`) | Proprietary mainframe cloud access (IBM AIX, z/OS s390x): Planning reserve **$100/mo x 12 = $1,200/year** | **Vendor Quote Required** *only* if customer contractually demands testing on rare mainframe architectures. | Native GitHub Actions Runners (`ubuntu-latest`, `windows-latest`, `macos-latest`, `ubuntu-24.04-arm`) for standard releases. | **$0.00/yr** | 15–30 person-days |
| **bot collaborator upstream** | `create-release-proposal.yml`, `find-inactive-collaborators.yml`, `find-inactive-tsc.yml`, `lint-release-proposal.yml`, `major-release.yml` | **Restricted / Blocked** (Requires upstream bot triage credentials / PAT) | GitHub Enterprise committer seat: **$21/user/month = $252/year** | **PO Required** if company compliance mandates billing bot automation as a dedicated committer seat. | GitHub App short-lived installation tokens (`GITHUB_TOKEN` or custom GitHub App) requiring zero paid committer seats. | **$0.00/yr** | 1–2 person-days |
| **sccache object storage** | `build-tarball.yml`, `coverage-linux.yml`, `coverage-linux-without-intl.yml`, `test-linux.yml` | **Accessible** (Requires AWS S3 / Cloud Storage bucket) | AWS S3 Standard Storage + Data Egress: **~$10/month = $120/year** | **Cloud PO Required** if enterprise policy mandates an external dedicated AWS S3 bucket. | GitHub Actions native cache backend (`Mozilla-Actions/sccache-action` with `actions/cache` 10 GB quota). | **$0.00/yr** | 0.5 person-days |
| **Cachix Nix binary cache** | `nix-changes.yml`, `nix-changes-comment.yml` | **Accessible** (Free OSS tier upstream) | Cachix Team Plan: **$200/month = $2,400/year** ceiling | **Vendor Quote Required** *only* if private proprietary Nix caching exceeding 5 GB storage is needed. | Standard Free Cachix OSS tier (5 GB storage + unlimited bandwidth) or GitHub native `actions/cache`. | **$0.00/yr** | 0.5 person-days |
| **Slack upstream** | `post-release.yml`, `notify-on-push.yml`, `notify-on-review-wanted.yml` | **Restricted / Blocked** (Confidential upstream webhook URLs) | Slack Business+ / Pro: **$8.70 – $15/user/month = $104.40 – $180/user/year** | **PO Required** *only* if establishing an isolated corporate Slack workspace for release alerts. | Microsoft Teams Incoming Webhook or Corporate SMTP Mail using existing enterprise Microsoft 365 / Google Workspace. | **$0.00/yr** | 0.5 person-days |
| **Codecov** | `coverage-windows.yml`, `test-internet.yml` | **Accessible** (Free for public repos; paid for private repos) | Codecov Pro: **$10 – $12/user/month = $120 – $144/user/year** | **PO Required** *only* if the downstream fork is maintained as a private repository. | Native `lcov` / `c8` HTML coverage reports uploaded directly as GitHub Actions workflow artifacts. | **$0.00/yr** | 1–2 person-days |
| **OpenJS ubuntu-slim upstream** | 33 core workflows (`test-linux.yml`, `build-shared.md`, etc.) | **Restricted / Blocked** (Custom runner label restricted to `nodejs/node`) | **Cannot be purchased**: Internal OpenJS Foundation private fleet. | **N/A (Not for Sale)**: Commercial purchase is impossible; must be remapped. | Remap runner label from `ubuntu-slim` to standard hosted runner `ubuntu-latest` / `ubuntu-24.04`. | **$0.00/yr** | 0.5 person-days |

---

## 4. List 2: Free & Open-Source Tools for Legal Compliance

> **Excel Filter Strategy**:
> - Filter Column 8 (`Free/Paid`) for text containing `"Free"`.

This list enables corporate legal counsel to audit license permissiveness, copyleft obligations, viral source disclosure risks, code telemetry/exfiltration, and commercial redistribution rights.

### Legal Compliance & Licensing Audit Table

| Tool / Component | Governing License | SPDX Identifier | Copyleft / Viral Disclosure Risk | Commercial Redistribution Rights | Telemetry & Code Exfiltration Risk | Attribution & Notice Requirements | Legal Verdict for Downstream Release |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GitHub Actions Hosted Runner** (`ubuntu-latest`, `ubuntu-slim` alternate) | GitHub Terms of Service | `Terms of Service` | **None / Permissive** | **Permitted** | **Local-only** (Ephemeral Azure VM; destroyed after job completion) | None | **Permissible** (Standard cloud compute infrastructure) |
| **OpenSSF Scorecard** | Apache License 2.0 | `Apache-2.0` | **None / Permissive** | **Permitted** | **Low** (Audits public repo security posture; read-only) | Standard notice | **Permissible** (Free supply-chain security audit tool) |
| **StepSecurity Harden-Runner Community** | Apache License 2.0 | `Apache-2.0` | **None / Permissive** | **Permitted** | **Low** (Agent runs locally within runner; audits outbound socket calls) | Standard notice | **Permissible** (Defensive runtime security monitor) |
| **AgentScan upstream** | MIT License | `MIT` | **None / Permissive** | **Permitted** | **Local-only** (PR automated triage script) | Standard notice | **Permissible** (Permissive utility script) |
| **wpt.fyi service** | BSD 3-Clause / Public API | `BSD-3-Clause` | **None / Permissive** | **Permitted** | **Cloud SaaS logs** (Uploads test result JSON to public dashboard) | Standard notice | **Restricted in Fork** (Upstream publishing disabled; run tests locally) |
| **sccache** | Apache License 2.0 | `Apache-2.0` | **None / Permissive** | **Permitted** | **Local-only / S3** (Compiler cache object storage) | Standard notice | **Permissible** (Permissive build accelerator) |
| **managed ARM64 runner** (`ubuntu-24.04-arm`) | GitHub Terms of Service | `Terms of Service` | **None / Permissive** | **Permitted** | **Local-only** (Ephemeral ARM64 VM) | None | **Permissible** (Free hosted compute for open-source repos) |
| **Standard Windows runner** (`windows-2025`) | GitHub Terms of Service | `Terms of Service` | **None / Permissive** | **Permitted** | **Local-only** (Ephemeral Windows Server VM) | None | **Permissible** (Free hosted compute for open-source repos) |
| **customer-specific special-platform runners** | MIT License (Runner Daemon) | `MIT` | **None / Permissive** | **Permitted** | **Local-only** (Runs on customer/organization hardware) | Standard notice | **Permissible** (Self-hosted runner daemon) |
| **Teams/email replacement** | Commercial Enterprise SaaS | `Commercial SaaS EULA` | **None** | **Permitted** | **Local-only / Corporate Tenant** (Internal notifications) | None | **Permissible** (Standard enterprise communication) |
| **Cachix Nix binary cache** (Client) | Apache License 2.0 | `Apache-2.0` | **None / Permissive** | **Permitted** | **Low** (Binary artifact cache) | Standard notice | **Permissible** (Permissive client utility) |

---

## 5. Verification Scripts and Reproducibility

The data in `workflow-fixes/data1.xlsx` was generated and validated by two scripts located in the repository:

1. **Populator Script** (`workflow-fixes/scripts/populate_nodejs_sheet.py`):
   - Extracts all 109 Node.js rows from `master_list`.
   - Populates all 44 columns according to the strict `template` schema.
   - Embeds concrete empirical evidence (workflow line numbers, pricing URLs, license terms).
2. **Verification Script** (`workflow-fixes/scripts/verify_nodejs_sheet.py`):
   - Confirms dimensions: 110 rows × 44 columns.
   - Verifies **0** empty or missing cells.
   - Audits all 21 distinct tool categories across List 1 (PO/Quote items) and List 2 (FOSS Legal Compliance items).

---

## 6. Official Pricing & Reference Documentation

- **GitHub Actions Runner & Seat Pricing**: [https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)
- **AWS EC2 Dedicated Bare-Metal & Larger Compute**: [https://aws.amazon.com/ec2/pricing/on-demand/](https://aws.amazon.com/ec2/pricing/on-demand/)
- **AWS S3 Object Storage Pricing**: [https://aws.amazon.com/s3/pricing/](https://aws.amazon.com/s3/pricing/)
- **Cachix Pricing**: [https://www.cachix.org/pricing](https://www.cachix.org/pricing)
- **Codecov Pricing**: [https://about.codecov.io/pricing/](https://about.codecov.io/pricing/)
- **Slack Enterprise Pricing**: [https://slack.com/pricing](https://slack.com/pricing)
- **Node.js Build Working Group & Jenkins Infrastructure**: [https://github.com/nodejs/build](https://github.com/nodejs/build)
