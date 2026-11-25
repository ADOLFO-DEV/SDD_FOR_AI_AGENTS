#!/usr/bin/env python3
"""Helper CLI for Spec-Driven Development (SDD) in Google Antigravity (AGY IDE).

Zero external dependencies (Python 3 standard library only).
Commands:
  status [spec_filter]       Inspect constitution, specs, tasks progress, and suggest next /sdd-* command.
  detect-stack               Detect project language, frameworks, UI presence, and test runner command.
  next-id [slug] [--mkdir]   Compute next NNN spec number (e.g., 001-heat-map) and optionally create dirs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


def detect_stack(root: Path) -> dict[str, Any]:
    info: dict[str, Any] = {
        "language": "unknown",
        "frameworks": [],
        "test_command": None,
        "has_web_ui": False,
        "rules_files": [f for f in ("AGENTS.md", "GEMINI.md") if (root / f).exists()],
        "has_constitution": (root / "docs" / "constitution.md").exists(),
        "has_memory": (root / "MEMORY.md").exists(),
    }

    pkg_json = root / "package.json"
    if pkg_json.exists():
        info["language"] = "typescript" if (root / "tsconfig.json").exists() else "javascript"
        try:
            pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
        except Exception:
            pkg = {}
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        scripts = pkg.get("scripts", {})

        for fw in ("next", "react", "vue", "svelte", "astro", "@angular/core", "express", "fastify", "nestjs"):
            if fw in deps:
                info["frameworks"].append(fw)
        if any(fw in deps for fw in ("next", "react", "vue", "svelte", "astro", "@angular/core", "vite")):
            info["has_web_ui"] = True

        pm = "pnpm" if (root / "pnpm-lock.yaml").exists() else ("yarn" if (root / "yarn.lock").exists() else ("bun" if (root / "bun.lockb").exists() or (root / "bun.lock").exists() else "npm"))

        if "test" in scripts and "no test specified" not in scripts["test"].lower():
            info["test_command"] = f"{pm} test" if pm != "npm" else "npm test"
            if "vitest" in scripts["test"] and "--run" not in scripts["test"] and "run" not in scripts["test"]:
                info["test_command"] = "npx vitest run"
        elif "vitest" in deps:
            info["test_command"] = "npx vitest run"
        elif "jest" in deps:
            info["test_command"] = "npx jest"
        else:
            info["test_command"] = "node --test"

    elif (root / "pyproject.toml").exists() or (root / "requirements.txt").exists() or list(root.glob("*.py")):
        info["language"] = "python"
        pyproject_text = (root / "pyproject.toml").read_text(encoding="utf-8", errors="ignore") if (root / "pyproject.toml").exists() else ""
        if "pytest" in pyproject_text or (root / "pytest.ini").exists() or (root / "tests").exists():
            info["test_command"] = "pytest"
        else:
            info["test_command"] = "python3 -m unittest discover"
        for fw in ("fastapi", "django", "flask", "streamlit"):
            if fw in pyproject_text.lower():
                info["frameworks"].append(fw)

    elif (root / "go.mod").exists():
        info["language"] = "go"
        info["test_command"] = "go test ./..."

    elif (root / "Cargo.toml").exists():
        info["language"] = "rust"
        info["test_command"] = "cargo test"

    elif (root / "index.html").exists() or list(root.glob("*.js")):
        info["language"] = "javascript (vanilla)"
        info["test_command"] = "node --test"
        info["has_web_ui"] = (root / "index.html").exists()

    if (root / "index.html").exists() or (root / "public" / "index.html").exists():
        info["has_web_ui"] = True

    return info


def parse_spec_dir(spec_dir: Path) -> dict[str, Any]:
    spec_file = spec_dir / "spec.md"
    plan_file = spec_dir / "plan.md"
    tasks_file = spec_dir / "tasks.md"

    result: dict[str, Any] = {
        "name": spec_dir.name,
        "path": str(spec_dir.relative_to(spec_dir.parent.parent)),
        "has_spec": spec_file.exists(),
        "has_plan": plan_file.exists(),
        "has_tasks": tasks_file.exists(),
        "spec_state": "inexistente",
        "open_questions": 0,
        "tasks_done": 0,
        "tasks_pending": 0,
        "tasks_total": 0,
        "next_task_id": None,
        "phase": "Sin iniciar",
        "next_command": f"/sdd-spec {spec_dir.name} <idea>",
    }

    if spec_file.exists():
        text = spec_file.read_text(encoding="utf-8", errors="ignore")
        m_state = re.search(r"^Estado:\s*(.+)$", text, flags=re.MULTILINE | re.IGNORECASE)
        result["spec_state"] = m_state.group(1).strip() if m_state else "sin estado explícito"
        result["open_questions"] = len(re.findall(r"\[NECESITA ACLARACI[ÓO]N\]", text, flags=re.IGNORECASE))

    if tasks_file.exists():
        t_text = tasks_file.read_text(encoding="utf-8", errors="ignore")
        done_matches = re.findall(r"^\s*-\s*\[[xX]\]\s*(.+)$", t_text, flags=re.MULTILINE)
        pending_matches = re.findall(r"^\s*-\s*\[\s\]\s*(.+)$", t_text, flags=re.MULTILINE)
        result["tasks_done"] = len(done_matches)
        result["tasks_pending"] = len(pending_matches)
        result["tasks_total"] = result["tasks_done"] + result["tasks_pending"]
        if pending_matches:
            m_tid = re.search(r"\b(T\d+)\b", pending_matches[0])
            result["next_task_id"] = m_tid.group(1) if m_tid else "siguiente-tarea"

    # Determine phase & next command
    if not result["has_spec"]:
        result["phase"] = "Paso 2: Especificación pendiente"
        result["next_command"] = f"/sdd-spec {spec_dir.name} <idea inicial>"
    elif result["open_questions"] > 0 or "borrador" in result["spec_state"].lower() and not result["has_plan"]:
        result["phase"] = "Paso 2/3: Especificación en borrador / Clarificación"
        result["next_command"] = f"/sdd-clarify {spec_dir.name} (o aprobar spec y ejecutar /sdd-plan {spec_dir.name})"
    elif not result["has_plan"]:
        result["phase"] = "Paso 4: Planificación pendiente"
        result["next_command"] = f"/sdd-plan {spec_dir.name}"
    elif not result["has_tasks"]:
        result["phase"] = "Paso 5: Desglose de tareas pendiente"
        result["next_command"] = f"/sdd-tasks {spec_dir.name}"
    elif result["tasks_total"] == 0:
        result["phase"] = "Paso 5: tasks.md vacío o sin checkboxes"
        result["next_command"] = f"/sdd-tasks {spec_dir.name}"
    elif result["tasks_pending"] > 0:
        tid = result["next_task_id"] or "T1"
        result["phase"] = f"Paso 6: Implementación en curso ({result['tasks_done']}/{result['tasks_total']} tareas)"
        result["next_command"] = f"/sdd-implement {spec_dir.name} {tid}"
    elif "implementada" in result["spec_state"].lower():
        result["phase"] = "Completada y validada (Mantenimiento)"
        result["next_command"] = f"/sdd-change {spec_dir.name} <nuevo requisito>"
    else:
        result["phase"] = f"Paso 7: Lista para Validación ({result['tasks_done']}/{result['tasks_total']} tareas hechas)"
        result["next_command"] = f"/sdd-validate {spec_dir.name}"

    return result


def cmd_status(root: Path, spec_filter: str | None) -> int:
    has_const = (root / "docs" / "constitution.md").exists()
    specs_root = root / "specs"
    specs: list[dict[str, Any]] = []

    if specs_root.exists():
        for d in sorted(p for p in specs_root.iterdir() if p.is_dir()):
            if spec_filter and spec_filter.lower() not in d.name.lower():
                continue
            specs.append(parse_spec_dir(d))

    report = {
        "workspace": str(root),
        "has_constitution": has_const,
        "has_memory": (root / "MEMORY.md").exists(),
        "specs_count": len(specs),
        "specs": specs,
        "recommended_first_step": None if has_const else "/sdd-constitution",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def sanitize_slug(slug: str) -> str:
    slug = slug.strip().lower()
    slug = re.sub(r"^\d{3}-", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug or "nueva-spec"


def cmd_next_id(root: Path, slug: str | None, mkdir: bool) -> int:
    specs_root = root / "specs"
    max_num = 0
    if specs_root.exists():
        for d in specs_root.iterdir():
            if d.is_dir():
                m = re.match(r"^(\d{3})-", d.name)
                if m:
                    max_num = max(max_num, int(m.group(1)))
    next_prefix = f"{max_num + 1:03d}"
    folder_name = f"{next_prefix}-{sanitize_slug(slug)}" if slug else next_prefix
    target_path = specs_root / folder_name

    if mkdir:
        (root / "docs").mkdir(parents=True, exist_ok=True)
        target_path.mkdir(parents=True, exist_ok=True)

    print(
        json.dumps(
            {
                "next_number": next_prefix,
                "folder_name": folder_name,
                "relative_path": f"specs/{folder_name}",
                "created": mkdir,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SDD Helper for AGY IDE")
    parser.add_argument("--root", default=".", help="Project root directory (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Get SDD status for all or matching specs")
    p_status.add_argument("spec_filter", nargs="?", default=None, help="Optional spec folder filter")

    sub.add_parser("detect-stack", help="Detect project language and test runner")

    p_next = sub.add_parser("next-id", help="Get next 3-digit spec ID and folder name")
    p_next.add_argument("slug", nargs="?", default=None, help="Feature slug (e.g. heat-map)")
    p_next.add_argument("--mkdir", action="store_true", help="Create docs/ and specs/NNN-slug/ directories")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if args.command == "status":
        return cmd_status(root, args.spec_filter)
    if args.command == "detect-stack":
        print(json.dumps(detect_stack(root), indent=2, ensure_ascii=False))
        return 0
    if args.command == "next-id":
        return cmd_next_id(root, args.slug, args.mkdir)
    return 1


if __name__ == "__main__":
    sys.exit(main())
