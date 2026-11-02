#!/usr/bin/env python3
"""
fill-column-33.py - Populates Column 33 ("Do we need this pipeline in forked repo
for enterprise release ? Answer with reason") in workflow-fixes/node_pipeline_result.xlsx
and workflow-fixes/nodejs_pipeline_result.xlsx for all 45 Node.js CI/CD workflows.
"""

import os
import shutil
import openpyxl
from openpyxl.styles import Alignment, Font

COL_33_DATA = {
    "doc.yml": (
        "Yes. Generates, formats, and validates the official Node.js API documentation "
        "and HTML/JSON artifacts. Enterprise releases require official, version-matched "
        "documentation bundled with distribution archives or published to internal enterprise "
        "developer portals for developer guidance and compliance."
    ),
    "linters.yml": (
        "Yes. Enforces static code quality, syntax standards, and formatting rules across C++ "
        "(clang-format, cpplint), JavaScript (ESLint), and Python (flake8). Essential in enterprise "
        "release pipelines to prevent syntax regressions, compiler warnings, and style deviations "
        "prior to production binary packaging."
    ),
    "scorecard.yml": (
        "Yes. Executes OpenSSF Scorecard supply-chain security analysis (evaluating branch protection, "
        "pinned dependencies, token permissions, and binary tampering). Vital for enterprise governance, "
        "SOC2/FedRAMP compliance, and verifying software supply-chain integrity for enterprise distributions."
    ),
    "commit-lint.yml": (
        "Yes. Validates commit message formatting and DCO sign-offs (Signed-off-by) against repository "
        "standards. Required for automated changelog generation, clean git audit trails, and legal IP "
        "contributor attribution in enterprise release governance."
    ),
    "create-release-proposal.yml": (
        "Yes. Core release engineering workflow that automates preparing release candidate branches, "
        "updating version headers (src/node_version.h), regenerating changelogs, and drafting formal release "
        "proposals for enterprise staging and QA validation."
    ),
    "daily-wpt-fyi.yml": (
        "No. Specifically designed to run nightly Web Platform Tests and push results to the external public "
        "wpt.fyi dashboard using upstream credentials. Enterprise releases do not publish test metrics to public "
        "dashboards, and WPT compliance is already validated internally in local test jobs."
    ),
    "label-pr.yml": (
        "No. Upstream community triage automation that attaches subsystem labels (e.g., crypto, fs, doc) based "
        "on changed file paths. Enterprise release workflows rely on internal project management tools (e.g., Jira, "
        "Azure DevOps) and designated codeowners rather than public GitHub labeling bots."
    ),
    "tools.yml": (
        "No. Automatically scans and updates auxiliary development dependencies and linting tool configurations. "
        "In enterprise release environments, all toolchain dependencies must be strictly version-pinned and manually "
        "vetted through corporate change control rather than upgraded automatically by bot."
    ),
    "update-wpt.yml": (
        "No. Periodically syncs and updates the vendored Web Platform Tests test suite from the upstream WPT repository. "
        "For predictable and repeatable enterprise releases, test specifications must remain frozen to the target release "
        "baseline rather than continuously drifting."
    ),
    "benchmark.yml": (
        "No. Runs micro-benchmarks against V8 and Node.js core subsystems. While helpful for isolated performance tuning, "
        "micro-benchmarks are non-deterministic on shared cloud runners, consume excessive runner minutes, and are not a "
        "gating requirement for enterprise binary packaging."
    ),
    "build-tarball.yml": (
        "Yes. Essential release packaging pipeline that builds official source distribution tarballs (node-vX.Y.Z.tar.gz), "
        "unpacks them, and verifies clean standalone compilation. Mandatory for generating official source release assets "
        "distributed to enterprise package repositories."
    ),
    "coverage-windows.yml": (
        "Yes. Compiles Node.js and executes unit test suites on Windows Server runners, measuring test coverage and validating "
        "Win32/IOCP APIs. Crucial for certifying enterprise releases intended for Windows Server and Windows enterprise desktop "
        "environments."
    ),
    "daily.yml": (
        "No. Nightly build trigger intended for upstream continuous integration against bleeding-edge master. Enterprise release "
        "cadences follow controlled milestones (Release Candidates, Feature Freezes, and Staged GA) rather than unvetted daily "
        "automated runs."
    ),
    "stress-test.yml": (
        "No. An upstream-specific optimization pipeline that rebases pull requests on main to maximize GitHub Actions runner cache "
        "hit rates. Not required for release pipelines, which must build deterministically from clean, immutable release tags."
    ),
    "test-linux-perfetto.yml": (
        "Yes. Builds and tests Node.js with Google Perfetto system tracing instrumentation enabled. Necessary for enterprise "
        "deployments where production application performance monitoring (APM), kernel-level tracing, and distributed "
        "observability are mandatory operational standards."
    ),
    "test-linux-quic.yml": (
        "Yes. Validates Node.js compilation and networking tests with QUIC and HTTP/3 support (ngtcp2 / nghttp3). Critical for "
        "enterprise microservices and edge architectures adopting modern HTTP/3 transport protocols."
    ),
    "test-linux.yml": (
        "Yes. Primary Linux compilation and comprehensive unit/integration test pipeline across multiple compiler configurations. "
        "Absolutely mandatory for enterprise releases, as Linux is the predominant enterprise server and container deployment target."
    ),
    "test-macos.yml": (
        "Yes. Compiles and runs test suites on macOS (Darwin). Required if the enterprise distributes developer runtimes, CLI "
        "utilities, or server software targeting macOS workstations and Apple Silicon environments."
    ),
    "test-shared.yml": (
        "Yes. Validates Node.js built against external shared system libraries (shared OpenSSL, zlib, libuv, nghttp2). Essential "
        "for enterprise Linux distributions (RHEL, Rocky, Debian) that mandate linking against system-approved, FIPS-compliant "
        "cryptographic libraries."
    ),
    "codeql.yml": (
        "Yes. GitHub-native Static Application Security Testing (SAST) scanning C/C++ and JavaScript codebases for security "
        "vulnerabilities (CWEs, memory safety, injection). Mandatory for enterprise security clearance and corporate vulnerability "
        "management compliance."
    ),
    "contributor-guidance.yml": (
        "No. Community greeting bot that posts welcoming remarks and contributor guide links to first-time public open-source "
        "contributors. Completely irrelevant in an enterprise fork maintained by dedicated internal engineering teams."
    ),
    "find-inactive-collaborators.yml": (
        "No. Audits git commit history to flag inactive upstream Node.js open-source collaborators. Enterprise repository "
        "permissions and team memberships are managed via corporate identity providers (SSO/SCIM) and enterprise IAM, making "
        "this bot redundant."
    ),
    "find-inactive-tsc.yml": (
        "No. Monitors Technical Steering Committee voting quorum and attendance records for upstream Node.js governance. Has no "
        "purpose in an enterprise organization where release authority is held by designated engineering leads and release managers."
    ),
    "license-builder.yml": (
        "Yes. Scans all vendored third-party dependencies (V8, OpenSSL, zlib, libuv, etc.) and regenerates the consolidated LICENSE "
        "file. Strictly required for enterprise legal compliance, open-source attribution, and third-party software IP auditing."
    ),
    "post-release.yml": (
        "Yes. Automates post-release procedures including release branch updates, changelog syncing, milestone tracking, and release "
        "publication notifications. Required to complete the release lifecycle cleanly in an enterprise pipeline."
    ),
    "stale.yml": (
        "No. Upstream issue management bot that automatically marks inactive public issues and PRs as stale and closes them. Enterprise "
        "defect tracking is governed by internal SLAs in Jira or GitHub Projects without arbitrary automated bot closures."
    ),
    "test-internet.yml": (
        "Yes. Executes Node.js network integration test suites requiring live outbound network connectivity (TLS handshakes, DNS "
        "resolution, HTTP/HTTPS client requests). Critical for certifying enterprise releases against real-world networking environments."
    ),
    "timezone-update.yml": (
        "Yes. Automates updating vendored IANA timezone database files (tools/icu/tzdata*.tar.gz). Necessary for ongoing enterprise "
        "release maintenance to ensure accurate temporal calculations, internationalization, and financial transaction timestamp validity."
    ),
    "update-openssl.yml": (
        "Yes. Automates pulling and applying OpenSSL security patches to the vendored cryptographic library. High priority for "
        "enterprise releases to rapidly ingest upstream CVE security fixes and maintain cryptographic standards."
    ),
    "update-v8.yml": (
        "Yes. Automates backporting and applying Google V8 engine bug fixes and security patches. Vital for protecting enterprise "
        "Node.js runtimes against zero-day JIT vulnerabilities and critical JavaScript engine bugs."
    ),
    "author-ready-conflicts.yml": (
        "No. Removes the 'author ready' label from PRs that encounter merge conflicts. Enterprise repositories manage merge conflicts "
        "through branch protection rules, mandatory rebase requirements, and CI status checks rather than label bots."
    ),
    "auto-start-ci.yml": (
        "No. Upstream-specific webhook integration that triggers jobs on the Node.js Foundation's private Jenkins cluster (ci.nodejs.org). "
        "In a forked enterprise repository, all CI runs via GitHub Actions or internal enterprise CI runners, making this hook obsolete."
    ),
    "build-shared.yml": (
        "Yes. Compiles Node.js as a dynamically linked shared library (libnode.so / libnode.dylib / node.dll). Mandatory for enterprise "
        "packaging formats (RPM, DEB) and for embedding Node.js runtimes into enterprise C++ host applications."
    ),
    "close-stalled.yml": (
        "No. Auto-closes community issues waiting for author response after a timeout. Irrelevant for internal enterprise repositories "
        "where issue lifecycle is managed by engineering teams through formal backlog grooming."
    ),
    "comment-labeled.yml": (
        "No. Upstream community bot that posts canned instructions when labels like 'fast-track' or 'tsc-agenda' are applied. Does not "
        "contribute to binary building, testing, or release packaging for an enterprise product."
    ),
    "commit-queue.yml": (
        "No. Upstream landing automation that triggers Jenkins 'node-test-commit' to merge PRs for upstream collaborators. Enterprise "
        "repositories use standard GitHub merge queues or branch protection rules to merge approved changes."
    ),
    "coverage-linux-without-intl.yml": (
        "Yes. Validates and measures test coverage for minimal Node.js builds configured '--without-intl' (omitting ICU). Essential "
        "for enterprise embedded systems, IoT devices, or micro-container base images where binary size must be minimized."
    ),
    "coverage-linux.yml": (
        "Yes. Generates comprehensive C++ and JavaScript test coverage reports (lcov/gcov) on Linux. Indispensable for enterprise "
        "release quality gates to detect untested code paths and satisfy corporate code-coverage compliance mandates."
    ),
    "label-flaky-test-issue.yml": (
        "No. Community issue triage bot that auto-tags reported flaky tests in public issues. In enterprise development, flaky tests "
        "are diagnosed and tracked directly through CI test failure summaries and developer issue boards."
    ),
    "lint-release-proposal.yml": (
        "Yes. Lints release proposal pull requests, verifying version header updates, changelog formatting, and release metadata. "
        "Essential quality gate during release staging to ensure release proposal PRs meet enterprise release standards."
    ),
    "major-release.yml": (
        "Yes. Orchestrates major version promotions, release branch cutoffs, and version deprecations. Required when cutting new "
        "major enterprise releases (e.g. promoting from Node.js 22 to 24) to maintain formal versioning lifecycles."
    ),
    "nix-changes-comment.yml": (
        "No. Posts informational comments on pull requests modifying Nix expression files. Irrelevant for enterprise releases unless "
        "Nix/NixOS is an explicit corporate development standard."
    ),
    "nix-changes.yml": (
        "No. Validates and flags modifications to upstream Nix configuration files. Redundant for enterprise release packaging unless "
        "Nix packages are explicitly targeted for distribution."
    ),
    "notify-on-push.yml": (
        "No. Broadcasts commit pushes to public IRC channels (#node-dev) and upstream Slack. Enterprise releases utilize corporate chat "
        "integrations (Slack/Teams) or native GitHub webhook notifications rather than public IRC bots."
    ),
    "notify-on-review-wanted.yml": (
        "No. Pings upstream GitHub team handles when the 'review-wanted' label is added. Unnecessary for enterprise workflows where "
        "code reviews are assigned via GitHub CODEOWNERS and team review requests."
    )
}


