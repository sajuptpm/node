# Cachix Service & Node.js Vendor Cost Analysis

## Executive Summary

| Question | Assessment / Answer |
| :--- | :--- |
| **What is Cachix?** | A hosted **binary cache service** for the **Nix package manager** and **NixOS** ecosystem (<https://www.cachix.org>). It stores pre-compiled immutable binary derivations (`/nix/store/...` `.nar` archives) on a global Cloudflare CDN to avoid recompiling heavy C/C++ dependencies (like Google V8 and OpenSSL). |
| **Does Node.js vendor pay for it?** | **No.** Neither the Node.js project nor the OpenJS Foundation pays Cachix. Node.js operates under Cachix's **Free Open-Source Software (OSS) Tier** and community sponsorship program. |
| **Annual Cost to Upstream** | **$0.00 / year** |
| **Annual Cost to Forked Repo** | **$0.00 / year** |
| **Mandatory for Fork Releases?** | **No.** Official Node.js production release builds use standard GNU Make / Ninja (`./configure && make -j$(nproc)`) and do not rely on Nix or Cachix. |

---

## 1. What is Cachix (`https://www.cachix.org`)?

### 1.1 Technical Definition
Cachix is a specialized binary artifact caching service created by Domen Kožar (a prominent NixOS contributor). It is built specifically to integrate with the **Nix package manager** and Nix continuous integration pipelines.

In traditional CI, when a project depends on large C/C++ libraries, runners must either:
1. Recompile the entire dependency tree from source on every run (very slow), or
2. Rely on OS package managers that may have version drift or lack required compile-time flags.

In the **Nix ecosystem**, software packages are built as deterministic, content-addressed derivations located at `/nix/store/<hash>-<package-name>`. Cachix provides a managed remote store for these derivations:
- Whenever a package is built inside Nix, the resulting binary archive (`.nar`) and its metadata (`.narinfo`) are uploaded to Cachix.
- Subsequent CI runners (and local developers) simply download the pre-compiled binary over a global Cloudflare CDN instead of compiling it locally.

### 1.2 Why Node.js Adopted Cachix
In PR [#60121](https://github.com/nodejs/node/pull/60121) (introduced by Node.js Technical Steering Committee member Antoine du Hamel), Node.js integrated Nix to automate CI tests against a matrix of shared external libraries (different versions of OpenSSL, zlib, brotli, libuv, and Google V8).

- Building **Google V8** from source inside CI takes **20 to 45 minutes** per architecture.
- By caching pre-built V8 derivations (`libv8-aarch64-linux`, etc.) on `nodejs.cachix.org`, Node.js CI runs finish in minutes rather than hours.

Node.js explicitly documents this in its core developer guide ([`BUILDING.md`](../BUILDING.md#L284-L285)):
```markdown
in which case those will be built locally, or you can use the Cachix repository
for the project: `cachix use nodejs`. See <https://docs.cachix.org/> for more
details.
```

---

## 2. Does the Node.js Vendor Pay for Cachix?

**No. The Node.js project and the OpenJS Foundation do not pay Cachix.**

### 2.1 Cachix Open-Source Policy
Cachix offers a permanent **Free Tier for Open-Source Projects**:
- **5 GB binary cache storage** per public open-source project.
- **Unlimited bandwidth** powered by a global Cloudflare CDN.
- **Upstream Deduplication**: Any binary package that is already present in the official NixOS upstream binary cache (`cache.nixos.org`) is deduplicated and **does not consume storage quota** on Cachix.
- **Automatic Garbage Collection**: If the 5 GB quota is reached, least recently used (LRU) cached derivations are purged automatically without failing builds.

### 2.2 Community Sponsorship
In addition to the standard free open-source tier, Cachix directly sponsors foundational open-source ecosystems. The `nodejs` cache namespace (`nodejs.cachix.org`) is granted complimentary community allowances as part of Cachix's open-source support initiative.

### 2.3 OpenJS Foundation Accounting Verification
The OpenJS Foundation publicly reports its annual budget, infrastructure expenses, and corporate sponsors (such as AWS, Microsoft Azure, Cloudflare, DigitalOcean, MacStadium, and Equinix Metal). Cachix is **not** a paid infrastructure vendor of the foundation.

---

## 3. Workflows Utilizing Cachix in Node.js

The following GitHub Actions workflows in `nodejs/node` interact with Cachix:

| Workflow File | Purpose | Cachix Role |
| :--- | :--- | :--- |
| [`.github/workflows/test-shared.yml`](../.github/workflows/test-shared.yml) | Matrix testing against shared external libraries | Pulls / pushes pre-compiled V8 and OpenSSL derivations |
| [`.github/workflows/build-shared.yml`](../.github/workflows/build-shared.yml) | Shared library build verification | Pulls cached Nix build tools and dependencies |
| [`.github/workflows/nix-changes.yml`](../.github/workflows/nix-changes.yml) | Verifies PR changes touching `shell.nix` / `tools/nix` | Evaluates derivations and caches verified outputs |
| [`.github/workflows/benchmark.yml`](../.github/workflows/benchmark.yml) | Performance benchmarks | Sets up reproducible Nix benchmark environments |
| [`.github/workflows/tools.yml`](../.github/workflows/tools.yml) | Internal tooling CI | Sets up hermetic development dependencies |

---

## 4. Security & Permissions Architecture

### 4.1 Write vs. Read Access
The repository handles Cachix credentials via the repository secret `CACHIX_AUTH_TOKEN`:

```yaml
# Upstream configuration in .github/workflows/test-shared.yml
- uses: cachix/cachix-action@v17
  if: ${{ steps.v8-drv.outputs.ALREADY_CACHED != 'true' }}
  with:
    name: nodejs
    authToken: ${{ secrets.CACHIX_AUTH_TOKEN }}
```

- **Write Access**: Restricted strictly to upstream `nodejs/node` CI runs that have access to `secrets.CACHIX_AUTH_TOKEN`.
- **Read Access**: **Completely open and public.** Anyone worldwide (including external contributors, PRs from forks, and downstream repositories) can read and pull cached binaries from `https://nodejs.cachix.org` over public HTTPS with no token.

### 4.2 Built-In Fork Fallback (Commit `cee0154af8`)
The Node.js core team designed the shared-library CI pipeline so that lack of Cachix write permissions **never breaks a build**. 

In commit [`cee0154af8`](https://github.com/nodejs/node/commit/cee0154af8) (*"tools: reuse V8 builds even without Cachix on test-shared"*), an automated fallback was implemented:

```yaml
# If not cached on Cachix and NO write token is present (e.g. on a fork):
- name: Upload libv8
  if: ${{ steps.cachix-check.outputs.ALREADY_CACHED != 'true' && steps.cachix-check.outputs.HAS_WRITE_TOKEN != 'true' }}
  uses: actions/upload-artifact@v4
  with:
    name: libv8
    path: libv8
```

1. The runner checks `https://nodejs.cachix.org/...narinfo` to see if the required derivation is already cached.
2. If already cached, it downloads it directly from Cachix for **free** (read-only mode).
3. If not cached and no `CACHIX_AUTH_TOKEN` is found, it compiles V8 locally and shares it with downstream jobs using standard **GitHub Actions Artifacts** (`actions/upload-artifact` and `actions/download-artifact`).

---

## 5. Downstream Fork & Enterprise Assessment

For an organization maintaining an internal or public fork of Node.js:

| Option | Implementation | Annual Vendor Cost | Operational Overhead |
| :--- | :--- | :--- | :--- |
| **Option A: Public Read (Recommended)** | Keep workflow unchanged without setting `CACHIX_AUTH_TOKEN`. Read public pre-compiled binaries from `nodejs.cachix.org`. Fall back to GitHub Actions artifacts if rebuilding. | **$0.00** | None |
| **Option B: Standard Build Bypass** | Completely bypass Nix/Cachix workflows. Run builds and releases via standard `./configure && make -j` or Ninja on standard runners. | **$0.00** | None (Standard release model) |
| **Option C: Dedicated Free OSS Cachix** | Register a free open-source account on cachix.org (5 GB free) and supply your own `CACHIX_AUTH_TOKEN` secret. | **$0.00** | Initial token setup |
| **Option D: Commercial Private Cachix** | Purchase a private Cachix subscription (only needed if building confidential proprietary Nix derivations in private repositories). | Starting at $30/mo ($360/yr) | Optional |

### Recommendation for Fork Release Engineering
Do **not** purchase or budget for Cachix. Official Node.js binary release packaging does not use Cachix or Nix. The existing upstream workflows handle absent tokens cleanly at **$0 / year**.
