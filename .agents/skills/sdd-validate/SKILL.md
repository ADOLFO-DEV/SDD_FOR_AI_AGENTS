---
name: sdd-validate
description: >-
  SDD · Fase 7: Valida la especificación (specs/NNN-nombre/spec.md) requisito por
  requisito ejecutando la suite de tests automatizados y verificando la interfaz
  con el subagente Browser o Chrome DevTools MCP (incluida vista móvil 375px).
  Úsala cuando el usuario ejecute /sdd-validate.
---

# SDD Fase 7 · Validación Integral RF por RF (`/sdd-validate`)

Audita y verifica de extremo a extremo si la implementación cumple `specs/<NNN-nombre>/spec.md` y `docs/constitution.md` siguiendo [sdd](../sdd/SKILL.md).

> [!IMPORTANT]
> **Modo auditoría y veredicto**: Si algún requisito funcional (`RF-x`), no funcional o criterio de finalización no está cubierto o falla, **repórtalo con total claridad, pero NO modifiques código fuente para arreglarlo todavía**. Espera instrucciones del usuario tras emitir el veredicto.

## Interpretación de parámetros
- Identifica `specs/<NNN-nombre>/` del argumento del usuario (o localízala mediante `sdd_helper.py status`).

## Procedimiento de Validación en AGY IDE

Usa `update_steps` y `update_focus` para mostrar el progreso de validación en vivo:

1. **Cargar especificación y ejecutar suite de tests**:
   - Lee `docs/constitution.md`, `specs/<NNN-nombre>/spec.md`, `specs/<NNN-nombre>/plan.md` y `specs/<NNN-nombre>/tasks.md`.
   - Comprueba si queda alguna tarea `- [ ]` sin completar en `tasks.md` y adviértelo si es el caso.
   - Ejecuta el comando oficial de tests del proyecto (ej. `node --test`, `npx vitest run`, `pytest`, `go test ./...`) y captura la salida real.

2. **Trazabilidad Requisito por Requisito (`RF-1` … `RF-n`)**:
   - Recorre **cada `RF-x`** de `spec.md` uno por uno.
   - Indica para cada `RF-x`:
     - Qué test(s) automatizado(s) concreto(s) (archivo y nombre del test) lo cubren.
     - El resultado real de su ejecución (`PASS` / `FAIL` / `SIN COBERTURA`).

3. **Validación de Interfaz y Vista Móvil (si el proyecto tiene UI web)**:
   - Para los `RF-x` visuales, de interacción DOM o responsive que no puedan verificarse solo con tests unitarios:
     - Levanta el servidor local si hace falta (o abre el `index.html` correspondiente) y verifica mediante el **subagente `browser`** (`invoke_subagent` con `TypeName: "browser"`) o las herramientas de **`chrome-devtools-mcp`**:
       1. Prueba interactiva del flujo principal y casos de error visibles.
       2. Revisión de la consola del navegador confirmando **cero errores**.
       3. Comprobación en **vista móvil (`375px` de ancho)** asegurando que no haya roturas de layout ni elementos inaccesibles.

4. **Criterios de Finalización y Veredicto Final**:
   - Evalúa uno por uno los puntos de `## Criterios de finalización` y el cumplimiento de `docs/constitution.md`.
   - Presenta una tabla resumen de trazabilidad (`RF-x` | Método de verificación | Estado) y emite un veredicto explícito:
     - **`VEREDICTO: SPEC CUMPLIDA`** (si el 100% de RF y criterios pasan en verde; en ese caso pregunta si deseas marcar `Estado: implementada` en `spec.md` y archivarla en el historial de `MEMORY.md`).
     - **`VEREDICTO: SPEC NO CUMPLIDA`** (detallando exactamente qué falló o faltó cubrir, sin tocar código aún).
