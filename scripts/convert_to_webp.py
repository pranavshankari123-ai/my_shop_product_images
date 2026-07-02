import subprocess
import os
from PIL import Image

# Only look at files changed in the most recent commit, so this doesn't
# reprocess the whole repo on every push.
diff = subprocess.run(
    ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
    capture_output=True, text=True
)
changed = [f for f in diff.stdout.splitlines() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for path in changed:
    if not os.path.isfile(path):
        continue
    webp_path = os.path.splitext(path)[0] + '.webp'
    try:
        img = Image.open(path)
        img.save(webp_path, format='WEBP', quality=85)
        os.remove(path)
        print(f'Converted {path} -> {webp_path}')
    except Exception as e:
        print(f'Skipped {path}: {e}')
