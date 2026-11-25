---
name: sdd-status
description: >-
  SDD · Estado y Diagnóstico: Muestra en pocas líneas en qué fase del flujo SDD se
  encuentra una spec (o el proyecto), cuántas tareas lleva completadas y cuál es el
  siguiente comando /sdd-* exacto a ejecutar, sin modificar ningún archivo. Úsala
  cuando el usuario ejecute /sdd-status.
---

# SDD Diagnóstico · Dónde Estamos (`/sdd-status`)

Informa de forma ejecutiva y rápida el estado actual del proyecto o de una spec dentro del flujo [sdd](../sdd/SKILL.md).

> [!IMPORTANT]
> **Modo solo lectura**: NO modifiques ni crees ningún archivo bajo ninguna circunstancia.

## Procedimiento

1. **Inspección rápida**:
   - Ejecuta `python3 <ruta-skills>/sdd/scripts/sdd_helper.py status [filtro-opcional]` pasando el argumento que el usuario haya escrito tras `/sdd-status` (si escribió alguno).
   - Lee `MEMORY.md` (si existe) y revisa brevemente los archivos de `specs/<NNN-nombre>/` (`spec.md`, `plan.md`, `tasks.md`) de la spec consultada para confirmar matices de estado.

2. **Respuesta ultraconcisa (en pocas líneas)**:
   Responde directamente con estos 3 puntos exactos:
   1. **Fase actual y estado**: En qué paso del flujo SDD está la spec (y si existe `docs/constitution.md` y dudas `[NECESITA ACLARACIÓN]`).
   2. **Progreso de tareas**: Tareas completadas y pendientes (`x de y`), indicando el nombre de la próxima tarea pendiente si aplica.
   3. **Siguiente paso exacto**: El comando `/sdd-*` listo para copiar y ejecutar en AGY IDE.
