# Node.js Architecture: Infrastructure, GitHub Tools & 3P Ecosystem

This document provides a comprehensive mapping of the **Infrastructure**, **GitHub-Native Tools**, and **Third-Party (3P) Tools & Libraries** powering the Node.js open-source project and its modernized CI/CD pipelines, directly mirroring the architectural model used in modern cloud-native systems.

---

## 1. INFRASTRUCTURE (`INFRA`)

| Infra | Purpose | Role in Node.js Project |
| :--- | :--- | :--- |
| **GitHub-Hosted Runners (Linux, macOS, Windows)** | Standard CI/CD & Matrix Builds | Executes multi-platform compilation, unit tests, linters, and documentation builds on `ubuntu-latest`, `windows-2025`, and `macos-15`. |
| **Dedicated Multi-Arch Build Farm (`ci.nodejs.org` Jenkins)** | Exotic Architecture Testing | Upstream OpenJS Foundation cluster of 100+ bare-metal servers testing IBM AIX, IBM z/OS (s390x), PowerPC (ppc64le), and SmartOS. |
| **Self-Hosted ARM64 Runners / Managed ARM64** | Native AArch64 Testing & Packaging | Compiles native 64-bit ARM binaries and validates V8 JIT code generation directly on ARM hardware (AWS Graviton, Apple Silicon, Ampere). |
| **Developer Workstation / Developer VM** | Development & Debugging | Local engineer environments for source code authoring, local `./configure && make -j` compilation, and C++/JS debugging. |
| **Benchmarking Bare-Metal Servers** | Performance & Latency Testing | Dedicated, quiet hardware machines without shared virtualization noise for running micro-benchmarks against V8, HTTP, and Streams. |
| **Public Internet & DNS Test Infrastructure** | Real-World Network Testing | Public DNS root servers and live HTTPS endpoints used by `test-internet.yml` to validate live socket and TLS handshakes. |

---

## 2. GITHUB TOOLS (`GITHUB TOOLS`)

| Tool | Purpose | Role in Node.js Project |
| :--- | :--- | :--- |
| **Public GitHub Repository** | Source Control & Issue Triage | Hosts the canonical git repository, issue tracker, pull requests, and collaborator discussions. |
| **GitHub Actions** | CI/CD & Automated Release Pipelines | Orchestrates all 45 automated workflows for linting, compilation, testing, security scanning, and release staging. |
| **GitHub Releases** | Release Management & Asset Distribution | Distributes official production binaries, source archives (`node-vX.Y.Z.tar.gz`), release notes, and SHA256 checksums. |
| **GitHub Container Registry (GHCR)** | Container & Package Registry | Stores and distributes official development container base images, devcontainers, and release containers. |
| **Dependabot** | Dependency Management (Vulnerabilities) | Automated monitoring and bump pull requests for GitHub Actions dependencies and development tools. |
| **CodeQL** | Security Scanning (SAST Vulnerabilities) | Semantic static code analysis detecting Common Weakness Enumerations (CWEs), memory safety flaws, and taint tracking in C/C++ and JS. |
| **GitHub Secrets** | Secrets Management | Securely stores sensitive tokens (`GITHUB_TOKEN`, signing certificates, release webhooks) without exposing them in code. |
| **GitHub Actions Artifacts** | Artifact Storage & Archiving | Stores build tarballs, shared libraries (`libnode.so`), coverage reports, test failure logs, and generated HTML/JSON documentation. |
| **GitHub Step Summaries** | Build Summaries & Observability | Renders inline markdown test summaries, coverage cards, security alerts, and notification reports directly on GitHub run pages. |
| **GitHub Pages / Doc Tools** | Official API Documentation | Formats and serves official Node.js API documentation and HTML/JSON reference manuals generated from `tools/doc`. |

---

## 3. THIRD-PARTY TOOLS & LIBRARIES (`3P TOOLS`)

| Tool | Purpose | Role in Node.js Project |
| :--- | :--- | :--- |
| **Clang / LLVM 19 & GCC** | C/C++ Compilers & Code Generation | Primary compilers used across Linux and macOS to compile Node.js, V8, and native C++ addons. |
| **MSVC Build Tools & Apple Clang** | Platform-Native Compilers | Compiles native Windows binaries (`node.exe`, Win32 IOCP) and macOS Darwin binaries (Apple Silicon / Intel). |
| **Ninja & GNU Make** | Parallel Build Generation & Execution | High-speed parallel build systems orchestrating multi-core C++ compilation. |
| **Python 3 & `configure.py` / GYP** | Build Configuration & Meta-Build Orchestration | `configure.py` inspects system flags and generates Ninja/Makefile configurations via GYP (`tools/gyp`). |
| **Node.js Core Test Harness (`test.py`)** | Unit, Parallel & Sequential Testing | Custom Python test runner executing thousands of parallel, sequential, message, and native addon test suites (`test/`). |
| **Web Platform Tests (WPT Runner)** | Conformance & Standards Testing | W3C cross-browser test runner validating compliance for Fetch, Streams, URL, WebCrypto, and WebSockets. |
| **Google Perfetto** | System Tracing & APM Telemetry | Low-level kernel tracing and performance instrumentation for production application profiling. |
| **ngtcp2 & nghttp3** | QUIC & HTTP/3 Protocol Testing | Native transport protocol libraries and test suites validating HTTP/3 networking. |
| **Google V8 Engine** | JavaScript & WebAssembly Engine | High-performance Google JavaScript engine compiling JS to machine code with TurboFan and Sparkplug JIT. |
| **OpenSSL 3.x** | Cryptography & Security Provider | Cryptographic core implementing TLS 1.3, X.509 certificates, crypto primitives, and FIPS compliance. |
| **libuv** | Asynchronous I/O & Event Loop | Multi-platform support library providing the asynchronous event loop, thread pool, file system I/O, and sockets. |
| **ESLint & Prettier** | Code Quality (JavaScript Linting) | Static AST-based linter enforcing JavaScript formatting, syntax standards, and security rules across core and tools. |
| **clang-format & cpplint** | Code Quality (C++ Linting) | Google style guide checker and automated formatting tool for all C/C++ header and source files (`src/`). |
| **flake8 / pyflakes** | Code Quality (Python Linting) | Enforces PEP8 compliance and syntax validity across build scripts, doc generators, and test runners. |
| **OpenSSF Scorecard** | Supply Chain Security Auditing | Evaluates software supply chain security posture (pinned dependencies, branch protection, dangerous workflows). |
| **StepSecurity Harden-Runner** | Runner Security & Egress Monitoring | Kernel-level runtime agent monitoring runner socket connections and preventing credential exfiltration. |
| **Codecov & gcovr / lcov** | Code Coverage Analysis & QA | Collects C++ `gcov` and JavaScript coverage data, generating line-by-line coverage reports and deltas. |
| **Mozilla sccache / Actions Cache** | Distributed Compiler Caching | Caches compilation object files to drastically reduce re-compilation times of V8, OpenSSL, and Node core. |
| **Node Benchmark Suite (`benchmark/`)** | Performance Micro-benchmarking | Rigorous benchmark suite measuring throughput and latency for HTTP, Buffers, Streams, Crypto, and Event Loop. |
| **license-builder & check-licenses** | Legal Compliance & Attribution | Scans third-party dependencies (V8, OpenSSL, zlib, libuv) and generates consolidated `LICENSE` attribution. |
| **Slack / Bot Integrations** | Operational Alerting & Notification | Real-time notifications for commit pushes, release staging proposals, and pull request review requests. |
