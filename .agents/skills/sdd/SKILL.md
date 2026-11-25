---
name: sdd
description: >-
  Metodología Spec-Driven Development (SDD) optimizada para Google Antigravity
  (AGY IDE). Úsala siempre que trabajes con desarrollo guiado por especificaciones
  (docs/constitution.md, MEMORY.md o cualquier archivo dentro de specs/): crear la
  constitución del proyecto, entrevistar y redactar specs en notación EARS, auditar
  ambigüedades como QA, diseñar planes técnicos, desglosar tareas atómicas,
  implementar mediante TDD (una tarea a la vez) o validar requisitos con tests y
  navegador.
---

# Spec-Driven Development (SDD) para AGY IDE

Este skill implementa el flujo completo de **Spec-Driven Development (SDD)** bajo el enfoque **Spec-anchored** (la especificación se mantiene viva y gobierna la evolución del código), adaptado a las capacidades nativas de **Google Antigravity (AGY IDE)**.

## 1. Flujo SDD y Reglas de Oro

```text
Constitución → Especificación → Clarificación → Planificación → Tareas → Implementación → Validación → Cambio (Loop)
```

1. **Compuerta de aprobación estricta**: **Nunca** avances a la siguiente fase ni generes archivos de fases posteriores sin la aprobación explícita del usuario.
2. **La spec manda**: Nada se implementa en el código si no está definido en la spec activa (`specs/NNN-nombre/spec.md`). Si falta una decisión o encuentras un caso gris, **detente y pregunta** (usando `ask_question`).
3. **Spec-anchored (cambios de requisitos)**: Cualquier cambio funcional se aplica primero en `spec.md`, luego se propaga a `plan.md` y `tasks.md`, y recién al final al código.
4. **Prohibido tocar código antes de la Fase 6**: Durante Constitución, Especificación, Clarificación, Planificación, Tareas, Cambio y Estado está estrictamente prohibido crear o editar código fuente del proyecto.
5. **Estructura estándar en el proyecto**:
   ```text
   <proyecto>/
   ├── AGENTS.md (o GEMINI.md)    # Reglas siempre activas del proyecto en AGY IDE
   ├── MEMORY.md                  # Estado vivo del proyecto y fase actual
   ├── docs/
   │   └── constitution.md        # Principios innegociables (una vez por proyecto)
   └── specs/
       └── NNN-nombre-funcionalidad/
           ├── spec.md            # QUÉ y POR QUÉ (Requisitos EARS)
           ├── plan.md            # CÓMO técnico y estrategia de tests
           └── tasks.md           # Tareas atómicas verificables (20-30 min)
   ```
6. **Memoria viva**: Al concluir y aprobarse cada fase (o cada tarea implementada), actualiza `MEMORY.md` con el estado actual y el siguiente paso.

---

## 2. Integración Nativa con AGY IDE

Aprovecha siempre las herramientas propias de Antigravity en lugar de flujos manuales de texto plano:

- **Entrevistas sin fricción (`ask_question`)**: Al levantar requisitos (`/sdd-spec`) o resolver dudas marcadas como `[NECESITA ACLARACIÓN]`, utiliza `ask_question` cuando existan opciones claras de diseño (marcando la recomendada con `(Recommended)`), o haz preguntas concretas de una en una si son abiertas. También puedes sugerir `/grill-me` para funcionalidades complejas.
- **Progreso en vivo (`update_steps` y `update_focus`)**: En fases multi-paso (`/sdd-plan`, `/sdd-implement`, `/sdd-validate`), mantén actualizado el checklist visual de AGY IDE mediante `update_steps` y el estado con `update_focus`.
- **Auditoría QA imparcial (`research` subagent)**: En proyectos grandes durante `/sdd-clarify`, puedes delegar la lectura cruzada de `spec.md` vs `docs/constitution.md` al subagente `research` (`invoke_subagent` con `TypeName: "research"`) para obtener una revisión sin sesgo de autor.
- **Documentación actualizada (`context7`)**: Si el proyecto usa librerías o frameworks externos, consulta el servidor MCP de Context7 durante `/sdd-plan` y `/sdd-implement` antes de asumir firmas de APIs.
- **Validación visual y móvil (`browser` subagent / `chrome-devtools-mcp`)**: En proyectos con interfaz web durante `/sdd-validate`, verifica los requisitos funcionales visuales usando el subagente `browser` o `chrome-devtools-mcp` (comprobando interacción real, consola sin errores y viewport móvil de `375px`).

