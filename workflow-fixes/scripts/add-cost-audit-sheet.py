#!/usr/bin/env python3
"""
add-cost-audit-sheet.py - Adds the 'paid_tools_cost_audit' sheet to
nodejs_pipeline_result.xlsx, node_pipeline_result.xlsx, and pipeline_result.xlsx
documenting the exact tool used before change, cost before change,
cost after change ($0.00), and evidence check details.
"""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

HEADERS = [
    "#",
    "Tool / Library Name (Before Change)",
    "Actual Tool or Library Used Before My Change",
    "Actual Tool or Library Used After My Code Change (GitHub-Native)",
    "Rough Cost of Tool Used Before My Change",
    "Cost of Tool Used After My Code Change",
    "Vendor",
    "License",
    "Subscription Model",
    "Actual Pipeline(s) Used (After Evidence Check)",
    "Evidence Check Details (Syntax & Secrets from Original YAML)",
    "Description & Use in Workflow Before Change",
    "GitHub Enterprise + Public Repo Applicability & OSS Release Impact"
]

ROWS = [
    (
        1,
        "Node.js Foundation Custom Runners",
        "OpenJS Foundation custom-built ubuntu-slim container / VM self-hosted runner infrastructure.",
        "Standard GitHub-hosted Linux runner (ubuntu-latest) via dynamic runner expression: ${{ vars.RUNNER_LABEL || 'ubuntu-latest' }}.",
        "$500 – $2,500 / month in dedicated server / VM hosting fees.",
        "$0.00 / month (100% Free on public repos).",
        "OpenJS Foundation / Node.js Build Workgroup",
        "Custom Infrastructure (Internal scripts MIT)",
        "Infrastructure Hosting (Dedicated Bare-Metal / Cloud VM Leases)",
        "Hardcoded in 42 workflows (e.g. doc.yml, linters.yml, commit-lint.yml, test-linux.yml, build-tarball.yml, scorecard.yml, codeql.yml, auto-start-ci.yml)",
        "runs-on: ubuntu-slim verified across 42 upstream YAML files at commit fe40b317efe.",
        "Used upstream as a lightweight pre-warmed virtual machine to minimize runner boot time and execute general CI tasks.",
        "Inaccessible on forks without deploying and paying for private VM infrastructure. Standard GitHub-hosted ubuntu-latest runs at $0 cost on public repos."
    ),
    (
        2,
        "OpenJS Foundation Dedicated Jenkins Farm",
        "OpenJS Foundation private Jenkins CI server cluster (https://ci.nodejs.org) invoked via @node-core/utils CLI.",
        "Native GitHub Actions matrix workflows on standard GitHub runners + Dual-Mode simulation fallback step with markdown Step Summary report.",
        "$3,000 – $10,000+ / month in multi-cloud hosting, hardware leases, power, and bandwidth across Equinix, AWS, DigitalOcean, and Rackspace.",
        "$0.00 / month (Runs entirely on standard free GitHub Actions runners).",
        "OpenJS Foundation / CloudBees / Dedicated Hosting Providers",
        "Jenkins is MIT (Open Source); Infrastructure is proprietary multi-cloud dedicated hosting",
        "Dedicated Infrastructure Hosting (Multi-Cloud / Hardware Leases)",
        "auto-start-ci.yml, commit-queue.yml",
        "npx @node-core/utils -u ${{ secrets.JENKINS_USER }} -t ${{ secrets.JENKINS_TOKEN }} calling ci.nodejs.org at lines in auto-start-ci.yml and commit-queue.yml.",
        "Orchestrated remote compilation and testing across exotic architectures (IBM AIX, IBM z/OS s390x, PowerPC ppc64le, SmartOS, Windows ARM64) before landing pull requests.",
        "Inaccessible to external forks; requires private foundation authentication. Dual-Mode executes locally or simulates safely at $0 cost."
    ),
    (
        3,
        "GitHub-Hosted Managed ARM64 Runners",
        "GitHub Actions managed 64-bit ARM compute runners (ubuntu-24.04-arm).",
        "Standard GitHub-hosted Linux runners (ubuntu-latest) via fallback expression ${{ vars.ARM_RUNNER_LABEL || vars.RUNNER_LABEL || 'ubuntu-latest' }} (or optional free self-hosted ARM runner).",
        "$0.005 / min (2-core) to $0.010 / min (4-core) -> $500 – $1,500 / month at full Node.js compilation build volume.",
        "$0.00 / month (Runs on free standard ubuntu-latest).",
        "GitHub, Inc. / Microsoft Corporation",
        "Proprietary Cloud Compute",
        "Usage-based per runner minute (Billed directly to Enterprise account)",
        "build-tarball.yml, coverage-linux.yml, test-shared.yml",
        "runs-on: ubuntu-24.04-arm verified in upstream build-tarball.yml, coverage-linux.yml, and test-shared.yml.",
        "Dedicated 64-bit ARM (AArch64) virtual machines for verifying ARM compilation, V8 JIT code generation on AArch64, and shared library linkages.",
        "Unlike standard x86 runners, managed ARM64 runners incur per-minute billing against the Enterprise account even in public repos. Fallback to ubuntu-latest eliminates this cost."
    ),
    (
        4,
        "Codecov Coverage Platform",
        "Codecov SaaS platform integration via codecov/codecov-action@fb8b358... requiring CODECOV_TOKEN.",
        "GitHub-native coverage pipeline using open-source gcovr, rendering formatted coverage markdown into $GITHUB_STEP_SUMMARY, and uploading coverage-report artifact.",
        "$0.00 (sponsored community tier for upstream public repo) OR $12 / user / month (Standard Pro tier if run in private/team environment).",
        "$0.00 / month (Native Step Summary & Artifacts; zero token or SaaS dependency).",
        "Sentry / Codecov Inc.",
        "Commercial SaaS (Action wrapper is Apache-2.0)",
        "Tiered SaaS (Free for OSS / Per Seat / Month for Private Enterprise)",
        "coverage-linux.yml, coverage-linux-without-intl.yml, coverage-windows.yml",
        "uses: codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f with token: ${{ secrets.CODECOV_TOKEN }} in upstream coverage workflows.",
        "Aggregated coverage LCOV data to generate web-based visual diffs, PR comments, and coverage change metrics.",
        "Public open-source repos qualify for free Codecov accounts. Step Summary and Actions Artifacts provide full auditability with zero third-party token management."
    ),
    (
        5,
        "Cachix Nix Binary Cache",
        "Cachix SaaS binary cache (https://nodejs.cachix.org) via cachix/cachix-action requiring CACHIX_AUTH_TOKEN.",
        "Standard direct native compilation (Clang/GCC) and GitHub Actions Cache (actions/cache@v4), with automatic bypass when token is unconfigured.",
        "$40 – $200 / month (Pro plan at $40/mo for 200 GB, or Team plan at $200/mo for 1 TB required for multi-GB Nix package caches).",
        "$0.00 / month (Standard compiler build / GitHub 10 GB free cache).",
        "Cachix Inc. / Domen Kožar",
        "Commercial SaaS (Client is Apache-2.0)",
        "Monthly Storage & Bandwidth Tiered SaaS",
        "build-shared.yml, benchmark.yml, nix-changes.yml, test-shared.yml",
        "uses: cachix/cachix-action@5f2d7c5294214f71b873db4b969586b980625e71 with authToken: ${{ secrets.CACHIX_AUTH_TOKEN }} and name: nodejs.",
        "Cloud-hosted binary cache storing pre-compiled Nix derivations and packages for shared library builds, avoiding multi-hour Nix compilation.",
        "Upstream cache is write-protected. Dual-Mode builds cleanly without Cachix at $0 cost."
    ),
    (
        6,
        "Slack Enterprise Messaging",
        "Slack webhook messaging via rtCamp/action-slack-notify@33ca3be... requiring SLACK_WEBHOOK.",
        "GitHub Actions native Step Summaries ($GITHUB_STEP_SUMMARY) and GitHub Release Announcements (or optional free Discord/Zulip webhook).",
        "$7.25 – $12.50 / user / month (Slack Pro / Business+) or $15 – $25 / user / month (Enterprise Grid).",
        "$0.00 / month (Rendered in GitHub Step Summary).",
        "Salesforce, Inc. / Slack Technologies LLC",
        "Commercial SaaS",
        "Per User Seat / Month (Annual/Monthly)",
        "notify-on-push.yml, notify-on-review-wanted.yml, post-release.yml",
        "uses: rtCamp/action-slack-notify@33ca3be66c6f378fe1610fd1d5258632dbed5e58 with env: SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }} in upstream notification workflows.",
        "Broadcasted real-time build notifications, commit landing alerts, and review requests to private team channels (#node-dev, #node-releases).",
        "Public open-source repos rarely use private Slack channels due to spam risk and per-user seat costs. Step Summaries provide complete native visibility."
    ),
    (
        7,
        "Upstream Bot Collaborator Accounts",
        "Dedicated bot account Personal Access Token (GH_USER_TOKEN, e.g. for @nodejs-github-bot).",
        "Built-in repository ${{ secrets.GITHUB_TOKEN }} with explicit scoped job permissions (contents: write, pull-requests: write).",
        "$21 / user / month (Standard GitHub Enterprise Cloud user seat allocated for a bot account).",
        "$0.00 / month (Built-in $GITHUB_TOKEN is 100% free with unlimited token generation).",
        "GitHub, Inc.",
        "GitHub User Account",
        "Per User Seat / Month",
        "22 workflows (e.g. create-release-proposal.yml, tools.yml, update-openssl.yml, update-v8.yml, update-wpt.yml, timezone-update.yml, find-inactive-collaborators.yml)",
        "git push https://${{ secrets.GH_USER_TOKEN }}@github.com/... and env: GITHUB_TOKEN: ${{ secrets.GH_USER_TOKEN }} across 22 upstream YAMLs.",
        "Used by maintainer automation bots to push release branches, bypass branch protection rules, and open pull requests.",
        "Built-in $GITHUB_TOKEN completely replaces the need for paid bot seats."
    ),
    (
        8,
        "Mozilla sccache Cloud Storage",
        "Mozilla sccache with cloud object storage bucket backend (AWS S3 / Google Cloud Storage / Azure Blob).",
        "GitHub Actions native Cache (actions/cache@v4 with 10 GB free cache storage per repository) or local ephemeral compilation.",
        "$10 – $50 / month in cloud storage bucket fees and network egress transfer.",
        "$0.00 / month (10 GB free cache per repository provided natively by GitHub Actions).",
        "Mozilla (Client) + AWS / Google Cloud / Microsoft Azure",
        "Client is Apache-2.0; Cloud Storage backend is commercial cloud storage",
        "Cloud Pay-As-You-Go",
        "build-tarball.yml, coverage-linux.yml, coverage-linux-without-intl.yml, stress-test.yml, test-internet.yml",
        "uses: Mozilla-Actions/sccache-action@fc920bf0ec8de6ee65d409111f7ec508035751ba in upstream compiler workflows.",
        "Distributed compiler cache for C/C++ (Clang/GCC) to cache compilation artifacts and accelerate recompilation across workflow runs.",
        "Native GitHub cache eliminates all cloud storage configuration and cloud provider billing."
    ),
    (
        9,
        "StepSecurity Harden-Runner",
        "StepSecurity Harden-Runner agent (step-security/harden-runner@05e315...).",
        "StepSecurity Harden-Runner in free community audit mode + GitHub Actions least-privilege token permissions (permissions: read-all).",
        "$0.00 (Free community edition on public repos) OR $10 – $20 / dev / month (Enterprise plan for private repositories).",
        "$0.00 / month (Runs in free audit mode on public repository).",
        "StepSecurity, Inc.",
        "Apache-2.0 (Agent) / Proprietary SaaS (Dashboard)",
        "Per Developer / Month (Enterprise)",
        "scorecard.yml",
        "uses: step-security/harden-runner@05e31511f85b41b11d1cf0ef85d0992719546e2c in upstream scorecard.yml.",
        "Runtime container security agent that monitors process activity, network socket connections, and DNS queries on runners to prevent token exfiltration.",
        "100% free for public open-source repositories."
    ),
    (
        10,
        "GitHub Advanced Security (GHAS) / CodeQL",
        "CodeQL analysis (github/codeql-action).",
        "GitHub CodeQL analysis (github/codeql-action@v3) publishing SARIF alerts to GitHub Security tab and step summary.",
        "$0.00 on public repositories (OR $49 / active committer / month if private).",
        "$0.00 / month (Free for all public repositories).",
        "GitHub, Inc. / Microsoft Corporation",
        "Proprietary GitHub Feature",
        "Per Active Committer / Month (Waived / Free on public repos)",
        "codeql.yml, scorecard.yml",
        "uses: github/codeql-action/init@..., analyze@..., upload-sarif@... in upstream security workflows.",
        "Deep semantic code analysis engine for C/C++ and JavaScript, performing SAST vulnerability detection, taint tracking, and SARIF alert generation.",
        "100% free and uncapped for public open-source releases under GitHub Enterprise Cloud."
    ),
    (
        11,
        "AgentScan PR Bot Scanner",
        "AgentScan cloud service via MatteoGabriele/agentscan-action@8112fb... calling https://agentscan.tools.",
        "GitHub native branch protection rules, required reviewer approvals, and template automation (or simulation mode).",
        "$0.00 (Free community tier) OR $19 – $99 / month (Commercial API plan).",
        "$0.00 / month (Handled natively by GitHub).",
        "AgentScan / Matteo Gabriele",
        "Freemium SaaS / Cloud API",
        "Monthly API Tier",
        "contributor-guidance.yml",
        "uses: MatteoGabriele/agentscan-action@8112fb79b33fafb8506159df20129a34209ac410 calling https://agentscan.tools.",
        "Analyzes pull request descriptions and comments using AI heuristics to detect spam or bot-generated contributions.",
        "Not needed for release engineering; safe to bypass."
    ),
    (
        12,
        "Web Platform Tests (WPT) Ingestion API",
        "Official WPT submission API (https://wpt.fyi/api/results/upload) requiring WPT_FYI_PASSWORD and WPT_FYI_USER.",
        "Local WPT runner executing tests locally and saving output JSON/HTML to downloadable GitHub Actions Artifacts (wpt-report).",
        "$0.00 (Sponsored by W3C/Google), but closed/restricted to authorized consortium credentials.",
        "$0.00 / month (Artifacts stored on GitHub for free).",
        "W3C / Google Cloud / Bocoup",
        "Open Source Platform / Restricted Upload API",
        "Consortium Private Authentication",
        "daily-wpt-fyi.yml",
        "WPT_FYI_PW: ${{ secrets.WPT_FYI_PASSWORD }} uploading to https://wpt.fyi/api/results/upload in daily-wpt-fyi.yml.",
        "Ingestion server for publishing official Node.js web standard compatibility test results to the cross-engine wpt.fyi dashboard.",
        "Inaccessible to forks; local artifacts provide full validation at $0 cost."
    ),
    (
        13,
        "GitHub Actions Standard Runners",
        "Standard GitHub-hosted Linux, Windows, and macOS virtual machine runners.",
        "Standard GitHub-hosted runners (ubuntu-latest, windows-2025, macos-15).",
        "$0.00 / month on public repos (or $0.008 Linux, $0.016 Windows, $0.08 macOS per min if private).",
        "$0.00 / month (100% Free on public repos).",
        "GitHub, Inc. / Microsoft Corporation",
        "Proprietary SaaS",
        "Usage-based (Free on public repos)",
        "Used across remaining workflows (e.g. linters.yml, doc.yml, commit-lint.yml, test-linux.yml)",
        "runs-on: ubuntu-latest, macos-15, windows-2025 across upstream workflows.",
        "Managed virtual machine execution environments across Linux, Windows, and macOS runtimes to build, test, lint, and package Node.js.",
        "100% Free. Public repositories receive unlimited standard runner minutes at $0 cost."
    )
]

