"""Architecture fitness functions asserting strict Clean Architecture layer boundaries.

Ensures that dependencies flow strictly inwards:
  presentation -> infrastructure -> application -> domain
Domain must remain completely isolated from outer layers and web/DB frameworks.
"""

from __future__ import annotations

import ast
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"


def _get_imports(directory: Path) -> list[tuple[str, str]]:
    """Extracts all imported module names from all python files in the directory."""
    imports: list[tuple[str, str]] = []
    for file_path in directory.rglob("*.py"):
        if file_path.name.startswith("__"):
            continue
        rel_path = file_path.relative_to(APP_DIR.parent).as_posix()
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((rel_path, alias.name))
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append((rel_path, node.module))
    return imports


def test_domain_layer_isolation_has_no_outer_or_framework_dependencies():
    """Domain layer must not depend on application, infrastructure, presentation, or frameworks."""
    forbidden_prefixes = (
        "app.application",
        "app.infrastructure",
        "app.presentation",
        "fastapi",
        "starlette",
        "sqlalchemy",
    )
    domain_imports = _get_imports(APP_DIR / "domain")
    violations = [
        f"{source} imports {module}"
        for source, module in domain_imports
        if any(module == prefix or module.startswith(f"{prefix}.") for prefix in forbidden_prefixes)
    ]
    assert not violations, f"Domain layer violations detected: {violations}"


def test_application_layer_does_not_depend_on_infrastructure_or_presentation():
    """Application layer must not depend on infrastructure, presentation, or web framework."""
    forbidden_prefixes = (
        "app.infrastructure",
        "app.presentation",
        "fastapi",
    )
    app_imports = _get_imports(APP_DIR / "application")
    violations = [
        f"{source} imports {module}"
        for source, module in app_imports
        if any(module == prefix or module.startswith(f"{prefix}.") for prefix in forbidden_prefixes)
    ]
    assert not violations, f"Application layer violations detected: {violations}"


def test_infrastructure_layer_does_not_depend_on_presentation():
    """Infrastructure layer must not depend on presentation (controllers/routers)."""
    forbidden_prefixes = (
        "app.presentation",
    )
    infra_imports = _get_imports(APP_DIR / "infrastructure")
    violations = [
        f"{source} imports {module}"
        for source, module in infra_imports
        if any(module == prefix or module.startswith(f"{prefix}.") for prefix in forbidden_prefixes)
    ]
    assert not violations, f"Infrastructure layer violations detected: {violations}"
