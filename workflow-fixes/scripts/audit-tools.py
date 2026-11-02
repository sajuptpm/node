import os
import re

workflows_dir = '.github/workflows'
actions_used = {}
secrets_used = {}
urls_used = {}
runners_used = {}

for f in sorted(os.listdir(workflows_dir)):
    if not f.endswith('.yml'):
        continue
    path = os.path.join(workflows_dir, f)
    with open(path, 'r', encoding='utf-8') as stream:
        content = stream.read()
    
    # find uses:
    uses = re.findall(r'uses:\s*([^\s#\r\n]+)', content)
    for u in uses:
        actions_used.setdefault(u, []).append(f)
        
    # find secrets
    sec = re.findall(r'secrets\.([A-Za-z0-9_]+)', content)
    for s in sec:
        secrets_used.setdefault(s, []).append(f)
        
    # find runs-on
    runs_on = re.findall(r'runs-on:\s*([^\r\n]+)', content)
    for r in runs_on:
        runners_used.setdefault(r.strip(), []).append(f)

    # find URLs / external services
    urls = re.findall(r'https?://[a-zA-Z0-9.-]+', content)
    for u in urls:
        urls_used.setdefault(u, []).append(f)

print('=== ACTIONS USED ===')
for a, fls in sorted(actions_used.items()):
    print(f'{a}: in {len(fls)} files -> {fls[:3]}')

print('\n=== SECRETS REFERENCED ===')
for s, fls in sorted(secrets_used.items()):
    print(f'{s}: in {len(fls)} files -> {fls}')

print('\n=== RUNNERS USED ===')
for r, fls in sorted(runners_used.items()):
    print(f'{r}: in {len(fls)} files -> {fls[:3]}')

print('\n=== EXTERNAL DOMAINS REFERENCED ===')
for u, fls in sorted(urls_used.items()):
    print(f'{u}: in {len(fls)} files -> {fls[:3]}')