COL_WIDTHS = {
    1: 6,
    2: 30,
    3: 35,
    4: 35,
    5: 25,
    6: 22,
    7: 25,
    8: 24,
    9: 25,
    10: 35,
    11: 40,
    12: 35,
    13: 35
}


def add_sheet_to_workbook(filepath: str):
    print(f"Opening {filepath}...")
    try:
        wb = openpyxl.load_workbook(filepath)
    except Exception as e:
        print(f"Error opening {filepath}: {e}")
        return

    sheet_name = "paid_tools_cost_audit"
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]

    ws = wb.create_sheet(title=sheet_name)

    # Header styling
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # Write Headers
    for c_idx, h_text in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = border_thin

    ws.row_dimensions[1].height = 45

    # Zebra fill
    alt_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    data_font = Font(name="Calibri", size=10)

    # Write Data
    for r_idx, row_data in enumerate(ROWS, 2):
        ws.row_dimensions[r_idx].height = 80
        is_even = (r_idx % 2 == 0)
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.border = border_thin
            if c_idx in [1, 5, 6]:
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            if is_even:
                cell.fill = alt_fill

    # Set Column Widths
    for c_idx, width in COL_WIDTHS.items():
        col_letter = openpyxl.utils.get_column_letter(c_idx)
        ws.column_dimensions[col_letter].width = width

    try:
        wb.save(filepath)
        print(f"Successfully added '{sheet_name}' to {filepath}")
    except PermissionError:
        print(f"Notice: {filepath} is locked by another process (e.g. Excel).")


def main():
    targets = [
        "workflow-fixes/nodejs_pipeline_result.xlsx",
        "workflow-fixes/node_pipeline_result.xlsx",
        "workflow-fixes/pipeline_result.xlsx"
    ]
    for t in targets:
        add_sheet_to_workbook(t)


if __name__ == "__main__":
    main()
