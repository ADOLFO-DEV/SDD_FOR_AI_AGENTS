---
name: sdd-change
description: >-
  SDD · Mantenimiento Spec-anchored: Incorpora un nuevo requisito o cambio funcional
  actualizando primero specs/NNN-nombre/spec.md en EARS y analizando el impacto en
  plan.md y tasks.md antes de tocar código. Úsala cuando el usuario ejecute /sdd-change.
---

# SDD Mantenimiento · Cambio de Requisitos (`/sdd-change`)

Aplica el principio **Spec-anchored** de [sdd](../sdd/SKILL.md): todo cambio de comportamiento entra primero en la especificación, luego en el plan y las tareas, y recién al final en el código.

> [!IMPORTANT]
> **PROHIBIDO tocar archivos de código fuente, `plan.md` o `tasks.md` en este paso.** Solo actualiza `specs/<NNN-nombre>/spec.md` y espera la aprobación del diff.

## Interpretación de parámetros
Extrae del mensaje del usuario tras `/sdd-change`:
- **Carpeta de la spec**: `<NNN-nombre>` (ej. `002-mapa-calor`). Si solo existe una spec o el usuario omitió el nombre, identifícala con `sdd_helper.py status` o confirma con `ask_question`.
- **Nuevo requisito o cambio**: el texto descriptivo con la modificación deseada.

## Procedimiento paso a paso

1. **Lectura de impacto**:
   - Lee `docs/constitution.md`, `specs/<NNN-nombre>/spec.md`, `specs/<NNN-nombre>/plan.md` y `specs/<NNN-nombre>/tasks.md` (los que existan), más las reglas EARS en [templates-and-ears.md](../sdd/references/templates-and-ears.md).
   - Si el nuevo requisito es ambiguo o contradice `docs/constitution.md` u otro `RF-x`, haz como máximo 1–2 preguntas puntuales con `ask_question` antes de editar `spec.md`.

2. **Actualización exclusiva de `specs/<NNN-nombre>/spec.md`**:
   - Añade el nuevo `RF-x` (o modifica el `RF-x` existente) estrictamente en **notación EARS en español** y con criterios verificables.
   - Actualiza en `spec.md` las secciones afectadas: Historias de usuario, Casos límite, Fuera de alcance, Criterios de finalización y cambia `Estado:` a `borrador (en revisión de cambio)` si ya estaba implementada.

3. **Análisis de impacto aguas abajo (sin editarlos aún)**:
   - Indica con precisión qué secciones y funciones de `specs/<NNN-nombre>/plan.md` habrá que modificar después.
   - Indica qué tareas nuevas (`Tn`) o ajustes en `specs/<NNN-nombre>/tasks.md` serán necesarios.

4. **Revisión de Diff y Compuerta de Aprobación**:
   - Muestra en tu respuesta un bloque `diff` claro con los cambios realizados en `spec.md` (el usuario también podrá inspeccionarlos en el Visual Diff Overlay de AGY IDE).
   - **Detente y espera la aprobación explícita del usuario** antes de propagar el cambio a `/sdd-plan` y `/sdd-tasks`.
