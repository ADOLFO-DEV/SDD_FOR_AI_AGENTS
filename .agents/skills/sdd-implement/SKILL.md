---
name: sdd-implement
description: >-
  SDD · Fase 6: Implementa UNA sola tarea de specs/NNN-nombre/tasks.md aplicando
  TDD estricto (tests primero en rojo, luego código en verde, marcar tarea y parar).
  Úsala cuando el usuario ejecute /sdd-implement.
---

# SDD Fase 6 · Implementación TDD por Tarea (`/sdd-implement`)

Implementa **ÚNICAMENTE UNA tarea** de `specs/<NNN-nombre>/tasks.md`, respetando `plan.md`, `docs/constitution.md` y el skill [sdd](../sdd/SKILL.md).

> [!CAUTION]
> **Regla de contención absoluta**: Implementa **SOLO** la tarea solicitada (`Tn`). Al terminar esa única tarea, **PÁRATE por completo**. Está estrictamente prohibido adelantar trabajo de la siguiente tarea sin una nueva orden explícita del usuario.

## Interpretación de parámetros
Extrae del mensaje del usuario tras `/sdd-implement`:
- **Carpeta de la spec** (`<NNN-nombre>`, ej. `002-mapa-calor`).
- **ID de tarea** (`<Tn>`, ej. `T1`, `T3`).
- Si falta alguno, ejecuta `python3 <ruta-skills>/sdd/scripts/sdd_helper.py status` para detectar la spec activa y la primera tarea pendiente `- [ ]`, o confirma con `ask_question` si hay más de una candidata.

## Ciclo de Ejecución TDD en AGY IDE

Registra desde el inicio tus pasos en la interfaz de AGY IDE llamando a `update_steps` y `update_focus`:

1. **Cargar contexto SDD y runner de tests**:
   - Lee `docs/constitution.md`, `AGENTS.md` / `GEMINI.md`, `specs/<NNN-nombre>/spec.md`, `specs/<NNN-nombre>/plan.md` y `specs/<NNN-nombre>/tasks.md`.
   - Verifica el comando de tests del proyecto (desde `AGENTS.md`, `constitution.md` o `sdd_helper.py detect-stack`).
   - Si encuentras una ambigüedad no resuelta en la spec o conflicto con una tarea previa no completada, **detente y pregunta** antes de tocar código.

2. **Fase ROJA (Tests primero)**:
   - Escribe primero los tests automatizados correspondientes a `Tn` (cubriendo los `RF-x` y casos límite asignados a `Tn`).
   - Ejecuta el comando de tests con `run_command` y **comprueba que los nuevos tests fallan** por el motivo esperado (funcionalidad aún no implementada).

3. **Fase VERDE y Refactor (Código mínimo y limpio)**:
   - Si usas librerías externas, verifica dudas de sintaxis con el MCP `context7`.
   - Implementa únicamente el código necesario descrito en `plan.md` para cumplir `Tn` (respetando funciones puras e inyección de parámetros como `now`/`today` donde aplique) hasta que los tests pasen.
   - Ejecuta la suite completa de tests del proyecto para garantizar **cero regresiones** y que todo esté en verde.

4. **Verificación del criterio `"Hecho cuando:"` y cierre**:
   - Comprueba que la condición `"Hecho cuando:"` de `Tn` en `tasks.md` se cumple al 100%.
   - Marca únicamente `Tn` como completada (`- [x]`) en `specs/<NNN-nombre>/tasks.md`.
   - Actualiza `MEMORY.md` con el nuevo progreso (`x de y` tareas completadas y cuál es la siguiente).
   - Muestra al usuario:
     1. El resultado real de ejecutar la suite de tests.
     2. Qué requisitos `RF-x` quedaron cubiertos con `Tn`.
     3. El comando sugerido para el siguiente paso (`/sdd-implement <NNN-nombre> <Tn+1>` o `/sdd-validate <NNN-nombre>` si era la última tarea).
   - **DETENTE AQUÍ.** No inicies la siguiente tarea.
