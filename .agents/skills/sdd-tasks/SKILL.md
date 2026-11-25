---
name: sdd-tasks
description: >-
  SDD · Fase 5: Divide el plan técnico (plan.md) y la especificación (spec.md) en
  tareas pequeñas, ordenadas por dependencia y verificables (specs/NNN-nombre/tasks.md).
  Úsala cuando el usuario ejecute /sdd-tasks.
---

# SDD Fase 5 · Desglose de Tareas Verificables (`/sdd-tasks`)

Vamos a generar `specs/<NNN-nombre>/tasks.md` a partir de `spec.md` y `plan.md` siguiendo las reglas de [sdd](../sdd/SKILL.md).

> [!IMPORTANT]
> **PROHIBIDO escribir o modificar código fuente del proyecto en esta fase.**

## Interpretación de parámetros
- Identifica `specs/<NNN-nombre>/` del mensaje del usuario (o consulta `sdd_helper.py status` si fue omitido).

## Procedimiento paso a paso

1. **Lectura y validación previa**:
   - Lee `docs/constitution.md`, `specs/<NNN-nombre>/spec.md` y `specs/<NNN-nombre>/plan.md`, además de la plantilla de tareas en [templates-and-ears.md](../sdd/references/templates-and-ears.md).
   - Si no existe `plan.md`, detente e indica al usuario que primero debe ejecutarse y aprobarse `/sdd-plan <NNN-nombre>`.

2. **Diseño de tareas atómicas**:
   - Divide la implementación en tareas pequeñas (**equivalentes a máx. 20–30 minutos cada una**), en **estricto orden de dependencia** (primero tipos/funciones puras de lógica con sus tests unitarios, después persistencia/adaptadores, luego conexión con UI/endpoints y casos borde finales).
   - Verifica que todos los `RF-x` de `spec.md` estén asignados al menos a una tarea.
   - **Control de tamaño (máx. 10 tareas)**: Intenta que no superen las **10 tareas**. Si la complejidad exige más de 10 tareas, **avisa al usuario y propón cómo dividir la spec en dos specs más pequeñas** antes de dar por cerrado el plan de trabajo.

3. **Escritura de `specs/<NNN-nombre>/tasks.md`**:
   - Usa checkboxes Markdown con el formato exacto:
     ```markdown
     - [ ] **T1. <Descripción clara y acotada>.** (Cubre: RF-1, RF-4)
       - Hecho cuando: <comprobación objetiva y verificable ejecutando tests o inspección concreta>.
     ```

4. **Cierre y compuerta de aprobación**:
   - Actualiza `MEMORY.md` con el total de tareas generadas (`0/N`).
   - Presenta un resumen breve al usuario y espera su aprobación para iniciar la primera tarea con `/sdd-implement <NNN-nombre> T1`.
