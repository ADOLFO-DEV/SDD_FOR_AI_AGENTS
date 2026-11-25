# Spec-Driven Development (SDD) Suite para Google Antigravity (AGY IDE)

Suite completa de **Agent Skills y Slash Commands** de **Spec-Driven Development (SDD)** diseñada específicamente para **Google Antigravity (AGY IDE)**, basada en el método **Spec-anchored** y sintaxis **EARS (Easy Approach to Requirements Syntax)**.

---

## Adaptación Específica para AGY IDE (vs. OpenCode)

En AGY IDE, cada carpeta dentro de `.agents/skills/<nombre>/` o `~/.gemini/config/skills/<nombre>/` actúa simultáneamente como:
1. **Slash Command de primera clase** al escribir `/<nombre>` en el Chat Canvas.
2. **Skill semántica con Progressive Disclosure**, cargándose bajo demanda sin contaminar la ventana de contexto.

Además, esta suite aprovecha las capacidades nativas de AGY IDE:
- **`ask_question`**: Entrevistas interactivas en `/sdd-spec` y resolución de dudas `[NECESITA ACLARACIÓN]`.
- **`update_steps` y `update_focus`**: Seguimiento visual en vivo durante `/sdd-plan`, `/sdd-implement` y `/sdd-validate`.
- **Subagente `browser` y `chrome-devtools-mcp`**: Verificación real de interfaz web, consola sin errores y viewport móvil (`375px`) en `/sdd-validate`.
- **Subagente `research`**: Auditoría QA con contexto limpio y sin sesgo de autor en `/sdd-clarify`.
- **MCP `context7`**: Consulta de documentación actualizada de librerías durante `/sdd-plan` y `/sdd-implement`.
- **Detección agnóstica del stack (`sdd_helper.py`)**: Detecta automáticamente el lenguaje y runner de tests del proyecto (`node --test`, `vitest`, `jest`, `pytest`, `go test ./...`, `cargo test`, etc.).

---

## Estructura de la Suite

```text
.agents/skills/
├── sdd/                              # Skill maestro: flujo, reglas de oro y router
│   ├── SKILL.md
│   ├── references/
│   │   └── templates-and-ears.md     # Plantillas (constitution, spec, plan, tasks) + Guía EARS
│   ├── resources/
│   │   └── AGENTS.sdd-snippet.md     # Reglas SDD para AGENTS.md / GEMINI.md del proyecto
│   └── scripts/
│       └── sdd_helper.py             # CLI Python sin dependencias (status, detect-stack, next-id)
├── sdd-constitution/SKILL.md         # Fase 1: Principios innegociables (docs/constitution.md)
├── sdd-spec/SKILL.md                 # Fase 2: Entrevista y redacción de spec.md en EARS
├── sdd-clarify/SKILL.md              # Fase 3: Auditoría QA (detecta ambigüedades y conflictos)
├── sdd-plan/SKILL.md                 # Fase 4: Plan técnico y estrategia de tests (plan.md)
├── sdd-tasks/SKILL.md                # Fase 5: Tareas atómicas de 20-30 min (tasks.md)
├── sdd-implement/SKILL.md            # Fase 6: Implementación TDD de UNA sola tarea a la vez
├── sdd-validate/SKILL.md             # Fase 7: Validación RF por RF (tests + Browser/DevTools)
├── sdd-change/SKILL.md               # Mantenimiento Spec-anchored (primero spec, luego código)
└── sdd-status/SKILL.md               # Diagnóstico rápido de fase, tareas y siguiente comando
```

---

## Flujo de Trabajo Paso a Paso en AGY IDE

| Orden | Comando en el Chat de AGY IDE | Qué hace |
| :---: | :--- | :--- |
| **1** | `/sdd-constitution [contexto]` | Analiza el proyecto y propone `docs/constitution.md` (6 principios innegociables). Espera tu aprobación. |
| **2** | `/sdd-spec 001-mapa-calor <idea>` | Te hace hasta 5 preguntas clave y genera `specs/001-mapa-calor/spec.md` en notación EARS (QUÉ y POR QUÉ). |
| **3** | `/sdd-clarify 001-mapa-calor` | Revisa la spec como QA senior (ambigüedades, contradicciones, casos límite y choques con constitución). |
| **4** | `/sdd-plan 001-mapa-calor` | Con la spec aprobada, diseña `plan.md` (archivos, funciones puras, pseudocódigo, decisiones y tests por RF). |
| **5** | `/sdd-tasks 001-mapa-calor` | Divide el plan en `tasks.md` con checkboxes, orden de dependencia y criterio `"Hecho cuando:"`. |
| **6** | `/sdd-implement 001-mapa-calor T1` | Ejecuta **solo T1** con TDD (test en rojo → código en verde → marca `[x]` → actualiza `MEMORY.md` → para). |
| **7** | `/sdd-validate 001-mapa-calor` | Verifica cada `RF-x` con tests + Browser/Chrome DevTools (`375px` móvil + consola) y emite veredicto. |
| **Loop** | `/sdd-change 001-mapa-calor <cambio>` | Actualiza primero `spec.md` en EARS, muestra el diff e impacto en `plan.md`/`tasks.md` y espera aprobación. |
| **Info** | `/sdd-status [001-mapa-calor]` | Informa en pocas líneas en qué fase estás, tareas completadas (`x/y`) y el siguiente comando exacto. |

---

## Instalación en otros proyectos o máquinas

- **Por proyecto (versionado en Git para todo el equipo)**:
  Copia la carpeta `.agents/skills/` a la raíz de tu repositorio:
  ```bash
  mkdir -p <tu-proyecto>/.agents/skills
  cp -R .agents/skills/sdd* <tu-proyecto>/.agents/skills/
  ```
- **Global (disponible en todos los workspaces de AGY IDE en tu equipo)**:
  ```bash
  mkdir -p ~/.gemini/config/skills
  cp -R .agents/skills/sdd* ~/.gemini/config/skills/
  ```
