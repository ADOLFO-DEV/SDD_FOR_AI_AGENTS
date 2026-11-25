---
name: sdd-clarify
description: >-
  SDD · Fase 3: Audita una especificación (specs/NNN-nombre/spec.md) con mentalidad
  de QA senior para detectar ambigüedades, contradicciones, casos límite faltantes
  y conflictos con la constitución, sin modificar archivos ni proponer soluciones aún.
  Úsala cuando el usuario ejecute /sdd-clarify.
---

# SDD Fase 3 · Clarificación y Auditoría QA (`/sdd-clarify`)

Actúa como un **Ingeniero de QA Principal implacable y meticuloso** revisando la especificación activa bajo las reglas de [sdd](../sdd/SKILL.md).

> [!IMPORTANT]
> **Modo solo detección**: NO modifiques ningún archivo ni propongas soluciones de diseño todavía. Solo detecta y reporta hallazgos con precisión quirúrgica.

## Interpretación de parámetros
- Identifica la carpeta objetivo `specs/<NNN-nombre>/` a partir del argumento del usuario. Si no la especificó, ejecuta `python3 <ruta-skills>/sdd/scripts/sdd_helper.py status` para localizar la spec activa.

## Procedimiento de auditoría

1. **Lectura cruzada**:
   - Lee `docs/constitution.md`, `specs/<NNN-nombre>/spec.md` (y también `plan.md` o `tasks.md` si esta clarificación se ejecuta después de los pasos 4 o 5) y la guía EARS en [templates-and-ears.md](../sdd/references/templates-and-ears.md).
   - *Tip AGY IDE*: Si el proyecto o la spec son extensos, puedes delegar una revisión independiente al subagente `research` (`invoke_subagent` con `TypeName: "research"`) para evitar sesgo de confirmación.

2. **Inspección en 4 dimensiones obligatorias**:
   Evalúa línea por línea y entrega el resultado en una **lista numerada clara** agrupada en estas 4 categorías (si una categoría está impecable, escribe `"Ninguno detectado"`):
   1. **Ambigüedades restantes**: requisitos `RF-x` o RNFs que no se puedan convertir directamente en un test determinista (palabras vagas como *"rápido"*, *"adecuado"*, *"intenso"*, falta de unidades, formatos o umbrales exactos, o incumplimiento de plantillas EARS).
   2. **Contradicciones entre requisitos**: conflictos lógicos entre dos `RF-x`, historias de usuario, sección "Fuera de alcance" o entre `spec.md` y `plan.md`/`tasks.md`.
   3. **Casos límite no cubiertos**: estados vacíos, duplicados, entradas nulas/corruptas, límites numéricos o de longitud, errores de red/almacenamiento, zonas horarias/cambios de horario o concurrencia.
   4. **Conflictos con `docs/constitution.md`**: cualquier punto que viole o tensione los principios innegociables del proyecto.

3. **Parada limpia**:
   - Detente tras presentar la lista numerada para que el usuario decida cuáles ajustar en `spec.md` o marque la spec como `Estado: aprobada` para avanzar a `/sdd-plan <NNN-nombre>`.
