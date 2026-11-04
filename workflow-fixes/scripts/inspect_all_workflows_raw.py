import subprocess
import re
import os

base_commit = '686612918b6'
res = subprocess.run(['git', 'ls-tree', '--name-only', f'{base_commit}:.github/workflows'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
files = sorted([f for f in res.stdout.splitlines() if f.endswith('.yml') or f.endswith('.yaml')])

print(f"Total workflow files: {len(files)}")

# Let's inspect each workflow to determine its exact jobs, runners, tools, description, category, and mandatory status
workflow_details = {}

for f in files:
    content = subprocess.run(['git', 'show', f'{base_commit}:.github/workflows/{f}'], capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout
    
    # Workflow name
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    wf_name = name_match.group(1).strip('"\'') if name_match else f
    
    # Lines of content
    lines = content.splitlines()
    
    # Runners
    runners = set(re.findall(r'runs-on:\s*([^\n\r]+)', content))
    cleaned_runners = []
    for r in runners:
        r_str = r.strip().strip('[]"\'')
        if ',' in r_str and not '${{' in r_str:
            cleaned_runners.extend([x.strip().strip('"\'') for x in r_str.split(',')])
        else:
            cleaned_runners.append(r_str)
            
    # Secrets
    secrets = set(re.findall(r'secrets\.([A-Za-z0-9_]+)', content))
    
    workflow_details[f] = {
        'name': wf_name,
        'runners': cleaned_runners,
        'secrets': list(secrets),
        'content': content
    }

for f, d in workflow_details.items():
    print(f"=== {f} ({d['name']}) ===")
    print(f"  Runners: {d['runners']}")
    print(f"  Secrets: {d['secrets']}")
