import subprocess
import re
import os

base_commit = '686612918b6'
res = subprocess.run(['git', 'ls-tree', '--name-only', f'{base_commit}:.github/workflows'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
files = sorted([f for f in res.stdout.splitlines() if f.endswith('.yml') or f.endswith('.yaml')])

print(f"Total workflow files at base commit: {len(files)}")

workflows_data = []

for f in files:
    content = subprocess.run(['git', 'show', f'{base_commit}:.github/workflows/{f}'], capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout
    
    # Extract workflow name
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    wf_name = name_match.group(1).strip('"\'') if name_match else f
    
    # Extract runs-on
    runs_on = set(re.findall(r'runs-on:\s*([^\n\r]+)', content))
    cleaned_runners = set()
    for r in runs_on:
        r_clean = r.strip().strip('[]"\'')
        if '${{' in r_clean:
            cleaned_runners.add(r_clean)
        elif ',' in r_clean:
            for part in r_clean.split(','):
                cleaned_runners.add(part.strip().strip('"\''))
        else:
            cleaned_runners.add(r_clean)
            
    # Extract secrets
    secrets = set(re.findall(r'secrets\.([A-Za-z0-9_]+)', content))
    
    # Check key tools/infra
    content_lower = content.lower()
    infra_items = []
    
    # Check runner types
    for r in cleaned_runners:
        if 'ubuntu-slim' in r:
            infra_items.append(('OpenJS Custom Runners (ubuntu-slim)', 'Pre-warmed VM runner pool for fast execution'))
        elif 'ubuntu-24.04-arm' in r:
            infra_items.append(('Managed ARM64 Runners (ubuntu-24.04-arm)', 'GitHub Actions managed ARM64 runner'))
        elif 'macos' in r:
            infra_items.append(('Standard GitHub macOS Runners (macos-latest / macos-15)', 'Standard GitHub-hosted macOS runner'))
        elif 'windows' in r:
            infra_items.append(('Standard GitHub Windows Runners (windows-2022 / windows-latest)', 'Standard GitHub-hosted Windows runner'))
        elif 'ubuntu' in r or 'matrix.runner' in r:
            infra_items.append(('Standard GitHub Linux Runners (ubuntu-latest / ubuntu-24.04)', 'Standard GitHub-hosted Linux runner'))
            
    # Check other tools/infra
    if 'sccache' in content_lower:
        infra_items.append(('Mozilla sccache Cloud Storage', 'Distributed compiler cache for C/C++'))
    if 'cachix' in content_lower:
        infra_items.append(('Cachix Nix Binary Cache (nodejs.cachix.org)', 'Nix binary derivation cache'))
    if 'codecov' in content_lower:
        infra_items.append(('Codecov Coverage Platform (codecov-action)', 'Code coverage tracking and visualization'))
    if 'harden-runner' in content_lower:
        infra_items.append(('StepSecurity Harden-Runner', 'Runtime security monitoring and network egress control'))
    if 'codeql' in content_lower or 'github/codeql-action' in content:
        infra_items.append(('GitHub Advanced Security (GHAS) / CodeQL', 'SAST security vulnerability scanner'))
    if 'slack' in content_lower or 'rtcamp/action-slack-notify' in content:
        infra_items.append(('Slack Enterprise Messaging (action-slack-notify)', 'Slack webhook notification'))
    if 'jenkins' in content_lower or 'ci.nodejs.org' in content_lower or 'start-ci' in content_lower:
        infra_items.append(('OpenJS Jenkins Build Farm (ci.nodejs.org)', 'Cross-platform multi-architecture build and test farm'))
    if 'agentscan' in content_lower:
        infra_items.append(('AgentScan PR Bot Scanner', 'AI-assisted PR contribution scanner'))
    if 'wpt.fyi' in content_lower or 'wpt_fyi' in content_lower:
        infra_items.append(('Web Platform Tests API (wpt.fyi)', 'External WPT results ingestion dashboard'))
    if 'benchmark.yml' in f:
        infra_items.append(('Bare-Metal Benchmark Server Pool', 'Dedicated physical benchmarking hardware for low-jitter runs'))
    if 'gh_user_token' in content_lower or 'node_core_utils_token' in content_lower:
        infra_items.append(('Bot Collaborator User Seat (GH_USER_TOKEN)', 'Service account user seat for repository automation'))
        
    # Deduplicate infra_items by name
    dedup_infra = []
    seen = set()
    for name, desc in infra_items:
        if name not in seen:
            seen.add(name)
            dedup_infra.append((name, desc))
            
    # If no infra detected (e.g. simple workflow), default to standard runner
    if not dedup_infra:
        dedup_infra.append(('Standard GitHub-Hosted Runners', 'Standard virtual machine runner'))
        
    workflows_data.append({
        'file': f,
        'name': wf_name,
        'runners': list(cleaned_runners),
        'secrets': list(secrets),
        'infra': dedup_infra
    })

print(f"Processed {len(workflows_data)} workflows.")
for w in workflows_data[:10]:
    print(f"\n{w['file']} ({w['name']}):")
    for inf, d in w['infra']:
        print(f"  - {inf}")
