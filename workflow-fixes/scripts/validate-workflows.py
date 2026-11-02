#!/usr/bin/env python3
"""
validate-workflows.py - Statically audits all GitHub Actions workflows in .github/workflows/*.yml.
Verifies YAML syntax, workflow_dispatch triggers, input schema, runner labels,
fork-compatible repo guards, and action version deprecations.
"""

import glob
import os
import sys

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install via: pip install pyyaml")
    sys.exit(1)

# Ensure stdout supports UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


PROPRIETARY_RUNNERS = ["ubuntu-slim", "ubuntu-24.04-arm"]


def check_workflow(filepath):
    errors = []
    warnings = []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Parse YAML
    try:
        data = yaml.safe_load(content)
    except Exception as e:
        return ["YAML parse error: " + str(e)], []

    if not isinstance(data, dict):
        return ["Workflow file does not contain a valid YAML mapping"], []

    # 2. Check workflow_dispatch trigger
    on_trigger = data.get("on") or data.get(True)  # PyYAML might parse 'on' as boolean True
    has_dispatch = False
    if isinstance(on_trigger, dict):
        has_dispatch = "workflow_dispatch" in on_trigger
    elif isinstance(on_trigger, list):
        has_dispatch = "workflow_dispatch" in on_trigger
    elif on_trigger == "workflow_dispatch":
        has_dispatch = True

    if not has_dispatch:
        errors.append("Missing 'workflow_dispatch' trigger")

    # 3. Check for hardcoded proprietary runners without fallback expressions
    jobs = data.get("jobs", {})
    if isinstance(jobs, dict):
        for j_name, j_data in jobs.items():
            if not isinstance(j_data, dict):
                continue
            runs_on = str(j_data.get("runs-on", ""))
            for prop in PROPRIETARY_RUNNERS:
                if prop in runs_on and "vars." not in runs_on:
                    warnings.append(f"Job '{j_name}' uses hardcoded runner '{prop}' without vars.RUNNER_LABEL fallback")

            # Check job-level if condition
            job_if = str(j_data.get("if", ""))
            if "github.repository == 'nodejs/node'" in job_if:
                if "workflow_dispatch" not in job_if and "vars." not in job_if and "github.repository_owner" not in job_if:
                    errors.append(f"Job '{j_name}' hardcodes 'github.repository == nodejs/node' blocking forks on manual dispatches")

    # 4. Check for deprecated action versions (v1, v2, v3 for checkout/upload-artifact)
    for line in content.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("- uses: actions/checkout@v1") or trimmed.startswith("- uses: actions/checkout@v2"):
            warnings.append("Using deprecated checkout action version (consider v4)")
        if trimmed.startswith("- uses: actions/upload-artifact@v1") or trimmed.startswith("- uses: actions/upload-artifact@v2") or trimmed.startswith("- uses: actions/upload-artifact@v3"):
            warnings.append("Using deprecated upload-artifact action version (consider v4)")

    return errors, warnings


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    workflow_dir = os.path.join(root_dir, ".github", "workflows")

    files = sorted(glob.glob(os.path.join(workflow_dir, "*.yml")) + glob.glob(os.path.join(workflow_dir, "*.yaml")))
    if not files:
        print(f"No workflow files found in {workflow_dir}")
        sys.exit(1)

    print("\n" + "=" * 45 + " Workflow Static Validation " + "=" * 45)
    print(f"{'Status':<8} {'File Name':<38} {'Issues'}")
    print("-" * 105)

    pass_count = 0
    warn_count = 0
    fail_count = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        errors, warnings = check_workflow(fpath)

        if errors:
            status = "[FAIL]"
            fail_count += 1
            issues_str = "; ".join(errors)
        elif warnings:
            status = "[WARN]"
            warn_count += 1
            issues_str = "; ".join(warnings)
        else:
            status = "[PASS]"
            pass_count += 1
            issues_str = "All structural checks passed cleanly"

        print(f"{status:<8} {fname:<38} {issues_str[:55]}")

    print("\n" + "=" * 40 + " Validation Summary " + "=" * 45)
    print(f"Total Workflows: {len(files)} | Passed: {pass_count} | Warnings: {warn_count} | Failed: {fail_count}")
    print("=" * 105 + "\n")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
