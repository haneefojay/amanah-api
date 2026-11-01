"""Write the OpenAPI contract to openapi.json (sorted keys, so diffs are reviewable).

uv run python scripts/export_openapi.py          # rewrite openapi.json
uv run python scripts/export_openapi.py --check  # exit 1 if the committed file is stale
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.core.config import Settings  # noqa: E402
from app.main import create_app  # noqa: E402

TARGET = ROOT / "openapi.json"


def render() -> str:
    # The schema never depends on configuration, so a placeholder is enough to build it.
    app = create_app(Settings(database_url="postgresql+asyncpg://unused@localhost/unused"))
    return json.dumps(app.openapi(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    rendered = render()
    if "--check" in sys.argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != rendered:
            print("openapi.json is stale. Run: uv run python scripts/export_openapi.py")
            return 1
        return 0
    TARGET.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Wrote {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
