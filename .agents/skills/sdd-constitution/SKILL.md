---
name: sdd-constitution
description: >-
  SDD · Fase 1: Propone o revisa la constitución del proyecto (docs/constitution.md)
  con principios técnicos innegociables y verificables adaptados al stack detectado.
  Úsala cuando el usuario ejecute /sdd-constitution o pida definir los principios
  base de Spec-Driven Development del proyecto.
---

# SDD Fase 1 · Constitución del Proyecto (`/sdd-constitution`)

Vamos a crear (o revisar, si ya existe) `docs/constitution.md` siguiendo la metodología del skill [sdd](../sdd/SKILL.md).

## Entradas del usuario
Toma cualquier texto adicional que el usuario haya escrito junto al comando `/sdd-constitution` como **contexto adicional o preferencias del proyecto** (audiencia, restricciones de arquitectura, idioma preferido, etc.).

## Procedimiento paso a paso

1. **Inspección previa obligatoria (sin modificar nada)**:
   - Ejecuta `python3 <ruta-skills>/sdd/scripts/sdd_helper.py detect-stack` para detectar lenguaje, frameworks, interfaz web y test runner del repositorio.
   - Lee `AGENTS.md`, `GEMINI.md`, `MEMORY.md` y `docs/constitution.md` (los que existan) más los archivos clave de configuración/código para comprender el estado real del proyecto.
   - Consulta la plantilla de constitución en [templates-and-ears.md](../sdd/references/templates-and-ears.md).

2. **Formular propuesta concisa**:
   - Propón en el chat un borrador de `docs/constitution.md` con **6 principios innegociables, cortos y verificables** (máximo 15–20 líneas en total) que cubran:
     1. **Simplicidad y stack**: tecnologías permitidas, política de dependencias nuevas y build.
     2. **Relación entre spec y código (Spec-anchored)**: nada se implementa fuera de la spec activa; ante dudas se detiene y se pregunta.
     3. **Separación entre lógica pura e interfaz/infraestructura**: cálculos y reglas de negocio desacoplados, inyectando dependencias volátiles (como fecha/hora actual `now`/`today`) por parámetro.
     4. **Política de tests como compuerta**: runner detectado (ej. `node --test`, `vitest`, `pytest`, `go test ./...`) y prohibición de avanzar con tests en rojo.
     5. **Protección de datos y seguridad**: compatibilidad hacia atrás, validación de entradas, manejo de zonas horarias o persistencia segura.
     6. **Idioma y convenciones**: idioma del código fuente frente al idioma de interfaz y documentación SDD.
   - Si falta alguna decisión clave del usuario (por ejemplo, si el repositorio está completamente vacío y aún no hay stack definido), usa `ask_question` antes de cerrar la propuesta.

3. **Compuerta de aprobación estricta**:
   - **NO escribas ni modifiques `docs/constitution.md` todavía.**
   - Muestra también qué bloque SDD propones añadir a `AGENTS.md` (basado en [AGENTS.sdd-snippet.md](../sdd/resources/AGENTS.sdd-snippet.md)) y **espera la aprobación explícita del usuario**.
   - Recién cuando el usuario apruebe la propuesta en el siguiente turno: escribe `docs/constitution.md`, actualiza `AGENTS.md` y crea/actualiza `MEMORY.md` indicando que el siguiente paso es `/sdd-spec 001-<nombre> <idea>`.
