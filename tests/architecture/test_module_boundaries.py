"""Import boundaries of the modular monolith (ADR-015). A violation fails the build.

Rules, all checked statically from the import statements under `app/`:

1. A module may import another module only through its public interface, `app.modules.<name>`.
   Reaching into `app.modules.<name>.<anything>` (router, schemas, models, service) is a violation.
2. Modules do not import each other in a cycle.
3. Layers point one way: `core` imports no other `app` code, `db` imports only `core`,
   and nothing under `app/` except the wiring in `app/main.py` imports `app.main`.
"""

import ast
from collections.abc import Mapping
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parents[2] / "app"
MODULES_DIR = APP / "modules"
INTERNAL_FILES = {"router", "schemas", "models", "service"}
MODULES = sorted(p.name for p in MODULES_DIR.iterdir() if p.is_dir() and p.name != "__pycache__")


def dotted(path: Path) -> str:
    parts = path.relative_to(APP.parent).with_suffix("").parts
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def imported_names(path: str, source: str) -> list[str]:
    """Absolute dotted names imported by `source`, which lives in `path` (relative to the repo)."""
    package = path.removesuffix(".py").split("/")
    package = package[:-1]  # the package a relative import is resolved against
    names: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package[: len(package) - (node.level - 1)]
                module = ".".join([*base, *(node.module.split(".") if node.module else [])])
            else:
                module = node.module or ""
            names.append(module)
            # `from app.modules import campaigns` imports the package itself, and
            # `from app.modules.campaigns import models` imports one of its internal files.
            parts = module.split(".")
            if module == "app.modules" or (parts[:2] == ["app", "modules"] and len(parts) == 3):
                names += [
                    f"{module}.{alias.name}"
                    for alias in node.names
                    if module == "app.modules" or alias.name in INTERNAL_FILES
                ]
    return [name for name in names if name == "app" or name.startswith("app.")]


def owner(file: str) -> str | None:
    parts = file.split("/")
    return parts[2] if len(parts) > 3 and parts[:2] == ["app", "modules"] else None


def find_violations(files: Mapping[str, str]) -> list[str]:
    """`files` maps a repo-relative path such as `app/modules/auth/router.py` to its source."""
    problems: list[str] = []
    graph: dict[str, set[str]] = {}
    for file, source in sorted(files.items()):
        own = owner(file)
        for name in imported_names(file, source):
            parts = name.split(".")
            if own is not None and parts[:2] == ["app", "modules"] and len(parts) >= 3:
                target = parts[2]
                if target != own:
                    graph.setdefault(own, set()).add(target)
                    if len(parts) > 3:
                        problems.append(
                            f"{file}: imports {name}; use the public interface app.modules.{target}"
                        )
            if own is not None and parts == ["app", "main"]:
                problems.append(f"{file}: modules must not import app.main")
            if file.startswith("app/core/") and name != "app" and parts[1] != "core":
                problems.append(f"{file}: core must not import {name}")
            if file.startswith("app/db/") and parts[1] not in {"core", "db"}:
                problems.append(f"{file}: db may import only core, not {name}")
    problems += cycles(graph)
    return problems


def cycles(graph: Mapping[str, set[str]]) -> list[str]:
    found: list[str] = []

    def visit(node: str, trail: list[str]) -> None:
        if node in trail:
            found.append(
                "import cycle between modules: " + " -> ".join([*trail[trail.index(node) :], node])
            )
            return
        for nxt in sorted(graph.get(node, ())):
            visit(nxt, [*trail, node])

    for start in sorted(graph):
        visit(start, [])
    return sorted(set(found))


def test_the_app_respects_the_module_boundaries() -> None:
    files = {
        str(path.relative_to(APP.parent)).replace("\\", "/"): path.read_text("utf-8")
        for path in APP.rglob("*.py")
    }
    assert find_violations(files) == []


@pytest.mark.parametrize("module", MODULES)
def test_every_module_declares_a_small_public_interface(module: str) -> None:
    init = MODULES_DIR / module / "__init__.py"
    tree = ast.parse(init.read_text("utf-8"))
    exported = {
        target.id
        for node in tree.body
        for target in (
            node.targets if isinstance(node, ast.Assign) else [getattr(node, "target", None)]
        )
        if isinstance(target, ast.Name)
    }
    assert "__all__" in exported, f"{init} must declare __all__"
    assert "routers" in exported, f"{init} must expose `routers` (empty if it has no endpoints)"


def test_the_checker_catches_a_reach_into_another_module() -> None:
    bad = {
        "app/modules/auth/router.py": "from app.modules.campaigns.schemas import CampaignStatus\n"
    }
    assert find_violations(bad) == [
        "app/modules/auth/router.py: imports app.modules.campaigns.schemas; "
        "use the public interface app.modules.campaigns"
    ]
    plain = {"app/modules/auth/router.py": "import app.modules.donations.service\n"}
    assert len(find_violations(plain)) == 1
    relative = {"app/modules/auth/router.py": "from ..campaigns import models\n"}
    assert len(find_violations(relative)) == 1


def test_the_checker_allows_the_public_interface_and_own_internals() -> None:
    ok = {
        "app/modules/auth/router.py": (
            "from app.modules.auth.schemas import LoginRequest\n"
            "from app.modules.campaigns import CampaignStatus\n"
            "from app.modules import donations\n"
            "from .schemas import LoginRequest\n"
        ),
        "app/modules/campaigns/router.py": "from app.core.schemas import ContractModel\n",
    }
    assert find_violations(ok) == []


def test_the_checker_catches_cycles_and_layer_violations() -> None:
    cyclic = {
        "app/modules/auth/__init__.py": "from app.modules import campaigns\n",
        "app/modules/campaigns/__init__.py": "from app.modules.auth import X\n",
    }
    assert any("import cycle" in problem for problem in find_violations(cyclic))
    assert find_violations({"app/core/x.py": "from app.db.session import get_session\n"})
    assert find_violations({"app/db/x.py": "from app.modules.auth import X\n"})
    assert find_violations({"app/modules/auth/router.py": "from app.main import create_app\n"})
