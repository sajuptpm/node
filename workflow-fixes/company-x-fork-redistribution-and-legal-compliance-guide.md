# Legal & Compliance Guide: Forking, Modifying, Rebranding, and Redistributing Node.js for Company X

## 1. Executive Legal Summary

**Yes, Company X can legally fork Node.js, apply bug fixes, vulnerability fixes, and enhancements, release the distribution under Company X's brand, redistribute it freely in source and binary formats, and keep the source code 100% open source.**

The core of the Node.js project is licensed under the **MIT License**, one of the most permissive open-source licenses in existence. The MIT License explicitly authorizes copying, modifying, merging, publishing, distributing, sublicensing, and selling the software without royalty or commercial restriction.

However, from an intellectual property and corporate governance perspective, Company X must manage **two critical legal requirements**:
1. **Copyright vs. Trademark Separation**: The MIT License grants rights to the *copyrighted source code*, but **not** to the trademarks or logos. The name **"Node.js"** and the official hexagon logo are registered trademarks of the **OpenJS Foundation** (Linux Foundation). Company X **must rebrand** its downstream distribution (e.g., *"Company X JavaScript Runtime, based on Node.js"*) to avoid trademark infringement and consumer confusion.
2. **Attribution & Notice Preservation**: Company X must retain the original copyright notices and permission notices for Node.js, Joyent, Inc., and all 42+ bundled third-party libraries in `deps/` in all source trees and binary distributions.

---

## 2. Evidence & Core Permissions Table

