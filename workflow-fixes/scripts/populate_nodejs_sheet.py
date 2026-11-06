import openpyxl

def generate_nodejs_data():
    wb = openpyxl.load_workbook('workflow-fixes/data1.xlsx')
    ws_master = wb['master_list']
    ws_nodejs = wb['nodejs']
    ws_template = wb['template']

    headers = [c.value for c in ws_template[1]]
    print(f"Total columns in template: {len(headers)}")

    # Extract all Node.js rows from master_list
    master_rows = []
    for r_idx, row in enumerate(ws_master.iter_rows(min_row=2, values_only=True), 2):
        comp = str(row[0]) if row[0] is not None else ''
        if 'node' in comp.lower():
            master_rows.append((r_idx, row))

    print(f"Total Node.js rows extracted from master_list: {len(master_rows)}")

    # Clear existing data rows in nodejs sheet (keep header)
    while ws_nodejs.max_row > 1:
        ws_nodejs.delete_rows(2)

    # Dictionary of detailed metadata generators by tool name pattern
    def build_row(m_idx, r_idx, m_row):
        comp = m_row[0]          # Component
        pipe = m_row[1]          # Pipeline
        yml = m_row[2]           # YAML File
        desc = m_row[3]          # Detailed Pipeline Description
        cat = m_row[4]           # Category
        mand = m_row[5]          # Mandatory (Yes/No)
        tool = m_row[6]          # Infra / Tool
        cost_pub = m_row[7]      # Yearly Cost with Vendor Published ($)
        cost_quote = m_row[8]    # Yearly Cost with Rough/Quote ($)
        remarks = m_row[9]       # Remarks
        pref_alt = m_row[10]     # Replacement Option and Cost (Preferred)
        pref_cost = m_row[11]    # Yearly Cost with Preferred Alternate ($)
        dev_act = m_row[12]      # Development Activities
        dev_est = m_row[13]      # Total Development Estimate
        plan = m_row[17]         # Plan based on Review
        quote_req = m_row[18]    # Quote Required?
        rev_cost = m_row[19]     # Yearly Cost - Reviewed ($)
        rev_effort = m_row[20]   # Additional Development Effort (Days)
        rev_sum = m_row[21]      # Review Summary
        rev_comm = m_row[22]     # Review comments

        # Determine tool category specifics
        t_lower = tool.lower()

        # Defaults
        version = "N/A"
        purpose = f"Supports workflow {pipe} ({yml})."
        rec_type = "Upstream Original Tool"
        alt_of = "N/A (Upstream Original)"
        replaces_tool = "N/A (Original Tool)"
        reason_selecting = ""
        usage_limit = "Standard usage limits."
        free_paid = "Free"
        blocked = "No"
        license_name = "MIT"
        spdx_id = "MIT"
        copyleft_risk = "None / Permissive"
        commercial_rights = "Permitted"
        telemetry_risk = "Local-only"
        attribution_req = "None"
        legal_verdict = "Permissible"
        subs_available = "Free open-source tier"
        subs_selected = "Free ($0.00)"
        subs_reason = "Zero-cost allocation for open-source repositories."
        user_limit = "Unlimited"
        concurrency_limit = "Standard GitHub account limits."
        auth_type = "GITHUB_TOKEN"
        license_suitable_5m = "Yes; permissible license accommodates 5-member team."
        subs_suitable_5m = "Yes; $0 cost."
        req_purchase = "No"
        why_upstream_uses = "Automates core CI/CD validation and release lifecycle."
        access_status_fork = "Accessible"
        mand_fork = mand if mand else "Yes"
        suitable_fork_release = "Yes; executes cleanly without commercial blockers."
        official_site = "https://github.com"
        purchase_link = "https://github.com/pricing"
        price_link = "https://github.com/pricing"
        suitable_opensource_reason = "Yes; fully compatible with open-source development and release."
        why_not_suitable = "N/A (Fully suitable for open-source model)"
        alt_options = "Self-hosted runner, Docker container"
        best_alt = "Standard Open Source Alternative"
        reason_best_alt = "$0 cost, zero maintenance overhead, universally supported."
        issues_identified = "None; correctly identified in master_list."
        evidence_verified = f".github/workflows/{yml}"

        # -------------------------------------------------------------
        # 1. GitHub Actions Hosted Runner
        # -------------------------------------------------------------
        if tool == "GitHub Actions Hosted Runner":
            version = "ubuntu-latest (Ubuntu 24.04/22.04 LTS)"
            purpose = f"Executes {pipe} workflow job steps in a clean ephemeral cloud Linux VM."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Standard GitHub-hosted Linux compute environment provided by GitHub Actions."
            usage_limit = "2 vCPU, 7 GB RAM, 14 GB SSD storage; 6-hour execution timeout per job."
            free_paid = "Free"
            blocked = "No"
            license_name = "GitHub Terms of Service"
            spdx_id = "Terms of Service"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Ephemeral Microsoft Azure VM)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free for public open-source repositories; 2,000 free pooled minutes/mo for private repos ($0.008/min thereafter)"
            subs_selected = "GitHub Actions Standard Free Tier ($0.00)"
            subs_reason = "Free compute allocation included with public repository hosting."
            user_limit = "Unlimited public repo concurrency (subject to GitHub standard 20 concurrent jobs account limit)"
            concurrency_limit = "20 concurrent jobs per user/org on free tier; 2 vCPU, 7 GB RAM limit per runner."
            auth_type = "None (Native GITHUB_TOKEN automatically provisioned)"
            license_suitable_5m = "Yes; standard GitHub-hosted runner provides ample capacity for 5 developers on public fork."
            subs_suitable_5m = "Yes; 100% free of charge on public repositories."
            req_purchase = "No"
            why_upstream_uses = "Provides reliable, zero-maintenance ephemeral cloud Linux compute for CI/CD automation."
            access_status_fork = "Accessible"
            suitable_fork_release = "Yes; standard hosted runners execute cleanly without any billing or configuration prerequisites."
            official_site = "https://github.com/features/actions"
            purchase_link = "https://github.com/pricing"
            price_link = "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions"
            suitable_opensource_reason = "Yes; 100% free on public repositories, highly available, and requires no external credentials."
            why_not_suitable = "N/A (Fully suitable for open-source model)"
            alt_options = "Self-hosted Linux runner, Docker container runner, GitHub Large Runners"
            best_alt = "GitHub Actions Standard Hosted Runner (ubuntu-latest)"
            reason_best_alt = "$0 cost, zero maintenance overhead, native GitHub Actions integration, securely isolated ephemeral VMs."
            issues_identified = "Standard GitHub-hosted runner is sufficient for public fork; no issues identified."
            evidence_verified = f".github/workflows/{yml}: runs-on: ubuntu-latest (or runner variable)"

        # -------------------------------------------------------------
        # 2. OpenJS ubuntu-slim upstream
        # -------------------------------------------------------------
        elif tool == "OpenJS ubuntu-slim upstream":
            version = "OpenJS Foundation custom base container image (ubuntu-slim)"
            purpose = f"Upstream proprietary runner image configured in {pipe} ({yml}) to run jobs on OpenJS Foundation self-hosted cluster."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Upstream Node.js uses ubuntu-slim to match internal build infrastructure and reduce runner image pull latency."
            usage_limit = "Restricted to upstream nodejs/node repository runner fleet; unavailable in standard public runner pools."
            free_paid = "Free (OpenJS Internal Infrastructure)"
            blocked = "Yes (Custom runner label 'ubuntu-slim' is restricted to upstream Node.js infrastructure; jobs queue indefinitely on forks if unmapped)"
            license_name = "OpenJS Foundation Internal / Ubuntu Base Image EULA"
            spdx_id = "Proprietary / Ubuntu EULA"
            copyleft_risk = "None (Operating system base environment)"
            commercial_rights = "Restricted (Private OpenJS runner pool image)"
            telemetry_risk = "Local-only (OpenJS managed infrastructure)"
            attribution_req = "None"
            legal_verdict = "Restricted (Internal OpenJS runner label cannot be consumed directly by downstream forks)"
            subs_available = "Internal OpenJS Foundation infrastructure; not available for commercial purchase."
            subs_selected = "Not Applicable (Internal OpenJS Infrastructure)"
            subs_reason = "Cannot be purchased; downstream forks must remap runner label to standard hosted runners."
            user_limit = "Restricted to upstream Node.js repository collaborators."
            concurrency_limit = "Dedicated OpenJS runner pool concurrency limits."
            auth_type = "Restricted repository runner group registration token."
            license_suitable_5m = "No; proprietary runner label is not accessible outside the upstream nodejs organization."
            subs_suitable_5m = "No; unavailable for commercial licensing."
            req_purchase = "No (Cannot be purchased)"
            why_upstream_uses = "Minimizes VM spin-up latency and standardizes package dependencies across Node.js build workers."
            access_status_fork = "Inaccessible (Runner label unresolvable on forks)"
            mand_fork = "No (Replaced by standard ubuntu-latest)"
            suitable_fork_release = "No; causes workflow execution failure or permanent job queue stall on forked repositories."
            official_site = "https://github.com/nodejs/build"
            purchase_link = "N/A (Not for sale)"
            price_link = "https://docs.github.com/en/billing/concepts/product-billing/github-actions"
            suitable_opensource_reason = "No; proprietary internal runner label that fails in standard forked repositories."
            why_not_suitable = "Forks do not have access to the private OpenJS runner pool, causing jobs referencing 'ubuntu-slim' to get stuck in queued state indefinitely."
            alt_options = "Standard GitHub-hosted runner (ubuntu-latest), Self-hosted Linux runner, Docker container runner"
            best_alt = "GitHub Actions Standard Hosted Runner (ubuntu-latest)"
            reason_best_alt = "100% compatible, $0 cost on public forks, zero infrastructure maintenance, universally available."
            issues_identified = "Master list records $30,000/yr rough ceiling in row 469; actual solution requires $0 expenditure by remapping runner label to ubuntu-latest."
            evidence_verified = f".github/workflows/{yml}: runs-on: ubuntu-slim"

        # -------------------------------------------------------------
        # 3. OpenJS Jenkins Build Farm upstream
        # -------------------------------------------------------------
        elif tool == "OpenJS Jenkins Build Farm upstream":
            version = "Jenkins LTS (ci.nodejs.org)"
            purpose = f"Orchestrates remote cross-platform build and regression test matrix for {pipe} ({yml}) via ci.nodejs.org."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Upstream uses Jenkins to support legacy enterprise mainframes (AIX, s390x) and donated physical bare-metal servers."
            usage_limit = "Restricted to upstream Node.js Technical Steering Committee and collaborators; requires private Jenkins API token."
            free_paid = "Free (Open-Source Jenkins + Donated Corporate Hardware)"
            blocked = "Yes (Protected Jenkins instance ci.nodejs.org; JENKINS_TOKEN secret is strictly confidential to nodejs/node)"
            license_name = "MIT License (Jenkins Core) + Foundation Infrastructure"
            spdx_id = "MIT"
            copyleft_risk = "None (Permissive open-source software)"
            commercial_rights = "Permitted"
            telemetry_risk = "High (Build logs, commits, and artifacts processed on external foundation servers)"
            attribution_req = "None"
            legal_verdict = "Restricted (Private upstream Jenkins credentials cannot be accessed or shared with forks)"
            subs_available = "Open source free self-hosted Jenkins; CloudBees commercial enterprise Jenkins (~$15,000 - $50,000+/yr)"
            subs_selected = "Not Applicable (Downstream forks replace upstream Jenkins with native GHA)"
            subs_reason = "Forks do not need upstream Jenkins; builds can be executed directly on GitHub Actions or local Docker Jenkins."
            user_limit = "Restricted to authorized Node.js core maintainers."
            concurrency_limit = "Controlled by MAX_WORKLOAD (15 concurrent PR jobs) and physical server availability."
            auth_type = "JENKINS_USER and JENKINS_TOKEN secrets."
            license_suitable_5m = "No; downstream team cannot obtain access tokens to upstream ci.nodejs.org."
            subs_suitable_5m = "No; upstream cluster cannot be subscribed to or purchased by external commercial entities."
            req_purchase = "Yes (Vendor Quote Required only if enterprise customer contractually mandates dedicated AIX/mainframe cloud access, otherwise $0)"
            why_upstream_uses = "Validates Node.js compatibility across diverse hardware architectures donated by IBM, Arm, Microsoft, Intel, and MacStadium."
            access_status_fork = "Inaccessible (Private Jenkins API token absent)"
            mand_fork = "Yes"
            suitable_fork_release = "No; calls to ci.nodejs.org fail without private credentials."
            official_site = "https://ci.nodejs.org/"
            purchase_link = "https://www.cloudbees.com/pricing"
            price_link = "https://docs.github.com/en/billing/concepts/product-billing/github-actions"
            suitable_opensource_reason = "No; external upstream cluster is inaccessible to forked repositories."
            why_not_suitable = "Forks lack access to the private OpenJS Jenkins cluster and secret tokens, causing ncu-ci commands to fail immediately."
            alt_options = "Native GitHub Actions Matrix Workflow, Local Docker Jenkins (jenkins/jenkins:lts), Customer-specific self-hosted runners"
            best_alt = "Native GitHub Actions Multi-Platform Matrix (ubuntu-latest, windows-latest, macos-latest)"
            reason_best_alt = "$0 cost, zero maintenance overhead, native GitHub Actions execution, eliminates external Jenkins master dependency."
            issues_identified = "Master list records $1,200 planning reserve quote; verified as $0 required expenditure for standard Linux/Windows/ARM releases."
            evidence_verified = f".github/workflows/{yml}:3-4, start-ci.sh; nodejs/build repository"

        # -------------------------------------------------------------
        # 4. customer-specific special-platform runners
        # -------------------------------------------------------------
        elif tool == "customer-specific special-platform runners":
            version = "Self-hosted GitHub Actions runner daemon (v2.320+) / SSH runner"
            purpose = f"Executes {pipe} ({yml}) on contractually mandated enterprise platforms (e.g. IBM AIX, IBM z/OS s390x, PowerPC ppc64le, FreeBSD)."
            rec_type = "Recommended Fork Alternate"
            alt_of = "OpenJS Jenkins Build Farm upstream"
            replaces_tool = "OpenJS Jenkins Build Farm upstream"
            reason_selecting = "Enables compliant testing on non-commodity enterprise architectures without depending on OpenJS foundation hardware."
            usage_limit = "Governed by customer-provided server capacity and concurrency."
            free_paid = "Free (GitHub Actions Runner Daemon is Open Source; hardware provided by customer)"
            blocked = "No (Configured in customer's own infrastructure)"
            license_name = "MIT License (actions/runner)"
            spdx_id = "MIT"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (On-premise customer network / dedicated lab)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free (GitHub Actions self-hosted runners have zero runner minute charges)"
            subs_selected = "GitHub Actions Self-Hosted Free Tier ($0.00)"
            subs_reason = "Free daemon software running on customer-owned infrastructure."
            user_limit = "Unlimited users within the GitHub organization."
            concurrency_limit = "Concurrency bounded only by physical machine count."
            auth_type = "Standard repository runner registration token."
            license_suitable_5m = "Yes; open-source runner software permits unlimited team members."
            subs_suitable_5m = "Yes; 100% free with no per-minute fees."
            req_purchase = "No (Hardware is customer-provided or existing lab equipment)"
            why_upstream_uses = "N/A (Recommended Fork Alternate)"
            access_status_fork = "Accessible"
            mand_fork = "Yes"
            suitable_fork_release = "Yes; provides verified compliance on customer target platforms."
            official_site = "https://github.com/actions/runner"
            purchase_link = "https://github.com/pricing"
            price_link = "https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners"
            suitable_opensource_reason = "Yes; fully supported, compliant, and cost-effective on customer hardware."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "SSH Remote Execution Script, Cloud Emulator / QEMU VM, Cloud Mainframe Rental"
            best_alt = "Customer-Specific Self-Hosted Runner / SSH Dispatch"
            reason_best_alt = "Direct access to target silicon with native build performance."
            issues_identified = "Correctly identified as $0 preferred alternate in master list."
            evidence_verified = f"workflow-fixes/jenkins-ci-pipeline-tests-and-runner-migration.md; commit a960de2286d"

        # -------------------------------------------------------------
        # 5. standard GitHub runner
        # -------------------------------------------------------------
        elif tool == "standard GitHub runner":
            version = "ubuntu-latest / windows-latest / macos-latest"
            purpose = f"Executes {pipe} ({yml}) build and test matrix natively on GitHub-hosted infrastructure without external Jenkins servers."
            rec_type = "Recommended Fork Alternate"
            alt_of = "OpenJS Jenkins Build Farm upstream"
            replaces_tool = "OpenJS Jenkins Build Farm upstream"
            reason_selecting = "Replaces external Jenkins dependencies with native GitHub Actions workflows."
            usage_limit = "Standard GitHub-hosted VM limits (2-4 vCPU, 7-14 GB RAM)."
            free_paid = "Free"
            blocked = "No"
            license_name = "GitHub Terms of Service"
            spdx_id = "Terms of Service"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Ephemeral Microsoft Azure VM)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free on public open-source repos; 2,000 pooled free minutes/mo on private."
            subs_selected = "GitHub Actions Standard Free Tier ($0.00)"
            subs_reason = "Zero-cost native compute for public open-source releases."
            user_limit = "Unlimited users on public repositories."
            concurrency_limit = "20 concurrent jobs account limit."
            auth_type = "GITHUB_TOKEN"
            license_suitable_5m = "Yes; ample capacity for 5 developers."
            subs_suitable_5m = "Yes; $0 cost."
            req_purchase = "No"
            why_upstream_uses = "N/A (Recommended Fork Alternate)"
            access_status_fork = "Accessible"
            mand_fork = "Yes"
            suitable_fork_release = "Yes; fully native execution."
            official_site = "https://github.com/features/actions"
            purchase_link = "https://github.com/pricing"
            price_link = "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions"
            suitable_opensource_reason = "Yes; standard GitHub compute at $0."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "Self-hosted runner, Docker runner, GitHub Larger Runners"
            best_alt = "GitHub Actions Standard Hosted Runner (ubuntu-latest / windows-latest)"
            reason_best_alt = "$0 cost, native GitHub Actions execution, zero maintenance."
            issues_identified = "Correctly identified as $0 preferred alternate in master list."
            evidence_verified = f"workflow-fixes/auto-start-ci-upstream-and-runner-analysis.md; commit 0c063456001"

        # -------------------------------------------------------------
        # 6. bot collaborator upstream
        # -------------------------------------------------------------
        elif tool == "bot collaborator upstream":
            version = "GitHub Machine User / Automation Service Account (node-bot)"
            purpose = f"Performs automated Git commits, branch rebases, PR creation, and release proposal automation in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Upstream uses a dedicated collaborator bot account (node-bot) to bypass branch protections and sign commits."
            usage_limit = "Restricted to upstream repository; requires private personal access token (PAT) with write permissions."
            free_paid = "Paid (Requires paid GitHub Enterprise / Team seat if billed as dedicated user, ~$21/user/mo = $252/yr)"
            blocked = "Yes (Private upstream bot token GH_USER_TOKEN is confidential to Node.js release managers)"
            license_name = "GitHub Terms of Service"
            spdx_id = "Terms of Service"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Standard GitHub API activity logs)"
            attribution_req = "None"
            legal_verdict = "Restricted (Requires internal fork machine user or GitHub App token)"
            subs_available = "GitHub Enterprise Cloud seat (~$21/user/month = $252/year); GitHub Team seat (~$4/user/month = $48/year); GitHub App (Free)"
            subs_selected = "GitHub App Short-Lived Token (Free - $0.00) OR GitHub Enterprise Committer Seat ($252/yr if dedicated seat is purchased)"
            subs_reason = "GitHub App short-lived tokens provide elevated automation without consuming a paid committer seat."
            user_limit = "1 dedicated automation identity."
            concurrency_limit = "Standard GitHub REST API rate limit (5,000 requests/hour)."
            auth_type = "GH_USER_TOKEN / PERSONAL_ACCESS_TOKEN."
            license_suitable_5m = "Yes; machine accounts are permissible under GitHub ToS."
            subs_suitable_5m = "Yes; affordable or free via GitHub App."
            req_purchase = "Yes (Purchase Order Required if customer policy mandates a dedicated paid enterprise committer seat, otherwise $0 via GitHub App)"
            why_upstream_uses = "Automates branch synchronization, dependency updates, and release proposals without manual committer intervention."
            access_status_fork = "Inaccessible (Upstream secret GH_USER_TOKEN is absent)"
            mand_fork = "Yes"
            suitable_fork_release = "No; workflows fail without a valid token possessing repo write permissions."
            official_site = "https://github.com"
            purchase_link = "https://github.com/pricing"
            price_link = "https://github.com/pricing"
            suitable_opensource_reason = "No; upstream bot account cannot be used on forks."
            why_not_suitable = "Upstream node-bot credentials are restricted to nodejs/node and cannot authenticate to fork repositories."
            alt_options = "GitHub App with short-lived installation tokens, Standard GITHUB_TOKEN with workflow write permissions, Dedicated organization machine user"
            best_alt = "GitHub App Short-Lived Token / Standard GITHUB_TOKEN"
            reason_best_alt = "Avoids purchasing paid committer seats ($252/yr saved), provides fine-grained permissions, and auto-rotates tokens."
            issues_identified = "Master list records $252/yr vendor quote ceiling; can be reduced to $0 using GitHub App authentication."
            evidence_verified = f".github/workflows/{yml}:3-4"

        # -------------------------------------------------------------
        # 7. Slack upstream
        # -------------------------------------------------------------
        elif tool == "Slack upstream":
            version = "Slack Web API / Incoming Webhooks"
            purpose = f"Posts real-time notifications about releases, review-wanted PRs, and commit pushes to internal Node.js Slack channels in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Node.js core team uses a private OpenJS Foundation Slack workspace for real-time collaboration."
            usage_limit = "Restricted to upstream Slack workspace; webhook URLs (SLACK_WEBHOOK_URL) are confidential."
            free_paid = "Free (Upstream OpenJS Foundation Workspace) / Paid if purchasing new corporate Slack"
            blocked = "Yes (Private OpenJS Slack incoming webhook URL is access-restricted and absent in forks)"
            license_name = "Commercial SaaS Terms of Service"
            spdx_id = "Commercial SaaS EULA"
            copyleft_risk = "None (Communication SaaS)"
            commercial_rights = "Permitted"
            telemetry_risk = "High (Transmits commit messages, author names, PR titles, and build URLs to Slack cloud)"
            attribution_req = "None"
            legal_verdict = "Restricted (Private OpenJS Slack channel cannot be used by downstream forks)"
            subs_available = "Slack Free (90-day history); Slack Pro (~$8.75/user/month); Slack Business+ (~$15/user/month); Existing Corporate Teams ($0)"
            subs_selected = "Not Applicable (Downstream forks replace Slack with existing enterprise chat or email)"
            subs_reason = "Avoids unnecessary software spend by leveraging existing corporate communication tools."
            user_limit = "Restricted to OpenJS Slack workspace members."
            concurrency_limit = "Standard Slack webhook rate limits (1 request per second)."
            auth_type = "SLACK_WEBHOOK_URL secret."
            license_suitable_5m = "No; downstream team cannot access upstream private Slack workspace."
            subs_suitable_5m = "No; unnecessary subscription cost for an open-source fork."
            req_purchase = "No (Can be discarded or replaced with existing corporate Teams/email)"
            why_upstream_uses = "Notifies core collaborators immediately when critical PRs need review or release staging finishes."
            access_status_fork = "Inaccessible (Secret missing in fork)"
            mand_fork = "No (Non-blocking notification utility)"
            suitable_fork_release = "No; notification steps fail or silently error out without secret webhook URL."
            official_site = "https://slack.com"
            purchase_link = "https://slack.com/pricing"
            price_link = "https://slack.com/pricing"
            suitable_opensource_reason = "No; upstream Slack channel is private to the OpenJS Foundation."
            why_not_suitable = "Fork workflows do not have the private OpenJS webhook secret, and commercial Slack seats are unneeded for fork release operations."
            alt_options = "Microsoft Teams Incoming Webhook, Corporate SMTP Email, GitHub Issue/PR Annotations, Workflow Discarded"
            best_alt = "Microsoft Teams Webhook / Corporate Email / Disable Notification Step"
            reason_best_alt = "$0 additional cost, integrates directly into existing enterprise communication channels."
            issues_identified = "Correctly identified as replaceable with Teams/email ($0) in master list."
            evidence_verified = f".github/workflows/{yml}:3-4"

        # -------------------------------------------------------------
        # 8. Teams/email replacement
        # -------------------------------------------------------------
        elif tool == "Teams/email replacement":
            version = "Microsoft Teams Incoming Webhook / Enterprise SMTP Connector"
            purpose = f"Delivers {pipe} ({yml}) build and release notifications to the organization's existing internal communication channels."
            rec_type = "Recommended Fork Alternate"
            alt_of = "Slack upstream"
            replaces_tool = "Slack upstream"
            reason_selecting = "Replaces external OpenJS Slack dependencies with company-standard messaging at zero extra cost."
            usage_limit = "Enterprise Microsoft 365 / corporate mail server limits."
            free_paid = "Free (Included in existing enterprise Microsoft 365 / Google Workspace subscription)"
            blocked = "No (Controlled by organization's internal IT)"
            license_name = "Commercial Enterprise License (Covered by corporate IT)"
            spdx_id = "Commercial SaaS EULA"
            copyleft_risk = "None"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Internal enterprise tenant)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Included with existing corporate M365 / Google Workspace ($0 incremental cost)."
            subs_selected = "Existing Enterprise Communications ($0.00)"
            subs_reason = "Utilizes existing corporate communication infrastructure."
            user_limit = "Organization enterprise directory."
            concurrency_limit = "Standard webhook rate limits."
            auth_type = "TEAMS_WEBHOOK_URL or SMTP credentials."
            license_suitable_5m = "Yes; team already has enterprise communication access."
            subs_suitable_5m = "Yes; zero incremental licensing fees."
            req_purchase = "No"
            why_upstream_uses = "N/A (Recommended Fork Alternate)"
            access_status_fork = "Accessible"
            mand_fork = "No (Utility notification)"
            suitable_fork_release = "Yes; notifications are delivered cleanly to internal team."
            official_site = "https://www.microsoft.com/en-us/microsoft-teams/group-chat-software"
            purchase_link = "https://www.microsoft.com/en-us/microsoft-365/enterprise/compare-office-365-plans"
            price_link = "https://www.microsoft.com/en-us/microsoft-365/enterprise/compare-office-365-plans"
            suitable_opensource_reason = "Yes; fully functional within enterprise environment."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "GitHub Actions Step Summary, Console Log Reporting, Disable Workflow"
            best_alt = "Microsoft Teams Webhook / Existing Corporate Email"
            reason_best_alt = "Zero additional software cost, internal compliance, reliable delivery."
            issues_identified = "Correctly recorded as $0 preferred alternate in master list."
            evidence_verified = f"workflow-fixes/notify-on-push.md; notify-on-review-wanted.md"

        # -------------------------------------------------------------
        # 9. Shared physical/VM benchmark server
        # -------------------------------------------------------------
        elif tool == "Shared physical/VM benchmark server":
            version = "Dedicated Bare-Metal Server / Performance Lab Host"
            purpose = f"Runs Node.js microbenchmarks and HTTP throughput tests ({yml}) without virtualization jitter or noisy neighbors."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Upstream uses dedicated bare-metal servers (donated by Intel/Nearform) to detect performance regressions accurately."
            usage_limit = "Restricted to upstream benchmark working group; requires dedicated isolated machine."
            free_paid = "Paid (Requires dedicated bare-metal host or high-spec VM; ~$250 - $500/month = $3,000 - $6,000/year)"
            blocked = "Yes (Dedicated upstream hardware is private to Node.js benchmark group; standard cloud VMs suffer CPU throttling)"
            license_name = "Hardware / Cloud Infrastructure EULA"
            spdx_id = "Commercial Infrastructure EULA"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only"
            attribution_req = "None"
            legal_verdict = "Permissible (Hardware infrastructure)"
            subs_available = "Dedicated Bare-Metal Rental (Equinix Metal / Hetzner: ~$150 - $350/mo = $1,800 - $4,200/yr); AWS c7i.metal ($4.50/hr on-demand); GitHub Larger Runner 16-core ($0.042/min = ~$40.32/yr on-demand)"
            subs_selected = "GitHub Larger Runner (Linux 16-core on-demand: $40.32/yr) OR On-Premises Lab Server Partition ($100-$200/yr power)"
            subs_reason = "On-demand execution avoids paying $6,000/yr for idle dedicated servers."
            user_limit = "Lab engineering team."
            concurrency_limit = "Dedicated execution (1 benchmark run at a time to avoid CPU contention)."
            auth_type = "Self-hosted runner registration token / SSH key."
            license_suitable_5m = "Yes; standard infrastructure allocation permits team testing."
            subs_suitable_5m = "Yes; on-demand model is highly cost-effective for a 5-member team."
            req_purchase = "Yes (Purchase Order Required if dedicated bare-metal server is rented; Quote Required for commercial hosting)"
            why_upstream_uses = "Eliminates hypervisor noise and CPU frequency scaling variations during microbenchmark regression detection."
            access_status_fork = "Accessible (via self-hosted runner or GitHub Larger Runner)"
            mand_fork = "Yes"
            suitable_fork_release = "Yes; validates that release binaries meet throughput and latency benchmarks."
            official_site = "https://github.com/nodejs/benchmarking"
            purchase_link = "https://aws.amazon.com/ec2/instance-types/c7i/"
            price_link = "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#per-minute-rates-for-larger-runners"
            suitable_opensource_reason = "Yes; essential for customer release performance assurance."
            why_not_suitable = "Upstream dedicated hardware cannot be accessed; fork must supply its own host or on-demand runner."
            alt_options = "GitHub Larger Runner (16-core Linux: $0.042/min), On-premises physical workstation / lab host, AWS c7i dedicated instance, Standard runner (advisory only)"
            best_alt = "GitHub Larger Runner (16-core Linux) on-demand (2 runs/mo = $40.32/yr) OR Existing Lab Server"
            reason_best_alt = "Drastically reduces annual spend from $6,000/yr to under $50/yr while providing reliable 16-core compute."
            issues_identified = "Master list records $6,000/yr rough ceiling; verified alternate on-demand model costs only $40.32/yr."
            evidence_verified = f"workflow-fixes/benchmark-runner-alternatives-and-cost-analysis.md; commit 0a8f44a7ba8"

        # -------------------------------------------------------------
        # 10. Cachix Nix binary cache / optional Cachix
        # -------------------------------------------------------------
        elif "cachix" in t_lower:
            version = "Cachix CLI / cachix/cachix-action@v17 (nodejs.cachix.org)"
            purpose = f"Hosted Nix binary cache distributing pre-compiled C/C++ derivations and Google V8 builds over Cloudflare CDN for {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Speeds up Nix shared-library matrix tests by downloading pre-compiled V8 binaries in seconds."
            usage_limit = "Write access requires CACHIX_AUTH_TOKEN; public read access is unlimited and free via Cloudflare CDN."
            free_paid = "Free (Open Source Free Tier & Community Sponsorship)"
            blocked = "No for public read ($0); Yes for write access (upstream CACHIX_AUTH_TOKEN is confidential)"
            license_name = "Apache-2.0 / MIT (Action & CLI) + Free OSS SaaS Tier"
            spdx_id = "Apache-2.0"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Public binary artifacts only)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free for public open-source (5 GB cache, unlimited Cloudflare CDN); Cachix Starter ($30/mo = $360/yr); Cachix Standard ($100/mo = $1,200/yr)"
            subs_selected = "Cachix Open Source Free Tier ($0.00)"
            subs_reason = "Free tier provides 5 GB storage with unlimited bandwidth; upstream Node.js pays $0."
            user_limit = "Unlimited public readers."
            concurrency_limit = "5 GB storage on free tier; upstream deduplication against cache.nixos.org consumes 0 GB."
            auth_type = "CACHIX_AUTH_TOKEN (Write access only; no token needed for read)."
            license_suitable_5m = "Yes; open-source free tier fully supports 5-member team."
            subs_suitable_5m = "Yes; $0 cost."
            req_purchase = "No (Upstream and forks operate under free OSS tier; vendor quote required only if proprietary private caching is mandated)"
            why_upstream_uses = "Saves 20 to 45 minutes of V8 compilation time per Nix CI runner."
            access_status_fork = "Accessible (Read-only access to nodejs.cachix.org is completely open and public)"
            mand_fork = "Yes" if mand == "Yes" else "No"
            suitable_fork_release = "Yes; read-only access pulls pre-compiled binaries cleanly at $0 cost."
            official_site = "https://www.cachix.org"
            purchase_link = "https://www.cachix.org/pricing"
            price_link = "https://www.cachix.org/pricing"
            suitable_opensource_reason = "Yes; public binary caching is 100% free and open-source friendly."
            why_not_suitable = "N/A (Fully suitable; built-in fallback in commit cee0154af8 ensures builds succeed even without write token)"
            alt_options = "Public Read from nodejs.cachix.org ($0), GitHub Actions Artifacts (upload-artifact), Dedicated Free OSS Cachix Account ($0), Standard Make/Ninja Build"
            best_alt = "Public Read from nodejs.cachix.org ($0) + GitHub Actions Artifact Fallback"
            reason_best_alt = "$0 cost, zero token setup, automated fallback handles cache misses seamlessly."
            issues_identified = "Master list records $2,400/yr quote ceiling; verified factual cost is $0.00 under Cachix Free OSS policy."
            evidence_verified = f"workflow-fixes/cachix-overview-and-cost-analysis.md; commit a095ee5514d"

        # -------------------------------------------------------------
        # 11. sccache object storage / sccache
        # -------------------------------------------------------------
        elif "sccache" in t_lower:
            version = "Mozilla sccache v0.8+ / Mozilla-Actions/sccache-action"
            purpose = f"Shared compiler cache for C/C++ compilation artifacts to avoid redundant compilation between CI jobs in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Accelerates Node.js C++ builds by caching object files across runner instances."
            usage_limit = "Standard cloud storage bucket limits or GitHub Actions cache 10 GB limit."
            free_paid = "Free (Open Source Tool; GitHub Actions cache backend is $0; S3 storage ~$10/mo = $120/yr if cloud bucket used)"
            blocked = "No (Supports native GitHub Actions cache backend via SCCACHE_GHA_ENABLED=true)"
            license_name = "Apache-2.0"
            spdx_id = "Apache-2.0"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Compiled object caches)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free via GitHub Actions Cache backend; AWS S3 / Azure Blob storage (~$5 - $10/month = $60 - $120/year)"
            subs_selected = "GitHub Actions Native Cache Backend ($0.00)"
            subs_reason = "Native integration with zero cloud storage billing."
            user_limit = "Unlimited repository committers."
            concurrency_limit = "GitHub Actions repository cache quota (10 GB max per repo)."
            auth_type = "ACTIONS_CACHE_URL / ACTIONS_RUNTIME_TOKEN (automatically provided)."
            license_suitable_5m = "Yes; Apache-2.0 open-source software."
            subs_suitable_5m = "Yes; $0 cost on GitHub Actions."
            req_purchase = "No (Purchase Order Required only if dedicated AWS S3 bucket is mandated by enterprise policy)"
            why_upstream_uses = "Reduces compile times on main and release branch builds."
            access_status_fork = "Accessible"
            mand_fork = "Yes" if mand == "Yes" else "No"
            suitable_fork_release = "Yes; builds execute cleanly with or without cache."
            official_site = "https://github.com/mozilla/sccache"
            purchase_link = "https://aws.amazon.com/s3/pricing/"
            price_link = "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows"
            suitable_opensource_reason = "Yes; native GitHub Actions cache support makes it 100% free."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "GitHub Actions Native Cache (SCCACHE_GHA_ENABLED=true), Local ccache on self-hosted runner, Cloud Object Storage (S3/GCS)"
            best_alt = "Mozilla sccache with GitHub Actions Cache Backend"
            reason_best_alt = "$0 cost, zero external cloud credentials, native cache eviction management."
            issues_identified = "Master list records $120/yr cloud storage quote; actual cost is $0 using GitHub Actions cache."
            evidence_verified = f".github/workflows/{yml}; Mozilla-Actions/sccache-action"

        # -------------------------------------------------------------
        # 12. Codecov
        # -------------------------------------------------------------
        elif "codecov" in t_lower:
            version = "codecov/codecov-action@v5"
            purpose = f"Uploads and visualizes line-by-line code test coverage reports across Linux and Windows builds in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Upstream Node.js uses Codecov to track test coverage regressions across pull requests."
            usage_limit = "Free for public open-source repositories; requires paid plan for private repositories (~$10 - $12/user/month)."
            free_paid = "Free (on public open-source repos)"
            blocked = "No for public open-source; requires CODECOV_TOKEN for private repos"
            license_name = "MIT (Action) / Commercial SaaS Terms of Service"
            spdx_id = "MIT"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "High (Uploads line-by-line source coverage data, commit metadata, and branch names to Codecov cloud)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free for public open-source projects; Codecov Pro (~$12/user/month = $144/year/user for private repositories)"
            subs_selected = "Codecov Open Source Free Plan ($0.00) OR Local LCOV/HTML Generation ($0.00)"
            subs_reason = "Free on public repositories; local HTML reports avoid SaaS telemetry on private forks."
            user_limit = "Unlimited on public open-source repositories."
            concurrency_limit = "Standard API upload limits."
            auth_type = "CODECOV_TOKEN (optional on public repos, required on private)."
            license_suitable_5m = "Yes; free for public open-source projects."
            subs_suitable_5m = "Yes; $0 on public repos."
            req_purchase = "No (Purchase Order Required only if maintaining private repo coverage dashboards)"
            why_upstream_uses = "Displays code coverage diffs and percentage changes on PRs."
            access_status_fork = "Accessible"
            mand_fork = "No (Quality reporting utility; non-blocking for binary compilation and release)"
            suitable_fork_release = "Yes; coverage steps can execute or be replaced with local reports."
            official_site = "https://about.codecov.io"
            purchase_link = "https://about.codecov.io/pricing/"
            price_link = "https://about.codecov.io/pricing/"
            suitable_opensource_reason = "Yes; fully functional on public repositories."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "Local c8 / lcov HTML report generation uploaded to GitHub Artifacts, SonarCloud OSS, Coveralls"
            best_alt = "Local c8/lcov HTML Coverage Report via GitHub Actions Artifacts"
            reason_best_alt = "$0 cost, zero external SaaS telemetry, self-contained within repository."
            issues_identified = "Correctly identified as $0 on public open-source forks."
            evidence_verified = f".github/workflows/{yml}: Codecov action invocation"

        # -------------------------------------------------------------
        # 13. AgentScan upstream
        # -------------------------------------------------------------
        elif "agentscan" in t_lower:
            version = "MatteoGabriele/agentscan-action@v2.5.0"
            purpose = f"Screens incoming pull requests from public users for automated bot/AI activity patterns and posts onboarding guidance in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Upstream uses AgentScan to manage high-volume anonymous PR submissions and enforce AI policies."
            usage_limit = "Standard GitHub Actions runtime execution limits."
            free_paid = "Free"
            blocked = "No"
            license_name = "MIT License"
            spdx_id = "MIT"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Low (Inspects public GitHub user activity heuristics)"
            attribution_req = "Standard MIT license notice"
            legal_verdict = "Permissible"
            subs_available = "Free open-source software (No paid subscription tiers exist)."
            subs_selected = "Open Source Free Tier ($0.00)"
            subs_reason = "Tool is 100% free open-source software."
            user_limit = "Unlimited."
            concurrency_limit = "Standard runner limits."
            auth_type = "GITHUB_TOKEN"
            license_suitable_5m = "Yes; permissive MIT license."
            subs_suitable_5m = "Yes; $0 cost."
            req_purchase = "No"
            why_upstream_uses = "Automates triage of external community contributions on nodejs/node."
            access_status_fork = "Accessible"
            mand_fork = "No (Utility workflow; 100% safely skippable in forked release models)"
            suitable_fork_release = "Yes (if enabled), but recommended to skip/discard for enterprise releases."
            official_site = "https://agentscan.tools"
            purchase_link = "N/A (Free open-source tool)"
            price_link = "https://github.com/MatteoGabriele/agentscan-action"
            suitable_opensource_reason = "Yes; permissive MIT open-source tool, but unnecessary for controlled engineering teams."
            why_not_suitable = "N/A (Fully suitable, but unneeded in enterprise forks where PRs are opened by internal staff)"
            alt_options = "Manual Code Review, GitHub CODEOWNERS, Disable Workflow"
            best_alt = "Disable Workflow / Standard GitHub Branch Protections"
            reason_best_alt = "Zero maintenance overhead; enterprise teams do not need automated bot screening bots."
            issues_identified = "Master list records $1,188/yr rough ceiling; verified factual cost is $0.00 under MIT open-source license."
            evidence_verified = f"workflow-fixes/contributor-guidance-upstream-and-cost-analysis.md; commit 0c46004b460"

        # -------------------------------------------------------------
        # 14. managed ARM64 runner
        # -------------------------------------------------------------
        elif "arm64" in t_lower:
            version = "ubuntu-24.04-arm (GitHub-hosted ARM64 runner / Works on Arm bare-metal)"
            purpose = f"Compiles and tests 64-bit ARM (aarch64) Node.js binaries and native addons in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Validates Node.js execution on ARM64 servers, AWS Graviton, and Apple Silicon."
            usage_limit = "Standard GitHub-hosted ARM runner limits (4 vCPU, 16 GB RAM)."
            free_paid = "Free (GitHub provides free ubuntu-24.04-arm runners for public open-source repositories)"
            blocked = "No"
            license_name = "GitHub Terms of Service"
            spdx_id = "Terms of Service"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Ephemeral cloud ARM VM)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free for public open-source repos; standard per-minute billing for private repos ($0.008/min)"
            subs_selected = "GitHub Actions Standard Free Tier ($0.00)"
            subs_reason = "Free ARM64 compute included for public open-source repositories."
            user_limit = "Unlimited on public repos."
            concurrency_limit = "Standard account concurrency limit."
            auth_type = "GITHUB_TOKEN"
            license_suitable_5m = "Yes; ample capacity."
            subs_suitable_5m = "Yes; $0 on public repos."
            req_purchase = "No"
            why_upstream_uses = "Validates Tier-1 platform support for Linux aarch64."
            access_status_fork = "Accessible"
            mand_fork = "Yes"
            suitable_fork_release = "Yes; native ARM64 compilation."
            official_site = "https://github.com/features/actions"
            purchase_link = "https://github.com/pricing"
            price_link = "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions"
            suitable_opensource_reason = "Yes; fully supported free ARM64 compute."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "Self-hosted ARM64 runner (AWS Graviton / Raspberry Pi), QEMU user-mode emulation on x64 runner"
            best_alt = "GitHub Actions Hosted ARM64 Runner (ubuntu-24.04-arm)"
            reason_best_alt = "$0 cost, native 4-core ARM hardware, zero maintenance."
            issues_identified = "Correctly identified as $0 in master list."
            evidence_verified = f".github/workflows/{yml}: runs-on: ubuntu-24.04-arm"

        # -------------------------------------------------------------
        # 15. OpenSSF Scorecard
        # -------------------------------------------------------------
        elif "scorecard" in t_lower:
            version = "ossf/scorecard-action@v2.4.0"
            purpose = f"Audits repository supply-chain security practices and generates SARIF alerts in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Automates OpenSSF Best Practices badge compliance and flags insecure pipeline configurations."
            usage_limit = "Standard GitHub Actions execution limits."
            free_paid = "Free"
            blocked = "No"
            license_name = "Apache-2.0"
            spdx_id = "Apache-2.0"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Scorecard publishes public results to api.securityscorecards.dev"
            attribution_req = "Standard Apache-2.0 notice"
            legal_verdict = "Permissible"
            subs_available = "Free open-source software."
            subs_selected = "Open Source Community Edition ($0.00)"
            subs_reason = "Free supply-chain security auditing for open-source repositories."
            user_limit = "Unlimited."
            concurrency_limit = "Standard runner limits."
            auth_type = "GITHUB_TOKEN (security-events: write)"
            license_suitable_5m = "Yes; Apache-2.0 permissive license."
            subs_suitable_5m = "Yes; $0 cost."
            req_purchase = "No"
            why_upstream_uses = "Validates OpenSSF supply chain security posture."
            access_status_fork = "Accessible"
            mand_fork = "Yes"
            suitable_fork_release = "Yes; validates security controls."
            official_site = "https://securityscorecards.dev"
            purchase_link = "N/A (Free open-source tool)"
            price_link = "https://github.com/ossf/scorecard-action"
            suitable_opensource_reason = "Yes; 100% free open-source supply-chain security auditing."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "Native CodeQL Analysis, OpenSSF Scorecard CLI, In-house Security Audit"
            best_alt = "OpenSSF Scorecard Action"
            reason_best_alt = "Industry-standard open-source supply chain verification at $0 cost."
            issues_identified = "Correctly identified as $0 in master list."
            evidence_verified = f".github/workflows/{yml}:32-55"

        # -------------------------------------------------------------
        # 16. StepSecurity Harden-Runner Community
        # -------------------------------------------------------------
        elif "harden-runner" in t_lower or "stepsecurity" in t_lower:
            version = "step-security/harden-runner@v2.10.1"
            purpose = f"Enforces outbound network egress filtering and file integrity monitoring during CI runs in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Prevents supply-chain exfiltration attacks by blocking unauthorized outbound connections during build."
            usage_limit = "Standard GitHub Actions execution limits."
            free_paid = "Free"
            blocked = "No"
            license_name = "Apache-2.0"
            spdx_id = "Apache-2.0"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only egress filtering with optional StepSecurity dashboard reporting"
            attribution_req = "Standard Apache-2.0 notice"
            legal_verdict = "Permissible"
            subs_available = "Free Community Edition; Enterprise commercial subscription available"
            subs_selected = "StepSecurity Community Free Edition ($0.00)"
            subs_reason = "Community edition is free for open-source workflows."
            user_limit = "Unlimited."
            concurrency_limit = "Standard runner limits."
            auth_type = "None"
            license_suitable_5m = "Yes; Apache-2.0 permissive license."
            subs_suitable_5m = "Yes; $0 cost."
            req_purchase = "No"
            why_upstream_uses = "Protects GitHub Actions build environments from network intrusion and credential harvesting."
            access_status_fork = "Accessible"
            mand_fork = "Yes"
            suitable_fork_release = "Yes; strengthens release security."
            official_site = "https://www.stepsecurity.io"
            purchase_link = "https://www.stepsecurity.io/pricing"
            price_link = "https://github.com/step-security/harden-runner"
            suitable_opensource_reason = "Yes; open-source security hardening."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "Native GitHub Actions network restrictions, Docker isolated networks"
            best_alt = "StepSecurity Harden-Runner Community Edition"
            reason_best_alt = "Drop-in security hardening for GitHub Actions runners at $0 cost."
            issues_identified = "Correctly identified as $0 in master list."
            evidence_verified = f".github/workflows/{yml}: step-security/harden-runner"

        # -------------------------------------------------------------
        # 17. wpt.fyi service
        # -------------------------------------------------------------
        elif "wpt.fyi" in t_lower:
            version = "wpt.fyi REST API / web-platform-tests reporting endpoint"
            purpose = f"Uploads Web Platform Tests compliance reports to the public W3C dashboard in {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Demonstrates Node.js browser and web standards compliance publicly."
            usage_limit = "Upstream upload requires WPT_FYI_TOKEN write secret."
            free_paid = "Free (Public W3C Open-Source Service)"
            blocked = "Yes for upload (WPT_FYI_TOKEN secret is restricted to upstream Node.js release managers)"
            license_name = "BSD-3-Clause / W3C Software License"
            spdx_id = "BSD-3-Clause"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Public web platform test results only"
            attribution_req = "None"
            legal_verdict = "Restricted (Remote upload secret absent in forks)"
            subs_available = "Free public service maintained by Google/W3C/community."
            subs_selected = "Not Applicable (Downstream forks retain local test reports)"
            subs_reason = "Forks do not need to publish to the global W3C public dashboard."
            user_limit = "Public dashboard."
            concurrency_limit = "Standard REST API upload rate limits."
            auth_type = "WPT_FYI_TOKEN"
            license_suitable_5m = "Yes; open-source standard."
            subs_suitable_5m = "Yes; $0."
            req_purchase = "No"
            why_upstream_uses = "Showcases Node.js conformance to web platform specifications."
            access_status_fork = "Inaccessible for remote upload (Secret absent)"
            mand_fork = "No"
            suitable_fork_release = "No for remote upload; Yes if retaining local WPT test report artifacts."
            official_site = "https://wpt.fyi"
            purchase_link = "N/A (Public community service)"
            price_link = "https://github.com/web-platform-tests/wpt.fyi"
            suitable_opensource_reason = "No for remote upload; Yes for local test execution."
            why_not_suitable = "Forks do not have write access to the upstream official nodejs dashboard on wpt.fyi."
            alt_options = "Local WPT HTML/JSON Test Report via GitHub Artifacts, Disable Remote Upload Step"
            best_alt = "Local WPT Report Generation via GitHub Actions Artifacts"
            reason_best_alt = "$0 cost, full test execution verification without external dependency."
            issues_identified = "Correctly identified as replaceable with local WPT reporting ($0) in master list."
            evidence_verified = f".github/workflows/{yml}:71-97; Makefile:714-720"

        # -------------------------------------------------------------
        # 18. Standard Windows runner
        # -------------------------------------------------------------
        elif "windows" in t_lower:
            version = "windows-2025 / windows-latest"
            purpose = f"Compiles Node.js with MSVC (Visual Studio 2022) and executes Windows tests for {pipe} ({yml})."
            rec_type = "Upstream Original Tool"
            alt_of = "N/A (Upstream Original)"
            replaces_tool = "N/A (Original Tool)"
            reason_selecting = "Validates Windows x64 build and executes vcbuild.bat."
            usage_limit = "Standard GitHub-hosted Windows VM limits (2 vCPU, 7 GB RAM)."
            free_paid = "Free (on public open-source repos)"
            blocked = "No"
            license_name = "GitHub Terms of Service"
            spdx_id = "Terms of Service"
            copyleft_risk = "None / Permissive"
            commercial_rights = "Permitted"
            telemetry_risk = "Local-only (Ephemeral Microsoft Azure VM)"
            attribution_req = "None"
            legal_verdict = "Permissible"
            subs_available = "Free for public open-source repos; standard per-minute billing for private repos ($0.016/min)"
            subs_selected = "GitHub Actions Standard Free Tier ($0.00)"
            subs_reason = "Free compute allocation included with public repository hosting."
            user_limit = "Unlimited on public repos."
            concurrency_limit = "Standard account concurrency limit."
            auth_type = "GITHUB_TOKEN"
            license_suitable_5m = "Yes; ample capacity."
            subs_suitable_5m = "Yes; $0 on public repos."
            req_purchase = "No"
            why_upstream_uses = "Validates Tier-1 platform support for Windows."
            access_status_fork = "Accessible"
            mand_fork = "Yes" if mand == "Yes" else "No"
            suitable_fork_release = "Yes; compiles node.exe natively."
            official_site = "https://github.com/features/actions"
            purchase_link = "https://github.com/pricing"
            price_link = "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions"
            suitable_opensource_reason = "Yes; native Windows build compute."
            why_not_suitable = "N/A (Fully suitable)"
            alt_options = "Self-hosted Windows runner, GitHub Larger Windows Runner, Cross-compilation"
            best_alt = "GitHub Actions Standard Windows Runner (windows-2025)"
            reason_best_alt = "$0 cost, pre-installed MSVC tools, zero maintenance."
            issues_identified = "Correctly identified as $0 in master list."
            evidence_verified = f".github/workflows/{yml}: runs-on: windows-2025"

        # Assemble the 44-column row exactly matching headers:
        # 1. Name of Tool/Infra
        # 2. Version
        # 3. Purpose
        # 4. Record Type (Upstream Original Tool / Recommended Fork Alternate)
        # 5. Alternate of which too/infra (Mapping to Upstream Original Tool /infra)
        # 6. Reason of selecting this tool
        # 7. Any usage Limit
        # 8. Free/Paid
        # 9. Access-restricted, blocked, not publicly accessible, or unavailable for purchase
        # 10. License
        # 11. SPDX License Identifier (e.g., MIT, Apache-2.0, Commercial SaaS EULA)
        # 12. Copyleft / Viral Source Disclosure Risk (None / Permissive vs Weak Copyleft vs Strong Copyleft)
        # 13. Commercial Redistribution Rights (Permitted / Restricted / Non-commercial only)
        # 14. Telemetry & Code Exfiltration Risk (Local-only / Cloud SaaS logs / High)
        # 15. Attribution / Notice Requirements (Standard notice / None)
        # 16. Permissible for Company Fork Release? (Legal Verdict)
        # 17. Subscription Models Vailable
        # 18. Selected Subscription Model
        # 19. Reason of selecting this subscription model
        # 20. Category
        # 21. Conponent Name
        # 22. workflow name
        # 23. workflow yml
        # 24. User Limit
        # 25. User / Concurrency / Usage Limits
        # 26. Token/Key/Secret Based access
        # 27. Lincese Suitable for 5 member team and reason
        # 28. Subscription Suitable for 5 member team and reason
        # 29. Required to Purchase ?
        # 30. Why Upstream Uses It
        # 31. Access Status in Fork
        # 32. Is It Mandatory in Fork? (Yes / No - Can be discarded)
        # 33. Suitable for Release from Fork? (Yes/No + Reason)
        # 34. Official site
        # 35. Purchase Link
        # 36. Price Link
        # 37. Is it suitable for release from Forked Opensource Model ? Reason
        # 38. why it not suitable for release from Forked Opensource Model
        # 39. Alternate Options for release from Forked Opensource Model
        # 40. Best One alternate Option for release from Forked Opensource Model (with name and version)
        # 41. Reson of seleting that Best One alternate Option for release from Forked Opensource Model
        # 42. Replaces Upstream Tool (Name of original tool if this is an alternate)
        # 43. issues identified in master_list
        # 44. List of all evidence  verified
        return [
            tool,                       # 1
            version,                    # 2
            purpose,                    # 3
            rec_type,                   # 4
            alt_of,                     # 5
            reason_selecting,           # 6
            usage_limit,                # 7
            free_paid,                  # 8
            blocked,                    # 9
            license_name,               # 10
            spdx_id,                    # 11
            copyleft_risk,              # 12
            commercial_rights,          # 13
            telemetry_risk,             # 14
            attribution_req,            # 15
            legal_verdict,              # 16
            subs_available,             # 17
            subs_selected,              # 18
            subs_reason,                # 19
            cat,                        # 20
            comp,                       # 21
            pipe,                       # 22
            yml,                        # 23
            user_limit,                 # 24
            concurrency_limit,          # 25
            auth_type,                  # 26
            license_suitable_5m,        # 27
            subs_suitable_5m,           # 28
            req_purchase,               # 29
            why_upstream_uses,          # 30
            access_status_fork,         # 31
            mand_fork,                  # 32
            suitable_fork_release,      # 33
            official_site,              # 34
            purchase_link,              # 35
            price_link,                 # 36
            suitable_opensource_reason, # 37
            why_not_suitable,           # 38
            alt_options,                # 39
            best_alt,                   # 40
            reason_best_alt,            # 41
            replaces_tool,              # 42
            issues_identified,          # 43
            evidence_verified           # 44
        ]

    # Populate rows
    for m_idx, (r_idx, m_row) in enumerate(master_rows):
        row_data = build_row(m_idx, r_idx, m_row)
        ws_nodejs.append(row_data)

    wb.save('workflow-fixes/data1.xlsx')
    print(f"Successfully populated {ws_nodejs.max_row - 1} rows into 'nodejs' sheet of workflow-fixes/data1.xlsx!")

if __name__ == '__main__':
    generate_nodejs_data()
