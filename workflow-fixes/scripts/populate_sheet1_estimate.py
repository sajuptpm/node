import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load the workbook
wb_path = 'workflow-fixes/infra_tool_estimate.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['Sheet1']

# Clear existing rows below header
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    for cell in row:
        cell.value = None

# Define the comprehensive dataset for component nodejs
# Columns: ['Component', 'Pipeline', 'Description', 'Category', 'Mandatory', 'Infra', 'Cost basis', 'Yearly Cost']

data = [
    # 1. author-ready-conflicts.yml
    ('nodejs', 'author-ready-conflicts.yml',
     'Triage automation that checks pull requests with "author-ready" label for merge conflicts against target branch, removing label when conflicts exist.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'author-ready-conflicts.yml',
     'Triage automation that checks pull requests with "author-ready" label for merge conflicts against target branch, removing label when conflicts exist.',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 2. auto-start-ci.yml
    ('nodejs', 'auto-start-ci.yml',
     'Automated trigger pipeline that contacts the private OpenJS Foundation Jenkins cluster (ci.nodejs.org) to launch remote cross-platform CI matrix builds.',
     'Internal to Vendor', 'No', 'OpenJS Jenkins Build Farm (ci.nodejs.org)',
     'OpenJS managed cluster: ~$3,000–$10,000/month', '$36,000–$120,000'),
    ('nodejs', 'auto-start-ci.yml',
     'Automated trigger pipeline that contacts the private OpenJS Foundation Jenkins cluster (ci.nodejs.org) to launch remote cross-platform CI matrix builds.',
     'Internal to Vendor', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'auto-start-ci.yml',
     'Automated trigger pipeline that contacts the private OpenJS Foundation Jenkins cluster (ci.nodejs.org) to launch remote cross-platform CI matrix builds.',
     'Internal to Vendor', 'No', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 3. benchmark.yml
    ('nodejs', 'benchmark.yml',
     'Comprehensive performance micro-benchmark suite measuring throughput, ops/sec, and latency across Buffer, HTTP, Crypto, and Event Loop subsystems.',
     'Test', 'No', 'Bare-Metal Benchmark Server Pool',
     'Physical servers / Dedicated VM: ~$200–$500/month', '$2,400–$6,000'),
    ('nodejs', 'benchmark.yml',
     'Comprehensive performance micro-benchmark suite measuring throughput, ops/sec, and latency across Buffer, HTTP, Crypto, and Event Loop subsystems.',
     'Test', 'No', 'Managed ARM64 Runners (ubuntu-24.04-arm)',
     'PAYG GitHub ARM Runners: $0.005–$0.010/minute', '$144'),
    ('nodejs', 'benchmark.yml',
     'Comprehensive performance micro-benchmark suite measuring throughput, ops/sec, and latency across Buffer, HTTP, Crypto, and Event Loop subsystems.',
     'Test', 'No', 'Standard GitHub macOS Runners (macos-latest / macos-15)',
     'Usage-based (Free on public repos; $0.064–$0.080/min private)', '$0'),
    ('nodejs', 'benchmark.yml',
     'Comprehensive performance micro-benchmark suite measuring throughput, ops/sec, and latency across Buffer, HTTP, Crypto, and Event Loop subsystems.',
     'Test', 'No', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),
    ('nodejs', 'benchmark.yml',
     'Comprehensive performance micro-benchmark suite measuring throughput, ops/sec, and latency across Buffer, HTTP, Crypto, and Event Loop subsystems.',
     'Test', 'No', 'Cachix Nix Binary Cache (nodejs.cachix.org)',
     'Pro ~$40/month (200 GB) to Team ~$200/month (1 TB)', '$480–$2,400'),
    ('nodejs', 'benchmark.yml',
     'Comprehensive performance micro-benchmark suite measuring throughput, ops/sec, and latency across Buffer, HTTP, Crypto, and Event Loop subsystems.',
     'Test', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),

    # 4. build-shared.yml
    ('nodejs', 'build-shared.yml',
     'Reusable workflow compiling Node.js dynamically linked against system-installed shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Build', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'build-shared.yml',
     'Reusable workflow compiling Node.js dynamically linked against system-installed shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Build', 'Yes', 'Standard GitHub macOS Runners (macos-latest / macos-15)',
     'Usage-based (Free on public repos; $0.064–$0.080/min private)', '$0'),
    ('nodejs', 'build-shared.yml',
     'Reusable workflow compiling Node.js dynamically linked against system-installed shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Build', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),
    ('nodejs', 'build-shared.yml',
     'Reusable workflow compiling Node.js dynamically linked against system-installed shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Build', 'Yes', 'Cachix Nix Binary Cache (nodejs.cachix.org)',
     'Pro ~$40/month (200 GB) to Team ~$200/month (1 TB)', '$480–$2,400'),

    # 5. build-tarball.yml
    ('nodejs', 'build-tarball.yml',
     'Generates the canonical node-vX.Y.Z.tar.gz source release tarball and verifies full release compilation and packaging across Linux x86 and ARM64.',
     'Package', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'build-tarball.yml',
     'Generates the canonical node-vX.Y.Z.tar.gz source release tarball and verifies full release compilation and packaging across Linux x86 and ARM64.',
     'Package', 'Yes', 'Managed ARM64 Runners (ubuntu-24.04-arm)',
     'PAYG GitHub ARM Runners: $0.005–$0.010/minute', '$144'),
    ('nodejs', 'build-tarball.yml',
     'Generates the canonical node-vX.Y.Z.tar.gz source release tarball and verifies full release compilation and packaging across Linux x86 and ARM64.',
     'Package', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),
    ('nodejs', 'build-tarball.yml',
     'Generates the canonical node-vX.Y.Z.tar.gz source release tarball and verifies full release compilation and packaging across Linux x86 and ARM64.',
     'Package', 'Yes', 'Codecov Coverage Platform (codecov-action)',
     'Free for public OSS repos ($0); $12/user/month private', '$0'),

    # 6. close-stalled.yml
    ('nodejs', 'close-stalled.yml',
     'Repository housekeeping automation that periodically reviews inactive pull requests and issues, applying stalled labels and closing abandoned threads.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'close-stalled.yml',
     'Repository housekeeping automation that periodically reviews inactive pull requests and issues, applying stalled labels and closing abandoned threads.',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 7. codeql.yml
    ('nodejs', 'codeql.yml',
     'Static Application Security Testing (SAST) analyzing C/C++ engine internals and JavaScript libraries for vulnerabilities, taint tracking, and CWE compliance.',
     'Security', 'Yes', 'GitHub Advanced Security (GHAS) / CodeQL',
     'Free for public OSS repos ($0); $49/active committer/month private', '$0'),
    ('nodejs', 'codeql.yml',
     'Static Application Security Testing (SAST) analyzing C/C++ engine internals and JavaScript libraries for vulnerabilities, taint tracking, and CWE compliance.',
     'Security', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'codeql.yml',
     'Static Application Security Testing (SAST) analyzing C/C++ engine internals and JavaScript libraries for vulnerabilities, taint tracking, and CWE compliance.',
     'Security', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 8. comment-labeled.yml
    ('nodejs', 'comment-labeled.yml',
     'Automated workflow posting standard governance and policy explanations on pull requests when specific labels (e.g. semver-major, fast-track) are applied.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'comment-labeled.yml',
     'Automated workflow posting standard governance and policy explanations on pull requests when specific labels (e.g. semver-major, fast-track) are applied.',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 9. commit-lint.yml
    ('nodejs', 'commit-lint.yml',
     'Validates PR commit messages against Node.js guidelines, verifying subsystem tags, character line limits, and DCO Signed-off-by attestation.',
     'Test', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'commit-lint.yml',
     'Validates PR commit messages against Node.js guidelines, verifying subsystem tags, character line limits, and DCO Signed-off-by attestation.',
     'Test', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 10. commit-queue.yml
    ('nodejs', 'commit-queue.yml',
     'Automated PR merge bot that verifies approvals, queries Jenkins CI REST API to check test results, rebases PR branch, and lands commits onto main.',
     'Internal to Vendor', 'No', 'OpenJS Jenkins Build Farm (ci.nodejs.org)',
     'OpenJS managed cluster: ~$3,000–$10,000/month', '$36,000–$120,000'),
    ('nodejs', 'commit-queue.yml',
     'Automated PR merge bot that verifies approvals, queries Jenkins CI REST API to check test results, rebases PR branch, and lands commits onto main.',
     'Internal to Vendor', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'commit-queue.yml',
     'Automated PR merge bot that verifies approvals, queries Jenkins CI REST API to check test results, rebases PR branch, and lands commits onto main.',
     'Internal to Vendor', 'No', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 11. contributor-guidance.yml
    ('nodejs', 'contributor-guidance.yml',
     'Analyzes incoming pull requests from external contributors, evaluating AI spam detection via AgentScan and directing contributors on Jenkins CI requirements.',
     'Internal to Vendor', 'No', 'AgentScan PR Bot Scanner',
     'Community tier ($0); $19–$99/month commercial plan', '$0'),
    ('nodejs', 'contributor-guidance.yml',
     'Analyzes incoming pull requests from external contributors, evaluating AI spam detection via AgentScan and directing contributors on Jenkins CI requirements.',
     'Internal to Vendor', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'contributor-guidance.yml',
     'Analyzes incoming pull requests from external contributors, evaluating AI spam detection via AgentScan and directing contributors on Jenkins CI requirements.',
     'Internal to Vendor', 'No', 'OpenJS Jenkins Build Farm (ci.nodejs.org)',
     'OpenJS managed cluster: ~$3,000–$10,000/month', '$36,000–$120,000'),

    # 12. coverage-linux-without-intl.yml
    ('nodejs', 'coverage-linux-without-intl.yml',
     'Compiles Node.js without International Components for Unicode (ICU) and executes full test suite under gcov/lcov instrumentation to track code coverage.',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'coverage-linux-without-intl.yml',
     'Compiles Node.js without International Components for Unicode (ICU) and executes full test suite under gcov/lcov instrumentation to track code coverage.',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),
    ('nodejs', 'coverage-linux-without-intl.yml',
     'Compiles Node.js without International Components for Unicode (ICU) and executes full test suite under gcov/lcov instrumentation to track code coverage.',
     'Test', 'Yes', 'Codecov Coverage Platform (codecov-action)',
     'Free for public OSS repos ($0); $12/user/month private', '$0'),

    # 13. coverage-linux.yml
    ('nodejs', 'coverage-linux.yml',
     'Full Linux code coverage pipeline compiling Node.js with gcov, running parallel/sequential test suites, and publishing coverage metrics to Codecov.',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'coverage-linux.yml',
     'Full Linux code coverage pipeline compiling Node.js with gcov, running parallel/sequential test suites, and publishing coverage metrics to Codecov.',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),
    ('nodejs', 'coverage-linux.yml',
     'Full Linux code coverage pipeline compiling Node.js with gcov, running parallel/sequential test suites, and publishing coverage metrics to Codecov.',
     'Test', 'Yes', 'Codecov Coverage Platform (codecov-action)',
     'Free for public OSS repos ($0); $12/user/month private', '$0'),

    # 14. coverage-windows.yml
    ('nodejs', 'coverage-windows.yml',
     'Windows test coverage workflow compiling Node.js with MSVC, executing Windows-specific test suites, and aggregating platform code coverage.',
     'Test', 'Yes', 'Standard GitHub Windows Runners (windows-2022 / windows-latest)',
     'Usage-based (Free on public repos; $0.016/min private)', '$0'),
    ('nodejs', 'coverage-windows.yml',
     'Windows test coverage workflow compiling Node.js with MSVC, executing Windows-specific test suites, and aggregating platform code coverage.',
     'Test', 'Yes', 'Codecov Coverage Platform (codecov-action)',
     'Free for public OSS repos ($0); $12/user/month private', '$0'),

    # 15. create-release-proposal.yml
    ('nodejs', 'create-release-proposal.yml',
     'Automates release staging by assembling changelogs, cherry-picking release commits onto staging branches, bumping version numbers, and opening release proposal PRs.',
     'Release', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'create-release-proposal.yml',
     'Automates release staging by assembling changelogs, cherry-picking release commits onto staging branches, bumping version numbers, and opening release proposal PRs.',
     'Release', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 16. daily-wpt-fyi.yml
    ('nodejs', 'daily-wpt-fyi.yml',
     'Scheduled W3C Web Platform Tests conformance pipeline running WPT suites and submitting test run results to the external wpt.fyi dashboard.',
     'Test', 'No', 'Web Platform Tests API (wpt.fyi)',
     'Consortium-sponsored upload API ($0)', '$0'),
    ('nodejs', 'daily-wpt-fyi.yml',
     'Scheduled W3C Web Platform Tests conformance pipeline running WPT suites and submitting test run results to the external wpt.fyi dashboard.',
     'Test', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'daily-wpt-fyi.yml',
     'Scheduled W3C Web Platform Tests conformance pipeline running WPT suites and submitting test run results to the external wpt.fyi dashboard.',
     'Test', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 17. daily.yml
    ('nodejs', 'daily.yml',
     'Scheduled nocturnal integration pipeline triggering master branch build verification and upstream synchronization tests.',
     'Build', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 18. doc.yml
    ('nodejs', 'doc.yml',
     'Compiles official Node.js API HTML and JSON documentation, lints markdown files, verifies anchor links, and uploads documentation distribution packages.',
     'Release Doc', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'doc.yml',
     'Compiles official Node.js API HTML and JSON documentation, lints markdown files, verifies anchor links, and uploads documentation distribution packages.',
     'Release Doc', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 19. find-inactive-collaborators.yml
    ('nodejs', 'find-inactive-collaborators.yml',
     'Project governance audit script reviewing repository commit, issue, and review history to identify inactive OpenJS collaborators.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'find-inactive-collaborators.yml',
     'Project governance audit script reviewing repository commit, issue, and review history to identify inactive OpenJS collaborators.',
     'Utility', 'No', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 20. find-inactive-tsc.yml
    ('nodejs', 'find-inactive-tsc.yml',
     'Project governance audit monitoring voting participation and repository engagement for Technical Steering Committee members.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'find-inactive-tsc.yml',
     'Project governance audit monitoring voting participation and repository engagement for Technical Steering Committee members.',
     'Utility', 'No', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 21. label-flaky-test-issue.yml
    ('nodejs', 'label-flaky-test-issue.yml',
     'Triage bot automatically applying flaky-test labels to GitHub issues opened with test failure templates.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'label-flaky-test-issue.yml',
     'Triage bot automatically applying flaky-test labels to GitHub issues opened with test failure templates.',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 22. label-pr.yml
    ('nodejs', 'label-pr.yml',
     'Triage bot analyzing changed file paths in pull requests and applying subsystem labels (e.g. crypto, fs, net, doc, stream).',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'label-pr.yml',
     'Triage bot analyzing changed file paths in pull requests and applying subsystem labels (e.g. crypto, fs, net, doc, stream).',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 23. license-builder.yml
    ('nodejs', 'license-builder.yml',
     'Audits all vendored third-party dependencies in deps/, verifies open-source licenses, and generates the canonical project LICENSE file.',
     'Package', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'license-builder.yml',
     'Audits all vendored third-party dependencies in deps/, verifies open-source licenses, and generates the canonical project LICENSE file.',
     'Package', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 24. lint-release-proposal.yml
    ('nodejs', 'lint-release-proposal.yml',
     'Release quality gate verifying changelog syntax, commit SHA references, and SemVer version declarations in release staging pull requests.',
     'Release', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'lint-release-proposal.yml',
     'Release quality gate verifying changelog syntax, commit SHA references, and SemVer version declarations in release staging pull requests.',
     'Release', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 25. linters.yml
    ('nodejs', 'linters.yml',
     'Core static code analysis matrix running ESLint for JavaScript, clang-format and cpplint for C++, yamllint for GitHub Actions, and remark for Markdown.',
     'Test', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'linters.yml',
     'Core static code analysis matrix running ESLint for JavaScript, clang-format and cpplint for C++, yamllint for GitHub Actions, and remark for Markdown.',
     'Test', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 26. major-release.yml
    ('nodejs', 'major-release.yml',
     'Prepares major Node.js releases, generating new staging release branches (e.g. v24.x-staging), updating upstream V8 branches, and configuring milestone metadata.',
     'Release', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'major-release.yml',
     'Prepares major Node.js releases, generating new staging release branches (e.g. v24.x-staging), updating upstream V8 branches, and configuring milestone metadata.',
     'Release', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 27. nix-changes-comment.yml
    ('nodejs', 'nix-changes-comment.yml',
     'Automated PR commenting workflow providing status and instructions whenever pull requests modify Nix packaging configurations in tools/nix/.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'nix-changes-comment.yml',
     'Automated PR commenting workflow providing status and instructions whenever pull requests modify Nix packaging configurations in tools/nix/.',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 28. nix-changes.yml
    ('nodejs', 'nix-changes.yml',
     'Builds and evaluates Nix derivations for modified files in tools/nix/, pushing pre-built binary derivations to Cachix (nodejs.cachix.org).',
     'Test', 'No', 'Cachix Nix Binary Cache (nodejs.cachix.org)',
     'Pro ~$40/month (200 GB) to Team ~$200/month (1 TB)', '$480–$2,400'),
    ('nodejs', 'nix-changes.yml',
     'Builds and evaluates Nix derivations for modified files in tools/nix/, pushing pre-built binary derivations to Cachix (nodejs.cachix.org).',
     'Test', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),

    # 29. notify-on-push.yml
    ('nodejs', 'notify-on-push.yml',
     'Monitors git push events on main, detecting force-pushes or commit message policy violations and dispatching alerts to the Node.js team Slack channel.',
     'Internal to Vendor', 'No', 'Slack Enterprise Messaging (action-slack-notify)',
     'SaaS messaging seat: ~$7–$25/user/month', '$84–$300'),
    ('nodejs', 'notify-on-push.yml',
     'Monitors git push events on main, detecting force-pushes or commit message policy violations and dispatching alerts to the Node.js team Slack channel.',
     'Internal to Vendor', 'No', 'Managed ARM64 Runners (ubuntu-24.04-arm)',
     'PAYG GitHub ARM Runners: $0.005–$0.010/minute', '$144'),

    # 30. notify-on-review-wanted.yml
    ('nodejs', 'notify-on-review-wanted.yml',
     'Monitors PR label events, alerting the Node.js core maintainers Slack channel when PRs are tagged with "review wanted" or "author-ready".',
     'Internal to Vendor', 'No', 'Slack Enterprise Messaging (action-slack-notify)',
     'SaaS messaging seat: ~$7–$25/user/month', '$84–$300'),
    ('nodejs', 'notify-on-review-wanted.yml',
     'Monitors PR label events, alerting the Node.js core maintainers Slack channel when PRs are tagged with "review wanted" or "author-ready".',
     'Internal to Vendor', 'No', 'Managed ARM64 Runners (ubuntu-24.04-arm)',
     'PAYG GitHub ARM Runners: $0.005–$0.010/minute', '$144'),

    # 31. post-release.yml
    ('nodejs', 'post-release.yml',
     'Executes post-release administrative actions, applying release git tags, publishing GitHub releases, and promoting compiled assets to release mirrors.',
     'Release', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'post-release.yml',
     'Executes post-release administrative actions, applying release git tags, publishing GitHub releases, and promoting compiled assets to release mirrors.',
     'Release', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 32. scorecard.yml
    ('nodejs', 'scorecard.yml',
     'OpenSSF Scorecard automated security audit verifying software supply-chain integrity, branch protections, token permissions, and dependency pinning.',
     'Security', 'Yes', 'StepSecurity Harden-Runner',
     'Free community tier for public OSS ($0); $10–$20/dev/month private', '$0'),
    ('nodejs', 'scorecard.yml',
     'OpenSSF Scorecard automated security audit verifying software supply-chain integrity, branch protections, token permissions, and dependency pinning.',
     'Security', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'scorecard.yml',
     'OpenSSF Scorecard automated security audit verifying software supply-chain integrity, branch protections, token permissions, and dependency pinning.',
     'Security', 'Yes', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 33. stale.yml
    ('nodejs', 'stale.yml',
     'Automated lifecycle management closing inactive issues and pull requests after defined periods of inactivity to maintain repository hygiene.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'stale.yml',
     'Automated lifecycle management closing inactive issues and pull requests after defined periods of inactivity to maintain repository hygiene.',
     'Utility', 'No', 'Standard GitHub-Hosted Runners (ubuntu-latest)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),

    # 34. stress-test.yml
    ('nodejs', 'stress-test.yml',
     'Executes designated flaky or concurrency-sensitive unit tests across hundreds of repetitions to detect timing bugs and race conditions.',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'stress-test.yml',
     'Executes designated flaky or concurrency-sensitive unit tests across hundreds of repetitions to detect timing bugs and race conditions.',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 35. test-internet.yml
    ('nodejs', 'test-internet.yml',
     'Integration test suite verifying networking features requiring live internet access (e.g. real DNS lookups, TLS root store verification, HTTP client).',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'test-internet.yml',
     'Integration test suite verifying networking features requiring live internet access (e.g. real DNS lookups, TLS root store verification, HTTP client).',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 36. test-linux-perfetto.yml
    ('nodejs', 'test-linux-perfetto.yml',
     'Builds Node.js with Google Perfetto tracing support and executes trace event verification suites to ensure kernel/userspace profiling works correctly.',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'test-linux-perfetto.yml',
     'Builds Node.js with Google Perfetto tracing support and executes trace event verification suites to ensure kernel/userspace profiling works correctly.',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 37. test-linux-quic.yml
    ('nodejs', 'test-linux-quic.yml',
     'Builds Node.js with experimental QUIC (ngtcp2 / nghttp3) support and executes UDP connection multiplexing and HTTP/3 transport test suites.',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'test-linux-quic.yml',
     'Builds Node.js with experimental QUIC (ngtcp2 / nghttp3) support and executes UDP connection multiplexing and HTTP/3 transport test suites.',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 38. test-linux.yml
    ('nodejs', 'test-linux.yml',
     'Primary Linux CI test pipeline compiling Node.js with GCC/Clang and running parallel, sequential, message, and C++ addon test suites.',
     'Build', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'test-linux.yml',
     'Primary Linux CI test pipeline compiling Node.js with GCC/Clang and running parallel, sequential, message, and C++ addon test suites.',
     'Build', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 39. test-macos.yml
    ('nodejs', 'test-macos.yml',
     'Primary macOS CI test pipeline compiling Node.js with Apple Clang and executing the standard test harness across Intel and Apple Silicon runners.',
     'Build', 'Yes', 'Standard GitHub macOS Runners (macos-latest / macos-15)',
     'Usage-based (Free on public repos; $0.064–$0.080/min private)', '$0'),
    ('nodejs', 'test-macos.yml',
     'Primary macOS CI test pipeline compiling Node.js with Apple Clang and executing the standard test harness across Intel and Apple Silicon runners.',
     'Build', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 40. test-shared.yml
    ('nodejs', 'test-shared.yml',
     'Comprehensive matrix testing Node.js against dynamically linked system shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Test', 'Yes', 'Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)',
     'Usage-based (Free on public repos; $0.008/min private)', '$0'),
    ('nodejs', 'test-shared.yml',
     'Comprehensive matrix testing Node.js against dynamically linked system shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Test', 'Yes', 'Managed ARM64 Runners (ubuntu-24.04-arm)',
     'PAYG GitHub ARM Runners: $0.005–$0.010/minute', '$144'),
    ('nodejs', 'test-shared.yml',
     'Comprehensive matrix testing Node.js against dynamically linked system shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Test', 'Yes', 'Standard GitHub macOS Runners (macos-latest / macos-15)',
     'Usage-based (Free on public repos; $0.064–$0.080/min private)', '$0'),
    ('nodejs', 'test-shared.yml',
     'Comprehensive matrix testing Node.js against dynamically linked system shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Test', 'Yes', 'Cachix Nix Binary Cache (nodejs.cachix.org)',
     'Pro ~$40/month (200 GB) to Team ~$200/month (1 TB)', '$480–$2,400'),
    ('nodejs', 'test-shared.yml',
     'Comprehensive matrix testing Node.js against dynamically linked system shared libraries (OpenSSL, zlib, libuv, nghttp2) across Linux and macOS.',
     'Test', 'Yes', 'Mozilla sccache Cloud Storage',
     'Object storage & cache: ~$5–$10/month (~100 GB active cache)', '$120'),

    # 41. timezone-update.yml
    ('nodejs', 'timezone-update.yml',
     'Automated maintenance updater that periodically fetches the latest IANA timezone database releases, updates ICU data, and opens PRs.',
     'Utility', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'timezone-update.yml',
     'Automated maintenance updater that periodically fetches the latest IANA timezone database releases, updates ICU data, and opens PRs.',
     'Utility', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 42. tools.yml
    ('nodejs', 'tools.yml',
     'Automated dependency updater checking for new versions of vendored ecosystem dependencies (npm, undici, amaro, acorn, simdjson) and preparing update PRs.',
     'Utility', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'tools.yml',
     'Automated dependency updater checking for new versions of vendored ecosystem dependencies (npm, undici, amaro, acorn, simdjson) and preparing update PRs.',
     'Utility', 'Yes', 'Cachix Nix Binary Cache (nodejs.cachix.org)',
     'Pro ~$40/month (200 GB) to Team ~$200/month (1 TB)', '$480–$2,400'),
    ('nodejs', 'tools.yml',
     'Automated dependency updater checking for new versions of vendored ecosystem dependencies (npm, undici, amaro, acorn, simdjson) and preparing update PRs.',
     'Utility', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 43. update-openssl.yml
    ('nodejs', 'update-openssl.yml',
     'Automated OpenSSL security patch updater that tracks OpenSSL 3.x releases, imports new crypto sources, applies Node.js custom patches, and creates update PRs.',
     'Utility', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'update-openssl.yml',
     'Automated OpenSSL security patch updater that tracks OpenSSL 3.x releases, imports new crypto sources, applies Node.js custom patches, and creates update PRs.',
     'Utility', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 44. update-v8.yml
    ('nodejs', 'update-v8.yml',
     'Automated Google V8 engine synchronizer fetching patch releases from Chromium V8 branches, regenerating GYP build files, and opening update PRs.',
     'Utility', 'Yes', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'update-v8.yml',
     'Automated Google V8 engine synchronizer fetching patch releases from Chromium V8 branches, regenerating GYP build files, and opening update PRs.',
     'Utility', 'Yes', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),

    # 45. update-wpt.yml
    ('nodejs', 'update-wpt.yml',
     'Synchronizes the in-tree Web Platform Tests (WPT) fixtures with upstream W3C wpt git repository and triggers upstream validation.',
     'Utility', 'No', 'OpenJS Jenkins Build Farm (ci.nodejs.org)',
     'OpenJS managed cluster: ~$3,000–$10,000/month', '$36,000–$120,000'),
    ('nodejs', 'update-wpt.yml',
     'Synchronizes the in-tree Web Platform Tests (WPT) fixtures with upstream W3C wpt git repository and triggers upstream validation.',
     'Utility', 'No', 'OpenJS Custom Runners (ubuntu-slim)',
     'Dedicated self-hosted VM pool: ~$500–$2,500/month', '$6,000–$30,000'),
    ('nodejs', 'update-wpt.yml',
     'Synchronizes the in-tree Web Platform Tests (WPT) fixtures with upstream W3C wpt git repository and triggers upstream validation.',
     'Utility', 'No', 'Bot Collaborator User Seat (GH_USER_TOKEN)',
     'GitHub Enterprise User Seat: ~$21/month', '$252'),
]

# Write data to Sheet1
for row_idx, row_data in enumerate(data, start=2):
    for col_idx, val in enumerate(row_data, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)

print(f"Successfully populated {len(data)} rows in Sheet1.")

# Apply styling to Sheet1
header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

# Header formatting
for col in range(1, 9):
    c = ws.cell(row=1, column=col)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Data row formatting
alt_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

for r in range(2, len(data) + 2):
    is_alt = (r % 2 == 1)
    for c in range(1, 9):
        cell = ws.cell(row=r, column=c)
        cell.border = thin_border
        if is_alt:
            cell.fill = alt_fill
        # Alignments
        if c in (1, 4, 5): # Component, Category, Mandatory
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c in (2, 6, 7, 8): # Pipeline, Infra, Cost basis, Yearly Cost
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else: # Description
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

# Auto-adjust column widths
col_widths = {
    1: 14, # Component
    2: 30, # Pipeline
    3: 50, # Description
    4: 18, # Category
    5: 14, # Mandatory
    6: 42, # Infra
    7: 42, # Cost basis
    8: 24  # Yearly Cost
}

for col_idx, width in col_widths.items():
    ws.column_dimensions[get_column_letter(col_idx)].width = width

ws.row_dimensions[1].height = 28

# Save workbook
wb.save(wb_path)
print(f"Workbook successfully saved to {wb_path}.")