| Item / Permission Question | Permissible? | Governing License | License File Location (Upstream URL & Local File) | Exact Words in License Allowing This | Legal Analysis & Practical Guidance |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Fork this project** | **YES** | MIT License | • [`LICENSE`](file:///c:/projects/node/LICENSE#L6-L11)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE) | *"Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy..."* | Company X can create public or private forks of the repository without requesting permission or paying any license fees. |
| **2. Apply bug fixes, vulnerability fixes, & enhancements** | **YES** | MIT License | • [`LICENSE`](file:///c:/projects/node/LICENSE#L8-L10)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE) | *"...including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software..."* | Company X has unrestricted legal authority to patch CVEs, optimize internal APIs, backport security patches, or add proprietary/open features. |
| **3. Release in the name of Company X** | **YES** *(Subject to Trademark Policy)* | MIT License & OpenJS Trademark Policy | • [`LICENSE`](file:///c:/projects/node/LICENSE#L8-L10)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE)<br>• [OpenJS Trademark Policy](https://trademark-policy.openjsf.org/) | • MIT: *"...rights to... publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so..."*<br>• OpenJS: *"Any use of marks that are confusingly similar to trademarks of the OpenJS Foundation is prohibited."* | Company X can release the distribution under its own company name and brand (e.g., *"Company X Enterprise Engine"*), but **must not call the binary `node` or the product `Node.js`** without OpenJS trademark authorization. Nominative use (e.g., *"compatible with Node.js"*) is allowed. |
| **4. Redistribute (Source & Binaries)** | **YES** | MIT License | • [`LICENSE`](file:///c:/projects/node/LICENSE#L8-L11)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE) | *"...to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software..."* | Redistribution is allowed in source code form, compiled executable/binary form, Docker images, and containerized cloud services, for both commercial and non-commercial purposes. |
| **5. Keep code open-sourced** | **YES** | MIT License | • [`LICENSE`](file:///c:/projects/node/LICENSE#L6-L14)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE) | *"...to deal in the Software without restriction... subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."* | MIT is a permissive license (not copyleft). It grants the freedom to redistribute the fork openly under MIT or compatible permissive terms. Company X can publish its modified source repository on GitHub/GitLab openly. |

---

## 3. Mandatory Compliance & Operational Obligations Table

To protect Company X against intellectual property claims, trademark disputes, or liability exposure, the following **6 critical obligations and restrictions** must be adhered to:

| Additional Compliance Item | Obligation Type | Governing Authority | Location & Reference Link | Exact Governing Clause / Rule | Compliance Action Required for Company X |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A. Mandatory Copyright Notice Retention** | **Legal Condition** | MIT License Condition | • [`LICENSE`](file:///c:/projects/node/LICENSE#L13-L14)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE) | *"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."* | **Mandatory**: Company X **must retain** the original notices (`Copyright Node.js contributors`, `Copyright Joyent, Inc.`) in source files, tarballs, and include a copy of `LICENSE` in binary installations. Company X may append its own notice: `Copyright (C) 2026 Company X Inc. All rights reserved.` |
| **B. Rebranding & Trademark Policy** | **Trademark Restriction** | OpenJS Foundation Trademark Policy | • [OpenJS Trademark Policy](https://trademark-policy.openjsf.org/)<br>• [OpenJS Foundation Guidelines](https://openjsf.org/about/trademark-policy) | *"The OpenJS Foundation trademarks may not be used in connection with any product or service that does not originate from the project... or in any manner that is likely to cause confusion."* | **Mandatory**: Company X must: <br>1. Change the executable/binary name or package name (e.g., `companyx-node` or `companyx-js`).<br>2. Remove official Node.js hexagon logos from UI/installer splash screens.<br>3. State in documentation: *"Company X Engine is a distribution based on the OpenJS Foundation's Node.js project."* |
| **C. Disclaimer of Warranty & Liability ("AS IS")** | **Liability Protection** | MIT License Disclaimer | • [`LICENSE`](file:///c:/projects/node/LICENSE#L16-L23)<br>• Upstream: [`nodejs/node/LICENSE`](https://github.com/nodejs/node/blob/main/LICENSE) | *"THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED... IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY..."* | **Mandatory**: Company X cannot promise customers warranties on behalf of upstream Node.js contributors. Company X must provide its own warranty/SLA terms for its downstream product and assume commercial liability for its fixes. |
| **D. Bundled Third-Party Dependencies Compliance (`deps/`)** | **Multi-License Compliance** | Individual FOSS Licenses (42+ libraries) | • [`LICENSE`](file:///c:/projects/node/LICENSE#L52-L2864)<br>• [`deps/`](file:///c:/projects/node/deps/) directory | Line 49: *"The Node.js license applies to all parts of Node.js that are not externally maintained libraries."* | **Mandatory**: Node.js bundles 42+ libraries. All are permissive, but each has notice obligations: <br>• **V8** (`deps/v8`): BSD-3-Clause (preserve BSD notice).<br>• **OpenSSL** (`deps/openssl`): Apache-2.0 (preserve Apache notice & `NOTICE` file).<br>• **libuv** (`deps/uv`): MIT.<br>• **ICU** (`deps/icu-small`): Unicode-DFS-2016.<br>Company X must distribute the unified `LICENSE` file containing all dependency notices. |
| **E. Patent Grant & Retaliation Terms** | **Intellectual Property** | Patent Law & Apache 2.0 (in `deps/openssl`) | • [`LICENSE`](file:///c:/projects/node/LICENSE#L461-L510) (OpenSSL Apache-2.0 section) | Section 3: *"Grant of Patent License... Each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable... patent license..."* | MIT has an implied patent license, while dependencies like OpenSSL provide an express patent grant. If Company X initiates patent litigation against upstream contributors over the software, patent licenses are subject to termination. |
| **F. Upstream Contribution & Agent Governance (DCO)** | **Contribution Policy** | Node.js Governance & AGENTS.md | • [`AGENTS.md`](file:///c:/projects/node/AGENTS.md)<br>• [doc/contributing/pull-requests.md](file:///c:/projects/node/doc/contributing/pull-requests.md) | *"All commits must be signed off by the human user using Signed-off-by... as an attestation to the Developer Certificate of Origin. AI-assistance must be acknowledged using Assisted-by."* | If Company X chooses to contribute bug fixes back upstream to `nodejs/node`, commits must include human sign-off (`Signed-off-by:`) and AI disclosure (`Assisted-by:`). |

---

## 4. Step-by-Step Practical Implementation Checklist for Company X

### Step 1: Forking & Source Repository Setup
1. Fork `https://github.com/nodejs/node` to Company X's organization account.
2. Establish a synchronization branch (e.g., `upstream-main`) to track official Node.js security releases and LTS updates.
3. Establish a Company X release branch (e.g., `companyx-main` or `companyx-lts`).

### Step 2: Applying Bug Fixes & Enhancements
1. Apply internal bug fixes, performance improvements, and CVE security patches.
2. Ensure automated regression test suites pass across targeted enterprise operating systems.

### Step 3: Rebranding & Trademark Separation
1. **Rename the Executable / Binary**:
   - Change output binary names in the build configuration from `node` to `companyx-node` (or provide a symlink with prominent documentation).
2. **Replace Brand Assets**:
   - Remove or replace official Node.js logos, splash graphics, and trademarked icons with Company X artwork.
3. **Documentation Clarification**:
   - In the `README.md` and user documentation, include a clear disclaimer:
     > *"Company X JavaScript Runtime is an independent distribution developed by Company X Inc. based on the Node.js open-source project. Node.js is a registered trademark of the OpenJS Foundation. This distribution is not endorsed by, sponsored by, or affiliated with the OpenJS Foundation or the Node.js Technical Steering Committee."*

### Step 4: License Notice & Attribution Compliance
1. Preserve the top-level `LICENSE` file containing the Node.js contributors notice, Joyent, Inc. notice, and all 42+ dependency licenses.
2. Optionally append Company X's copyright header at the top of the `LICENSE` file or in modified source files:
   ```text
   Copyright (C) 2026 Company X Inc. All rights reserved.
   Copyright Node.js contributors. All rights reserved.
   Copyright Joyent, Inc. and other Node contributors. All rights reserved.
   ```
3. Ensure binary installers (MSI, PKG, DEB, RPM, Docker) include the full `LICENSE` file in the installation directory.

### Step 5: Redistribution & Open-Source Release
1. Publish the modified source code in a public git repository under the MIT License.
2. Distribute binaries, container images, and packages freely without royalty restrictions.

---

## 5. Authoritative References & Policies

- **Node.js Upstream LICENSE**: [https://github.com/nodejs/node/blob/main/LICENSE](https://github.com/nodejs/node/blob/main/LICENSE)
- **OpenJS Foundation Trademark Policy**: [https://trademark-policy.openjsf.org/](https://trademark-policy.openjsf.org/)
- **OpenJS Foundation Project Guidelines**: [https://openjsf.org/about/trademark-policy](https://openjsf.org/about/trademark-policy)
- **Open Source Initiative (OSI) - MIT License Specification**: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)
- **Node.js AI Automation Guidelines**: [`AGENTS.md`](file:///c:/projects/node/AGENTS.md)
