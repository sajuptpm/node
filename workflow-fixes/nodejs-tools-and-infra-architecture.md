# Node.js Architecture: Infrastructure, GitHub Tools & 3P Ecosystem (Original Upstream Before Changes)

> [!NOTE]
> This inventory documents the **exact Infrastructure, GitHub-Native Tools, and Third-Party (3P) Tools** used in the original upstream Node.js CI/CD pipelines **BEFORE any code changes or refactoring**. All entries are verified against the upstream commit `fe40b317efe`.

---

## 1. ⚙️ INFRASTRUCTURE (`INFRA`)

| Infra | Purpose | Evidence in Original Workflow (Before Changes) |
| :--- | :--- | :--- |
| **`ubuntu-slim` (OpenJS Custom Self-Hosted Runners)** | **Lightweight CI/CD Runner Platform** | Hardcoded across **42 upstream workflows** (`runs-on: ubuntu-slim` in `doc.yml`, `linters.yml`, `test-linux.yml`, `build-tarball.yml`, `scorecard.yml`, `codeql.yml`, etc.). |
| **Dedicated Multi-Arch Build Farm (`ci.nodejs.org` Jenkins)** | **Cross-Platform Compilation & Regression Testing** | Invoked in `auto-start-ci.yml` and `commit-queue.yml` via `@node-core/utils` connecting to `https://ci.nodejs.org` across 100+ bare-metal servers (IBM AIX, IBM z/OS s390x, PowerPC ppc64le, SmartOS). |
| **`ubuntu-24.04-arm` (GitHub-Hosted Managed ARM64 Runners)** | **Native AArch64 Testing & Binary Packaging** | Hardcoded in `build-tarball.yml:100`, `coverage-linux.yml:51`, `test-shared.yml:52`, and `notify-on-push.yml:18` (`runs-on: ubuntu-24.04-arm`). |
| **`macos-15` (GitHub-Hosted Apple Silicon macOS Runners)** | **macOS Darwin Build & Test Execution** | Configured in `test-macos.yml:21` (`runs-on: macos-15`). |
| **`windows-2025` (GitHub-Hosted Windows Server Runners)** | **Windows Build & Test Execution** | Configured in `coverage-windows.yml:18` (`runs-on: windows-2025`). |
| **`ubuntu-24.04` / `ubuntu-latest` (Standard GitHub-Hosted Linux)** | **Standard Linux Runner Environment** | Configured in `coverage-linux-without-intl.yml:45` (`ubuntu-24.04`), `linters.yml:16` (`ubuntu-latest`), and `scorecard.yml:27` (`ubuntu-latest`). |
| **Developer Workstation / Developer VM** | **Local Development & Interactive Debugging** | Local developer environments executing `./configure` and `make -j` for manual builds. |
| **Benchmarking Bare-Metal Servers** | **Performance & Latency Testing** | Isolated bare-metal hardware pool used by `benchmark.yml` to minimize virtualization noise during V8/HTTP microbenchmarks. |
| **Public Internet & DNS Test Infrastructure** | **Real-World Network Integration Testing** | Public DNS root servers and live endpoints queried during network socket tests in `test-internet.yml`. |

---

## 2. 🐙 GITHUB TOOLS (`GITHUB TOOLS`)

