---
name: sdd-spec
description: >-
  SDD · Fase 2: Entrevista al usuario para eliminar ambigüedades y genera la
  especificación funcional (specs/NNN-nombre/spec.md) con criterios de aceptación
  en notación EARS. Úsala cuando el usuario ejecute /sdd-spec o quiera especificar
  una nueva funcionalidad antes de planificar o programar.
---

# SDD Fase 2 · Especificación en EARS (`/sdd-spec`)

Vamos a entrevistar y redactar la especificación funcional de una característica usando la metodología [sdd](../sdd/SKILL.md).

> [!IMPORTANT]
> **PROHIBIDO escribir o modificar código fuente del proyecto en ningún momento de esta fase.**

## Interpretación de parámetros en AGY IDE
Extrae del mensaje del usuario tras `/sdd-spec`:
- **Carpeta de la spec**: primer argumento tipo `NNN-nombre` (ej. `002-mapa-calor`). Si el usuario solo dio un nombre sin número o solo describió la idea, ejecuta `python3 <ruta-skills>/sdd/scripts/sdd_helper.py next-id <slug>` para obtener el siguiente `NNN-nombre` correlativo.
- **Idea inicial**: todo el texto descriptivo restante después del nombre de la spec. Si el usuario invocó `/sdd-spec` vacío, pídele brevemente la idea inicial.

## Procedimiento paso a paso

1. **Lectura de contexto**:
   - Lee `docs/constitution.md` y `MEMORY.md`. *(Si `docs/constitution.md` no existe aún, avisa al usuario y pregúntale con `ask_question` si prefiere crear primero la constitución con `/sdd-constitution` o continuar directamente).*
   - Lee la plantilla de `spec.md` y las reglas EARS en [templates-and-ears.md](../sdd/references/templates-and-ears.md).

2. **Entrevista de descubrimiento (antes de generar el archivo)**:
   - Analiza la idea inicial buscando vacíos en: casos límite, comportamiento ante errores, métricas de criterios vagos y qué queda fuera de esta versión.
   - Haz **máximo 5 preguntas** para eliminar ambigüedades:
     - En AGY IDE, prioriza la herramienta interactiva `ask_question` cuando puedas ofrecer opciones concretas con una recomendación `(Recommended)` (el usuario también tiene campo libre "Other").
     - Si necesitas preguntas abiertas, hazlas de **UNA en UNA** para no abrumar al usuario.
   - Detente y espera las respuestas del usuario antes de escribir `spec.md`.

3. **Generación de `specs/NNN-nombre/spec.md`**:
   - Con las respuestas del usuario, crea `specs/NNN-nombre/spec.md` siguiendo exactamente la plantilla de [templates-and-ears.md](../sdd/references/templates-and-ears.md):
     - `Estado: borrador`
     - Contexto y objetivo, Usuarios/actores, Historias de usuario (`HU-x`), Definiciones (solo si aplica).
     - **Requisitos funcionales (`RF-x`) redactados estrictamente en notación EARS en español** (`CUANDO...`, `SI... ENTONCES...`, `MIENTRAS...`, `EL SISTEMA...`), 100% verificables y sin adjetivos ambiguos.
     - Requisitos no funcionales, Casos límite, Fuera de alcance, Criterios de finalización y Dudas abiertas marcadas con `[NECESITA ACLARACIÓN]`.
   - **Regla de abstracción**: Describe únicamente **el QUÉ y el POR QUÉ**. Nada de stack técnico, arquitectura, estructuras internas ni nombres de archivos de código (eso pertenece a `/sdd-plan`).

4. **Cierre de fase**:
   - Actualiza `MEMORY.md` registrando la nueva spec en borrador.
   - Presenta un resumen breve y sugiere al usuario revisarla, ejecutar `/sdd-clarify NNN-nombre` (auditoría QA) o aprobarla explícitamente para pasar a `/sdd-plan NNN-nombre`.