def populate_workbook(src_path: str):
    print(f"Loading {src_path}...")
    wb = openpyxl.load_workbook(src_path)
    ws = wb["nodejs"]

    # Header check / set
    header_cell = ws.cell(1, 33)
    if not header_cell.value:
        header_cell.value = "Do we need this pipeline in forked repo for enterprise release ? Answer with reason"
    header_cell.font = Font(name="Calibri", size=11, bold=True)
    header_cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)

    col_a_ranges = {r.min_row: r.max_row for r in ws.merged_cells.ranges if r.min_col == 1 and r.max_col == 1}

    updated_count = 0
    yes_count = 0
    no_count = 0

    row = 2
    while row <= ws.max_row:
        yaml_name = ws.cell(row, 3).value
        end_row = col_a_ranges.get(row, row)

        if not yaml_name:
            row = end_row + 1
            continue

        yaml_clean = str(yaml_name).strip()
        if yaml_clean in COL_33_DATA:
            answer = COL_33_DATA[yaml_clean]
            if answer.startswith("Yes"):
                yes_count += 1
            else:
                no_count += 1

            top_cell = ws.cell(row=row, column=33)
            top_cell.value = answer
            top_cell.font = Font(name="Calibri", size=11)
            top_cell.alignment = Alignment(vertical="center", wrap_text=True)

            # Clear sub-cells in multi-row blocks
            for sub_r in range(row + 1, end_row + 1):
                sub_cell = ws.cell(row=sub_r, column=33)
                sub_cell.value = None

            # Merge if multi-row
            if end_row > row:
                ws.merge_cells(start_row=row, start_column=33, end_row=end_row, end_column=33)

            updated_count += 1
        else:
            print(f"WARNING: No Column 33 definition for {yaml_clean} (row {row})")

        row = end_row + 1

    print(f"\nPopulated {updated_count} workflows: {yes_count} YES, {no_count} NO.")

    # Save to nodejs_pipeline_result.xlsx (requested file)
    target_nodejs = "workflow-fixes/nodejs_pipeline_result.xlsx"
    wb.save(target_nodejs)
    print(f"Saved: {target_nodejs}")

    # Also save to pipeline_result.xlsx
    target_pipeline = "workflow-fixes/pipeline_result.xlsx"
    wb.save(target_pipeline)
    print(f"Saved: {target_pipeline}")

    # Try saving to node_pipeline_result.xlsx if not write-locked by another process
    target_node = "workflow-fixes/node_pipeline_result.xlsx"
    try:
        wb.save(target_node)
        print(f"Saved: {target_node}")
    except PermissionError:
        print(f"Notice: {target_node} is currently open in another program (e.g. Excel).")
        print(f"Created {target_nodejs} and {target_pipeline} successfully.")

    return updated_count, yes_count, no_count


if __name__ == "__main__":
    populate_workbook("workflow-fixes/node_pipeline_result.xlsx")