| Tool | Purpose | Evidence in Original Workflow (Before Changes) |
| :--- | :--- | :--- |
| **Public GitHub Repository (`nodejs/node`)** | **Source Control & Community Collaboration** | Canonical upstream repository hosting source code, pull requests, issue tracker, and discussions. |
| **GitHub Actions** | **CI/CD Workflow Automation** | Upstream execution engine running 45 YAML pipelines in `.github/workflows/*.yml`. |
| **`actions/checkout`** | **Repository Checkout** | `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` across 46 workflow jobs. |
| **`actions/setup-node`** | **Node.js Toolchain Provisioning** | `uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020` across 15 workflow jobs. |
| **`actions/setup-python`** | **Python Runtime Provisioning** | `uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97` across 17 workflow jobs. |
| **`actions/upload-artifact`** | **Artifact Packaging & Storage** | `uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` across 8 workflow jobs. |
| **`actions/download-artifact`** | **Inter-Job Artifact Retrieval** | `uses: actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` across 6 workflow jobs. |
| **`actions/github-script`** | **Octokit GitHub API Scripting** | `uses: actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3` in `commit-lint.yml`, `benchmark.yml`, `build-shared.yml`. |
| **`actions/stale`** | **Stale Issue & PR Triage** | `uses: actions/stale@4391f3da665fdf50b6810c1a66712fb9ba21aa93` in `stale.yml` and `close-stalled.yml`. |
| **`actions/cache`** | **Build & Dependency Caching** | `uses: actions/cache@55cc8345863c7cc4c66a329aec7e433d2d1c52a9` in `update-v8.yml`. |
| **GitHub Secrets** | **Secrets Management** | `secrets.GH_USER_TOKEN`, `secrets.JENKINS_USER`, `secrets.JENKINS_TOKEN`, `secrets.CACHIX_AUTH_TOKEN`, `secrets.CODECOV_TOKEN`, `secrets.SLACK_WEBHOOK`, `secrets.WPT_FYI_PASSWORD`. |
| **GitHub Releases** | **Release Distribution & Tagging** | Official release proposal generation and source tarball uploads in `create-release-proposal.yml`, `major-release.yml`, and `build-tarball.yml`. |
| **GitHub Bot Account (`@nodejs-github-bot`)** | **Automated Commits & PR Creation** | Authenticated via `secrets.GH_USER_TOKEN` across 22 workflows to bypass branch protections and open maintenance PRs. |
| **CodeQL (`github/codeql-action`)** | **Security Scanning (SAST Vulnerabilities)** | `uses: github/codeql-action/init`, `analyze`, `upload-sarif` (`@cdf488f...`) in `codeql.yml` and `scorecard.yml`. |
| **Dependabot** | **Dependency Vulnerability Alerts** | Monitored upstream GitHub Actions dependencies for security advisory notifications. |

---

## 3. 🧩 3P TOOLS & LIBRARIES (`3P TOOLS`)

