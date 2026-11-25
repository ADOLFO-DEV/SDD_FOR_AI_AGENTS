# Plantillas Oficiales SDD y Guía de Requisitos EARS

Este documento contiene las plantillas canónicas y reglas de redacción para todas las fases de **Spec-Driven Development (SDD)** en AGY IDE.

---

## 1. Guía de Sintaxis EARS (Easy Approach to Requirements Syntax)

**EARS** elimina la ambigüedad obligando a que **una frase equivalga exactamente a un comportamiento verificable** (casi 1:1 con un test automatizado).

### Plantillas EARS permitidas (en español)

1. **Guiado por eventos (`CUANDO`)**:
   - `RF-x: CUANDO <evento desencadenante>, EL SISTEMA <respuesta exacta / salida esperada>.`
   - *Ejemplo*: `RF-1: CUANDO el usuario guarda una sesión con duración mayor a 0 minutos, EL SISTEMA incrementa el contador diario y persiste el registro.`
2. **Comportamiento no deseado / Errores (`SI ... ENTONCES`)**:
   - `RF-x: SI <condición de error o caso anómalo>, ENTONCES EL SISTEMA <respuesta defensiva exacta>.`
   - *Ejemplo*: `RF-2: SI el usuario intenta registrar una fecha futura, ENTONCES EL SISTEMA bloquea el envío y muestra el mensaje "No puedes registrar sesiones futuras".`
3. **Guiado por estado (`MIENTRAS`)**:
   - `RF-x: MIENTRAS <estado activo>, EL SISTEMA <respuesta o restricción continua>.`
   - *Ejemplo*: `RF-3: MIENTRAS exista una petición de guardado en curso, EL SISTEMA mantiene deshabilitado el botón de envío.`
4. **Ubicuo / Permanente (`EL SISTEMA`)**:
   - `RF-x: EL SISTEMA <comportamiento invariante o permanente>.`
   - *Ejemplo*: `RF-4: EL SISTEMA almacena y calcula todas las fechas en la zona horaria local del dispositivo en formato "AAAA-MM-DD".`
5. **Opcional / Condicional de configuración (`DONDE`)** *(si aplica a feature flags/roles)*:
   - `RF-x: DONDE <característica o rol esté habilitado>, EL SISTEMA <respuesta>.`

### Anti-patrones prohibidos en requisitos
- **Adjetivos subjetivos sin métrica**: Prohibido usar *"rápido"*, *"intenso"*, *"intuitivo"*, *"bonito"*, *"seguro"* o *"adecuadamente"* sin acompañarlo de un umbral medible (ej. `< 200 ms`, `4 niveles discretos de opacidad: 0%, 30%, 60%, 100%`, `contraste mínimo WCAG AA 4.5:1`).
- **Párrafos múltiples o conectores ambiguos**: Si una frase necesita explicar tres cosas distintas, divídela en `RF-1`, `RF-2` y `RF-3`.
- **Detalles de implementación en la spec**: No menciones nombres de archivos, tablas SQL, hooks de React ni librerías en los `RF-x`. Eso pertenece exclusivamente a `plan.md`.

---

## 2. Plantilla Fase 1: Constitución (`docs/constitution.md`)

Máximo ~15-25 líneas. Debe contener principios cortos, innegociables y verificables que apliquen a toda spec, plan y tarea del repositorio.

```markdown
# Constitución — <Nombre del Proyecto>

Principios innegociables. Toda especificación, plan y tarea debe cumplirlos sin excepción.

1. **Simplicidad y stack**: <Stack oficial, política de dependencias nuevas y restricciones de arquitectura/build>.
2. **La spec manda (Spec-anchored)**: Nada se implementa si no figura en la spec activa (`specs/NNN-*/spec.md`). Ante cualquier duda o vacío, se detiene la ejecución y se pregunta.
3. **Lógica pura desacoplada**: La lógica de negocio y cálculos se escriben como funciones/módulos puros desacoplados de UI, red o almacenamiento, recibiendo dependencias volátiles (ej. fecha/hora actual) por parámetro.
4. **Tests como compuerta**: La lógica se verifica con `<comando-de-test>`. Prohibido dar por terminada una tarea o avanzar con tests en rojo.
5. **Integridad de datos y seguridad**: <Reglas sobre persistencia, compatibilidad hacia atrás, validación de entradas, zonas horarias o privacidad>.
6. **Idioma y convenciones**: <Ej. Código e identificadores en inglés; interfaz de usuario, commits y documentación SDD en español>.
```

---

## 3. Plantilla Fase 2: Especificación (`specs/NNN-nombre/spec.md`)

Recuerda: **Solo el QUÉ y el POR QUÉ**. Cero arquitectura, cero stack y cero rutas de archivos de código.

