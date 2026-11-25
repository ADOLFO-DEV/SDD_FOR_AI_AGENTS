## Spec-Driven Development (SDD)

### Comandos de verificación
- Tests automatizados: `<COMANDO_DE_TESTS>`
- Verificación UI (si aplica): Subagente `browser` o MCP `chrome-devtools-mcp` (funcionalidad, consola sin errores y vista móvil `375px`).

### Reglas innegociables SDD
- Lee siempre `docs/constitution.md`, `MEMORY.md` y la spec activa (`specs/NNN-*/`) antes de modificar cualquier archivo de código.
- **La spec manda**: no implementes funcionalidades ni cambios de comportamiento que no estén respaldados en `specs/NNN-*/spec.md`. Si falta una decisión, detente y pregunta.
- En implementación (`/sdd-implement`), trabaja **una sola tarea a la vez** siguiendo TDD estricto (escribe el test en rojo → implementa hasta pasar en verde → marca la tarea en `tasks.md` → actualiza `MEMORY.md` → detente).