| Tool | Purpose | Evidence in Original Workflow (Before Changes) |
| :--- | :--- | :--- |
| **Jenkins (`ci.nodejs.org`)** | **Remote Multi-Architecture Build Farm** | `auto-start-ci.yml:65` and `commit-queue.yml:83` invoking `ncu-config set jenkins_token "$JENKINS_TOKEN"` calling `ci.nodejs.org`. |
| **Cachix (`cachix-action`)** | **Managed Nix Binary Caching** | `uses: cachix/cachix-action@5f2d7c5294214f71b873db4b969586b980625e71` pushing to `https://nodejs.cachix.org` with `CACHIX_AUTH_TOKEN`. |
| **Nix (`install-nix-action`)** | **Nix Package Manager Installation** | `uses: cachix/install-nix-action@13d8dd58da0234aa297dedd986986ccb8e7f3e24` in `build-shared.yml`, `benchmark.yml`, `nix-changes.yml`. |
| **Codecov (`codecov-action`)** | **Code Coverage Analysis & PR Reporting** | `uses: codecov/codecov-action@fb8b3582c8e4def4969c97caa2f19720cb33a72f` in `coverage-linux.yml:88` with `CODECOV_TOKEN`. |
| **Slack (`action-slack-notify`)** | **Real-Time Team Alerting** | `uses: rtCamp/action-slack-notify@33ca3be66c6f378fe1610fd1d5258632dbed5e58` in `notify-on-push.yml:32`, `notify-on-review-wanted.yml:25`, `post-release.yml:35`. |
| **Web Platform Tests Dashboard (`wpt.fyi`)** | **Web Standards Compliance Reporting** | `daily-wpt-fyi.yml:162` uploading results to `https://wpt.fyi/api/results/upload` with `WPT_FYI_PASSWORD` and `WPT_FYI_USERNAME`. |
| **StepSecurity Harden-Runner** | **Runner Runtime Security & Egress Monitoring** | `uses: step-security/harden-runner@05e31511f85b41b11d1cf0ef85d0992719546e2c` in `scorecard.yml:39`. |
| **OpenSSF Scorecard** | **Supply Chain Security Auditing** | `uses: ossf/scorecard-action@2d1146689b8cda280b9bc96326124645441f03bc` in `scorecard.yml:45`. |
| **AgentScan (`agentscan.tools`)** | **AI / Bot Contributor Detection** | `uses: MatteoGabriele/agentscan-action@8112fb79b33fafb8506159df20129a34209ac410` calling `https://agentscan.tools` in `contributor-guidance.yml:23`. |
| **Mozilla sccache (`sccache-action`)** | **Distributed C/C++ Compiler Caching** | `uses: Mozilla-Actions/sccache-action@fc920bf0ec8de6ee65d409111f7ec508035751ba` in `build-tarball.yml:123`, `coverage-linux.yml:71`. |
| **`@node-core/utils` CLI** | **Maintainer CI & Release CLI** | `npm install -g @node-core/utils` in `auto-start-ci.yml:58`, `commit-queue.yml:73`, `create-release-proposal.yml:70`. |
| **`peter-evans/create-pull-request`** | **Automated PR Generation** | `uses: peter-evans/create-pull-request@5f6978faf089d4d20b00c7766989d076bb2fc7f1` in `tools.yml:45` and `update-v8.yml:60`. |
| **`gr2m/create-or-update-pull-request-action`** | **Automated Branch/PR Creation** | `uses: gr2m/create-or-update-pull-request-action@b65137ca591da0b9f43bad7b24df13050ea45d1b` in `license-builder.yml:42`, `find-inactive-collaborators.yml:35`. |
| **`mszostok/codeowners-validator`** | **CODEOWNERS Syntax Validation** | `uses: mszostok/codeowners-validator@7f3f5e28c6d7b8dfae5731e54ce2272ca384592f` in `linters.yml:75`. |
| **`nodejs/node-pr-labeler`** | **Subsystem PR Path Labeling** | `uses: nodejs/node-pr-labeler@d4cf1b8b9f23189c37917000e5e17e796c770a6b` in `label-pr.yml:25`. |
| **Clang 19 / LLVM & GCC** | **C/C++ Compilers & Code Generation** | Installed via `.github/actions/install-clang` across `build-tarball.yml`, `coverage-linux.yml`, and `test-linux.yml`. |
| **MSVC Build Tools & Apple Clang** | **Windows & macOS Compilers** | Windows Visual C++ toolchain in `coverage-windows.yml` and Xcode Apple Clang in `test-macos.yml`. |
| **Ninja & GNU Make** | **Build Platform & Compilation Drivers** | `apt-get install -y ninja-build` in `daily.yml` and `make -j` in `test-linux.yml`, `build-tarball.yml`. |
| **Python 3 & GYP (`configure.py`)** | **Build Configuration & Meta-Build** | `python configure.py` and `tools/gyp` generating build files in `test-linux.yml`, `build-tarball.yml`. |
| **Node.js Core Test Runner (`test.py`)** | **Unit & Regression Testing** | `python tools/test.py` executing `parallel`, `sequential`, and `addons` suites in `test-linux.yml`, `coverage-linux.yml`. |
| **Web Platform Tests (WPT Runner)** | **Web Standards Conformance Testing** | Custom WPT harness in `daily-wpt-fyi.yml` and `update-wpt.yml` validating Fetch, Streams, and WebCrypto. |
| **Google Perfetto** | **System Tracing & APM Telemetry** | Low-level tracing instrumentation compiled and verified in `test-linux-perfetto.yml`. |
| **ngtcp2 & nghttp3** | **QUIC & HTTP/3 Protocol Testing** | Vendored HTTP/3 transport protocol libraries tested in `test-linux-quic.yml`. |
| **Google V8 Engine** | **JavaScript & WebAssembly JIT Engine** | Core runtime engine in `deps/v8`, updated via `update-v8.yml`. |
| **OpenSSL 3.x** | **Cryptography & TLS Security Provider** | Embedded crypto engine in `deps/openssl`, updated via `update-openssl.yml`. |
| **libuv** | **Asynchronous I/O & Event Loop** | Core asynchronous event loop in `deps/uv`. |
| **ESLint & Prettier** | **JavaScript Linting & Formatting** | Executed in `linters.yml` via `make lint-js`. |
| **clang-format & cpplint** | **C++ Linting & Style Checking** | Executed in `linters.yml` via `make lint-cpp`. |
| **flake8 / pyflakes** | **Python Linting** | Executed in `linters.yml` via `make lint-py`. |
| **gcovr / lcov** | **Code Coverage Instrumentation** | `pip install gcovr==7.2` in `coverage-linux.yml` and `coverage-linux-without-intl.yml`. |
| **license-builder / check-licenses** | **License & Legal Attribution Generator** | Executed in `license-builder.yml` via `tools/actions/check-licenses`. |
| **Node Benchmark Suite (`benchmark/`)** | **Performance Micro-benchmarking** | Executed in `benchmark.yml` running microbenchmarks against V8, HTTP, and Streams. |