```markdown
# Spec NNN — <Nombre de la funcionalidad>

Estado: borrador | aprobada | implementada

## Contexto y objetivo
<Qué problema concreto resuelve para el usuario o negocio y por qué vale la pena construirlo ahora. Un párrafo conciso.>

## Usuarios / actores
- <Actor 1: quién interactúa y en qué contexto.>

## Historias de usuario
- HU-1: Como <rol>, quiero <acción>, para <beneficio medible>.

## Definiciones
<Opcional. Incluir solo si existen términos del dominio que puedan interpretarse de más de una manera.>

## Requisitos funcionales (criterios de aceptación en EARS)
- RF-1: CUANDO <evento>, EL SISTEMA <respuesta verificable>.
- RF-2: SI <condición no deseada / error>, ENTONCES EL SISTEMA <respuesta verificable>.
- RF-3: MIENTRAS <estado>, EL SISTEMA <respuesta verificable>.
- RF-4: EL SISTEMA <comportamiento permanente verificable>.

## Requisitos no funcionales
<Solo los que apliquen con criterios medibles: rendimiento, accesibilidad, responsive (ej. móvil 375px), seguridad, compatibilidad, idioma.>

## Casos límite
- < Estado vacío / cero datos >
- < Duplicados / límites numéricos / textos largos >
- < Datos corruptos, errores de red, zonas horarias o concurrencia >

## Fuera de alcance
- <Lo que explícitamente NO se incluye en esta iteración para evitar scope creep.>

## Criterios de finalización (Definition of Done)
- [ ] Todos los RF cubiertos por tests automatizados en verde (`<comando-de-test>`).
- [ ] RF visuales/interfaz verificados sin errores de consola (incluyendo vista móvil si aplica).
- [ ] Cero dudas abiertas en esta especificación.

## Dudas abiertas
- [NECESITA ACLARACIÓN] <Pregunta pendiente, o escribir "Ninguna" cuando todas estén resueltas.>
```

---

## 4. Plantilla Fase 4: Planificación Técnica (`specs/NNN-nombre/plan.md`)

Traduce una `spec.md` **aprobada** (sin dudas abiertas) al diseño técnico concreto, trazando siempre qué `RF-x` cubre cada componente.

```markdown
# Plan Técnico — Spec NNN: <Nombre de la funcionalidad>

## 1. Archivos y responsabilidades
| Archivo | Acción (`Crear` / `Modificar`) | Responsabilidad concreta | RF cubiertos |
| :--- | :--- | :--- | :--- |
| `<ruta/archivo>` | `Crear` / `Modificar` | <Qué hace y qué NO hace> | RF-1, RF-2 |

## 2. Lógica de dominio / Funciones puras
<Firmas de funciones/clases/módulos puros, entradas (inyectando reloj `now`/`today` o estado externo como parámetro), salidas y manejo de errores. Indica qué RF cubre cada función.>

## 3. Algoritmo principal (Pseudocódigo)
```text
<Pseudocódigo claro paso a paso para la lógica no trivial y sus casos límite>
```

## 4. Interfaz / Capa de presentación o API
<Cómo se conecta la lógica pura con el DOM/componentes UI, CLI o endpoints HTTP; estados de carga/vacío/error y comportamiento responsive si aplica. Indica RF cubiertos.>

## 5. Decisiones técnicas justificadas
- **Decisión 1**: <Qué se eligió y por qué respeta `docs/constitution.md`>.
  - *Alternativa descartada*: <Qué otra opción existía y por qué se descartó>.

## 6. Estrategia de verificación y mapeo de tests
- **Comando de ejecución**: `<comando-de-test>`
- **Casos de prueba unitarios / integración**:
  - `test("<descripción>")` → Cubre `RF-1` (caso feliz + caso límite X).
  - `test("<descripción>")` → Cubre `RF-2` (condición de error Y).
- **Verificación de interfaz / E2E** *(si aplica)*:
  - Comprobación con Browser / Chrome DevTools MCP → Cubre `RF-3`, vista `375px` y consola limpia.
```

---

## 5. Plantilla Fase 5: Tareas (`specs/NNN-nombre/tasks.md`)

Reglas:
- Tareas pequeñas (**máx. 20-30 minutos** de trabajo equivalente cada una).
- Ordenadas estrictamente por dependencia (primero modelos/funciones puras + sus tests, luego integración/UI, finalmente pulido/casos borde).
- **Máximo recomendado: 10 tareas**. Si salen más de 10, propón al usuario dividir la spec en dos iteraciones independientes antes de continuar.

```markdown
# Tareas — Spec NNN: <Nombre de la funcionalidad>

- [ ] **T1. <Descripción concisa y accionable>.** (Cubre: RF-1, RF-4)
  - Hecho cuando: <Comprobación objetiva y ejecutable, ej. los tests de X pasan en verde con `<comando>` cubriendo caso vacío y normal>.

- [ ] **T2. <Descripción concisa y accionable>.** (Cubre: RF-2)
  - Hecho cuando: <Comprobación objetiva y ejecutable>.
```

---

## 6. Plantilla de Memoria Viva (`MEMORY.md`)

Si el proyecto aún no tiene `MEMORY.md`, créalo con esta estructura ligera y mantenlo al día al cerrar cada fase:

```markdown
# Memoria del Proyecto — <Nombre>

## Estado SDD Actual
- **Constitución**: `docs/constitution.md` (vigente)
- **Spec activa**: `specs/NNN-nombre/` — Fase: `<Especificación | Clarificación | Plan | Tareas | Implementación (Tn/Tm) | Validada>`
- **Siguiente paso sugerido**: `<ej. /sdd-implement NNN-nombre T2>`

## Historial de Specs Completadas
- `NNN-nombre`: <Resumen de 1 línea de lo entregado y fecha>.

## Notas de Contexto y Decisiones Clave
- <Aprendizajes breves del código o restricciones importantes descubiertas>.
```