---

## 3. Detección Agnóstica del Stack y Helper Script

Este skill incluye el script auxiliar [sdd_helper.py](./scripts/sdd_helper.py) (Python 3 estándar, sin dependencias). Ejecútalo desde la raíz del workspace activo:

- **Diagnosticar estado SDD y tareas**:
  `python3 <ruta-skill-sdd>/scripts/sdd_helper.py status [prefijo-o-nombre-spec]`
- **Detectar lenguaje, framework y test runner del proyecto**:
  `python3 <ruta-skill-sdd>/scripts/sdd_helper.py detect-stack`
- **Obtener siguiente ID correlativo (`001`, `002`...) o inicializar carpeta**:
  `python3 <ruta-skill-sdd>/scripts/sdd_helper.py next-id <nombre-kebab> [--mkdir]`

> [!TIP]
> Resuelve `<ruta-skill-sdd>` usando la ubicación desde la cual leíste este `SKILL.md` (ya sea `.agents/skills/sdd` en el workspace o `~/.gemini/config/skills/sdd` global).

### Política Agnóstica de Tests y Lógica Pura
- Usa siempre el **test runner nativo o configurado en el proyecto** (ej. `vitest`, `jest`, `node --test`, `pytest`, `go test ./...`, `cargo test`, `phpunit`, etc.). Si es un proyecto JS/TS sin dependencias de test, usa `node --test` por defecto sin instalar paquetes innecesarios (salvo que la constitución diga otra cosa).
- En la planificación e implementación, exige **separación entre lógica de dominio e infraestructura/UI**: extrae cálculos y reglas de negocio a funciones o módulos puros que reciban dependencias volátiles como parámetros (ej. fecha/hora actual `now`/`today`, configuración o estado), facilitando tests unitarios deterministas y ultrarrápidos.

---

## 4. Referencias y Plantillas Obligatorias

Antes de redactar o validar cualquier documento SDD, **lee el archivo de referencia correspondiente**:

- **Plantillas oficiales (`constitution.md`, `spec.md`, `plan.md`, `tasks.md`, `MEMORY.md`) y guía completa de sintaxis EARS en español**:
  Lee [templates-and-ears.md](./references/templates-and-ears.md).
- **Reglas base para `AGENTS.md` / `GEMINI.md` del proyecto**:
  Consulta [AGENTS.sdd-snippet.md](./resources/AGENTS.sdd-snippet.md) al configurar la constitución en Fase 1.

---

## 5. Comandos Disponibles en la Suite SDD

Si el usuario invoca `/sdd` directamente indicando una acción o sin recordar el comando específico, oriéntalo o ejecuta la fase solicitada siguiendo el protocolo del comando respectivo:

| Comando Slash en AGY IDE | Uso típico | Fase SDD | Modifica código |
| :--- | :--- | :--- | :--- |
| `/sdd-constitution` | `/sdd-constitution [contexto]` | 1. Constitución | No |
| `/sdd-spec` | `/sdd-spec 001-nombre <idea inicial>` | 2. Especificación (EARS) | No |
| `/sdd-clarify` | `/sdd-clarify 001-nombre` | 3. Clarificación (QA) | No |
| `/sdd-plan` | `/sdd-plan 001-nombre` | 4. Planificación técnica | No |
| `/sdd-tasks` | `/sdd-tasks 001-nombre` | 5. Desglose de tareas | No |
| `/sdd-implement` | `/sdd-implement 001-nombre T1` | 6. Implementación (TDD) | **Sí (1 tarea)** |
| `/sdd-validate` | `/sdd-validate 001-nombre` | 7. Validación (Tests + UI) | No (solo audita) |
| `/sdd-change` | `/sdd-change 001-nombre <cambio>` | Mantenimiento Spec-anchored | No |
| `/sdd-status` | `/sdd-status [001-nombre]` | Estado actual y siguiente paso | No |
