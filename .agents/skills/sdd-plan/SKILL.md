---
name: sdd-plan
description: >-
  SDD · Fase 4: Genera el plan técnico detallado (specs/NNN-nombre/plan.md) a partir
  de una especificación aprobada, definiendo archivos, funciones puras, pseudocódigo,
  decisiones justificadas y estrategia de tests mapeada a cada RF. Úsala cuando el
  usuario ejecute /sdd-plan.
---

# SDD Fase 4 · Planificación Técnica (`/sdd-plan`)

Vamos a traducir una especificación funcional aprobada en el diseño técnico `specs/<NNN-nombre>/plan.md` siguiendo [sdd](../sdd/SKILL.md).

> [!IMPORTANT]
> **PROHIBIDO escribir o modificar código fuente del proyecto en esta fase.** Solo se trabaja sobre la documentación de la spec y `MEMORY.md`.

## Interpretación de parámetros
- Identifica `specs/<NNN-nombre>/` del argumento del usuario (o detéctala con `sdd_helper.py status` si solo hay una spec activa).

## Procedimiento paso a paso

1. **Verificación de compuerta previa**:
   - Lee `docs/constitution.md`, `AGENTS.md` / `GEMINI.md`, `MEMORY.md` y `specs/<NNN-nombre>/spec.md`.
   - **Validación obligatoria**: Comprueba si `spec.md` contiene algún marcador `[NECESITA ACLARACIÓN]` sin resolver o si sigue en `Estado: borrador` sin que el usuario la haya aprobado.
     - Si tiene dudas abiertas o no ha sido aprobada, **DETENTE inmediatamente y avisa al usuario** indicando exactamente qué falta aprobar o aclarar antes de generar `plan.md`.
     - Si el usuario acaba de aprobar la spec al invocar `/sdd-plan`, actualiza `Estado: aprobada` en `specs/<NNN-nombre>/spec.md`.

2. **Análisis del código y stack real**:
   - Ejecuta `python3 <ruta-skills>/sdd/scripts/sdd_helper.py detect-stack` e inspecciona los módulos actuales del proyecto que se verán afectados para reutilizar utilidades existentes.
   - Si la solución involucra APIs de librerías o frameworks externos, consulta el MCP `context7` para confirmar las firmas vigentes.
   - Usa `update_focus` en AGY IDE para informar del diseño técnico en curso.

3. **Generación de `specs/<NNN-nombre>/plan.md`**:
   - Sigue la plantilla oficial de `plan.md` en [templates-and-ears.md](../sdd/references/templates-and-ears.md), incluyendo:
     1. **Archivos que se crean o modifican** y la responsabilidad única de cada uno.
     2. **Lógica pura de dominio**: firmas de funciones/módulos puros (desacoplados de UI, red o persistencia, recibiendo dependencias volátiles como fecha/hora actual `now`/`today` por parámetro).
     3. **Algoritmo principal en pseudocódigo**, cubriendo los casos límite de la spec.
     4. **Integración con interfaz / UI / API**: cómo se renderiza o expone sin mezclar lógica de negocio.
     5. **Decisiones técnicas justificadas**, indicando explícitamente **la alternativa descartada** y por qué se descartó.
     6. **Estrategia de tests** usando el runner del proyecto (ej. `node --test`, `vitest`, `pytest`, `go test`), detallando qué casos de prueba verifican cada requisito.
   - **Trazabilidad total**: Marca explícitamente qué `RF-x` cubre cada archivo, función y bloque de tests. Asegúrate de que **todos** los `RF-x` de `spec.md` queden cubiertos y que nada viole `docs/constitution.md`.

4. **Cierre y espera de aprobación**:
   - Actualiza `MEMORY.md` y espera la aprobación explícita del usuario antes de pasar a `/sdd-tasks <NNN-nombre>`.
