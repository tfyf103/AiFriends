"""Read Vite's generated manifest so Django never hard-codes hashed asset names."""

import json
from pathlib import Path

from django.conf import settings


def get_vite_entry():
    manifest_path = Path(settings.BASE_DIR) / 'static' / 'frontend' / '.vite' / 'manifest.json'
    if not manifest_path.exists():
        return {'js': None, 'css': []}

    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    entry = manifest.get('index.html')
    if not entry:
        entry = next((item for item in manifest.values() if item.get('isEntry')), None)
    if not entry:
        return {'js': None, 'css': []}

    return {
        'js': f"frontend/{entry['file']}",
        'css': [f'frontend/{css}' for css in entry.get('css', [])],
    }
