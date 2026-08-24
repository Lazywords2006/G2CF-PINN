"""Rebuild the local PDF integrity manifest from Appendix A."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "附录A_本地PDF清单_156份.json"
OUTPUT = HERE / "附录C_本地PDF_SHA256与重复组.json"


def main() -> int:
    records = json.loads(SOURCE.read_text(encoding="utf-8"))
    files = []
    by_hash: dict[str, list[str]] = defaultdict(list)
    for record in records:
        relative = str(record["path"])
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append({"path": relative, "sha256": digest, "bytes": path.stat().st_size})
        by_hash[digest].append(relative)
    duplicates = [
        {"sha256": digest, "paths": paths}
        for digest, paths in sorted(by_hash.items())
        if len(paths) > 1
    ]
    result = {
        "source": SOURCE.name,
        "algorithm": "SHA-256",
        "file_count": len(files),
        "unique_content_count": len(by_hash),
        "duplicate_group_count": len(duplicates),
        "duplicate_groups": duplicates,
        "files": files,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("file_count", "unique_content_count", "duplicate_group_count")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
