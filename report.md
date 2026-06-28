# Informe del Proyecto – War is Coming

**Autor:** Cynthia Moreno Miranda  
**Curso:** MatCom, 2025–2026  

---
## Tabla de Contenidos

- [1. ¿Qué hace el programa?](#1-qué-hace-el-programa)
- [2. Diseño del programa y decisiones tomadas](#2-diseño-del-programa-y-decisiones-tomadas)
- [3. Flujo del programa](#3-flujo-del-programa)
- [4. Cómo se usa el programa (ejemplos)](#4-cómo-se-usa-el-programa-ejemplos)
- [5. Dificultades encontradas y cómo las resolví](#5-dificultades-encontradas-y-cómo-las-resolví)
- [6. Aprendizajes durante el desarrollo](#6-aprendizajes-durante-el-desarrollo)
- [7. Conclusión](#7-conclusión)
---

## 1. ¿Qué hace el programa?

*War is Coming* es un sistema de planificación de eventos militares ambientado en el universo de *Canción de Hielo y Fuego*. Permite a un comandante organizar campañas bélicas (asedios, batallas navales, asaltos, defensas, emboscadas, misiones diplomáticas y batallas campales) asignando recursos limitados —tropas de distintas casas, maquinaria de asedio, elementos especiales como Fuego Valyrio, personajes clave y recursos económicos— de forma que no se produzcan conflictos temporales ni violaciones de las reglas del universo.

El programa ofrece las siguientes funcionalidades principales:

- **Agregar eventos**: el usuario introduce el nombre, tipo, era histórica (DC o AC), ubicación, lista de recursos (por ID) y fechas de inicio y fin. El sistema valida automáticamente que los recursos existan, que las fechas sean coherentes, que no haya conflictos de recursos (ningún recurso asignado a otro evento en ese horario) y que se cumplan todas las restricciones del dominio (co‑requisitos, exclusiones mutuas, enemistades entre casas y exigencias por tipo de evento). Si todo es correcto, el evento se guarda y se asigna un ID único.
- **Búsqueda automática de huecos**: el usuario puede solicitar que el sistema encuentre el próximo intervalo de tiempo disponible para un conjunto de recursos y una duración determinada. El motor analiza el calendario existente, respetando tanto los conflictos de recursos como todas las restricciones, y sugiere una franja horaria válida.
- **Listar eventos**: muestra una tabla con todos los eventos planificados, incluyendo ID, nombre, tipo, fechas y recursos asignados.
- **Ver detalles de un evento**: a partir de un ID, muestra toda la información del evento (nombre, descripción, fechas, tipo, ubicación, recursos, estado).
- **Ver agenda de un recurso**: dado el ID de un recurso, muestra todos los eventos en los que está asignado, con sus fechas, permitiendo visualizar la ocupación de ese recurso.
- **Eliminar eventos**: elimina un evento por su ID, liberando automáticamente los recursos que ocupaba.
- **Persistencia**: todos los datos (recursos, restricciones, eventos, ID siguiente) se guardan en un archivo JSON, de modo que el estado se mantiene entre ejecuciones.

El programa está diseñado para ser usado desde la línea de comandos, con una interfaz enriquecida que utiliza colores y tablas para mejorar la experiencia de usuario.

[Volver al inicio](#tabla-de-contenidos)

---

## 2. Diseño del programa y decisiones tomadas

### 2.1 Arquitectura en capas

He organizado el código en tres capas bien diferenciadas, siguiendo el principio de separación de responsabilidades:

- **Capa de modelos** (`src/models/`): contiene las clases `Event` y `Resource`, que representan las entidades del dominio. Estas clases solo definen la estructura y métodos de conversión a/desde diccionarios, sin lógica de negocio. Esto sigue el principio de *responsabilidad única* y facilita la serialización. Cada clase implementa métodos `to_dict` y `from_dict` para la persistencia en JSON, manejando correctamente objetos `datetime` mediante `isoformat()` y `fromisoformat()`.

- **Capa de servicios** (`src/services/`): contiene la lógica de negocio.  
  - `data_manager.py` gestiona el estado global (carga/guardado de datos, operaciones CRUD). Es el punto de acceso a los datos. Mantiene listas y diccionarios en memoria (EVENTS, RESOURCES, RESTRICTIONS, NEXT_EVENT_ID) y se encarga de sincronizar con el archivo JSON. Todas las funciones de modificación (add, delete) llaman a `save_data()` para persistir los cambios inmediatamente.  
  - `planner.py` alberga el motor de validación de restricciones y el algoritmo de búsqueda de huecos. Separa la lógica de validación en funciones específicas para cada tipo de restricción, lo que facilita su mantenimiento y extensión. La función `find_next_available_time_slot` es el núcleo del planificador inteligente.

- **Capa de interfaz** (`src/interface/`): contiene los comandos CLI y el menú principal. Cada comando (`add`, `list`, `view`, `delete`) está en un archivo independiente, lo que facilita el mantenimiento y la extensión. Utiliza la librería `rich` para mostrar tablas, paneles y prompts interactivos, mejorando la usabilidad.

Esta separación de responsabilidades hace que el código sea más comprensible, mantenible y escalable. Además, permite probar la lógica de negocio de forma aislada sin depender de la interfaz.

### 2.2 Elección del dominio y modelado

Elegí el universo de *Canción de Hielo y Fuego* porque ofrece un trasfondo rico en reglas y conflictos que se prestan naturalmente a un sistema de planificación con restricciones. Los eventos son acciones militares o diplomáticas, los recursos son unidades y personajes, y las restricciones reflejan las alianzas y enemistades de la saga. Esto hace que el proyecto sea atractivo y fácil de entender para cualquier aficionado.

**Decisiones clave en el modelado:**

- **Uso de tipos de recurso en lugar de IDs**: inicialmente definí las restricciones con IDs concretos (ej. `recurso 3` requiere `recurso 7`). Esto obligaba a actualizar las reglas al añadir nuevos recursos de la misma clase (por ejemplo, una nueva maquinaria de asedio para otra casa). Opté por usar el campo `tipo` del recurso, de modo que las restricciones se aplican a cualquier recurso que tenga ese tipo, independientemente de su casa. Esto hace el sistema genérico y escalable. Por ejemplo, la restricción "Maquinaria de asedio requiere Ingeniero de asedio" se aplica a cualquier recurso cuyo tipo sea "Maquinaria de asedio" y exige que también haya un recurso de tipo "Ingeniero de asedio". Así, al añadir una nueva casa, solo se crean sus recursos con los tipos adecuados y las reglas ya funcionan.

- **Validación en el momento de agregar**: todas las validaciones (restricciones y conflictos) se realizan antes de guardar el evento. Si algo falla, se devuelve un mensaje de error y el evento no se crea. Esto garantiza que el estado siempre sea consistente y evita tener que corregir datos incorrectos posteriormente. La función `add_event` en `data_manager.py` actúa como un "control de acceso" que solo permite la inserción si se superan todas las comprobaciones.

- **Mantenimiento de orden cronológico**: la lista de eventos se mantiene ordenada por fecha de inicio mediante `bisect.insort`. Esto acelera la búsqueda de huecos y la detección de conflictos, ya que se recorren los eventos en orden temporal. Para ello, la clase `Event` implementa el método `__lt__` que compara los inicios, lo que permite a `bisect` y `sort` ordenar sin necesidad de una función `key` explícita.

- **Persistencia automática**: cada cambio en el estado (agregar o eliminar evento) se guarda inmediatamente en el archivo JSON. Esto evita pérdidas de datos y permite retomar la planificación en cualquier momento. El archivo se almacena en `data/war_planner.json`, y si no existe al inicio, se carga `default_data.json` para tener un conjunto de recursos y restricciones predefinidos.

- **Interfaz de consola enriquecida**: elegí la librería `rich` porque ofrece tablas, colores y paneles sin la complejidad de una GUI. Los mensajes de error en rojo y los textos en verde para éxito mejoran la usabilidad. Además, los prompts interactivos guían al usuario paso a paso, con validación de entrada para evitar errores de formato.

- **Manejo de errores robusto**: toda entrada del usuario se valida con bucles `while True` y `try-except`, asegurando que el programa nunca falle por datos incorrectos. Las fechas se piden por separado (año, mes, día, hora, minuto) para simplificar la entrada y evitar problemas con formatos.

### 2.3 Restricciones implementadas

El corazón del proyecto son las reglas que dictan cómo se pueden combinar los recursos. He definido tres tipos de restricciones, todas evaluadas al agregar un evento y durante la búsqueda de huecos:

1. **Inclusiones entre recursos (co‑requisitos)**: si se usa un recurso de cierto tipo, debe incluirse otro tipo complementario. Por ejemplo:
   - `Maquinaria de asedio` requiere `Ingeniero de asedio`.
   - `Fuego Valyrio` requiere `Piromante`.
   - `Maestro de espías` requiere `Oro`.
   - `Mercenarios` requiere `Oro`.
   - `Dragón` requiere `Noble de sangre valyria`.
   - `Espada de acero valyrio` requiere `Noble`.
   - `Flota` requiere `Almirante`.

   Estas reglas reflejan necesidades logísticas y narrativas (un dragón necesita un jinete, el fuego valyrio necesita un piromante para manejarlo, etc.). Se implementan en la función `validate_resource_type_inclusion_restrictions`.

2. **Exclusiones entre recursos**: impiden combinar ciertos tipos en un mismo evento. Por ejemplo:
   - `Fuego Valyrio` no puede usarse con `Maquinaria de asedio` (riesgo de explosión).
   - `Mercenarios` no pueden coincidir con `Caballero` (códigos opuestos).
   - `Dragón` no se combina con `Maquinaria de asedio` (el dragón destruiría la maquinaria).
   - `Maestro de espías` no puede estar con `Caballero` (sigilo vs. honor).

   La lógica está en `validate_resource_type_exclusion_restrictions`.

3. **Exclusiones entre casas**: reflejan las enemistades históricas del universo. Por ejemplo, Lannister no se alía con Stark, Targaryen, Tully ni Martell; Stark no se alía con Lannister, Bolton ni Greyjoy; etc. Si un evento incluye recursos de dos casas enemigas, el sistema lo rechaza. Esta validación se realiza en `validate_houses_exclusion_restrictions`.

4. **Restricciones por tipo de evento**: cada tipo de evento obliga a incluir ciertos recursos y prohíbe otros. Por ejemplo:
   - *Asedio*: debe incluir `Maquinaria de asedio` e `Ingeniero de asedio`, además de `Arqueros` e `Infantería pesada` según la inclusión, y no puede usar caballería (exclusión).
   - *Batalla naval*: debe incluir `Almirante`, `Flota` y `Fuego Valyrio`, y no puede usar caballería.
   - *Batalla campal*: requiere `Infantería pesada`, `Caballería pesada` y `Arqueros`, y prohíbe `Maestro de espías` y `Flota`.
   - *Asalto*: requiere `Infantería pesada` y `Caballería pesada`, y prohíbe maquinaria de asedio.
   - *Defensa*: requiere `Infantería pesada` y `Arqueros`, y prohíbe caballería.
   - *Emboscada*: requiere `Infantería ligera` y `Arqueros`, y prohíbe maquinaria de asedio.
   - *Misión diplomática*: requiere `Embajador` y prohíbe maquinaria de asedio.

   Estas reglas tienen sentido táctico y hacen que la planificación sea más realista. Se implementan en `validate_event_type_inclusion_restriction` y `validate_event_type_exclusion_restriction`.

No se implementaron restricciones entre personajes porque quedaban redundantes con las de casas (por ejemplo, si Stark y Lannister ya no pueden aliarse, no hace falta prohibir a Eddard Stark con Jaime Lannister).

Todas estas restricciones se aplican de forma genérica usando los tipos de recurso, lo que facilita la adición de nuevos recursos sin modificar el código de validación. El archivo `default_data.json` contiene la definición completa de recursos y restricciones, que puede ser modificada por el usuario para adaptar el dominio.

[Volver al inicio](#tabla-de-contenidos)

---

## 3. Flujo del programa

El programa comienza en `main.py`, que llama a `main_menu.py`, donde se muestra un panel de bienvenida y un menú con las opciones. Dependiendo de la tecla pulsada (`a`, `l`, `v`, `d`, `s`), se invoca al comando correspondiente.

### 3.1 Inicialización y carga de datos

Al ejecutar `main.py`, el módulo `data_manager.py` se importa y ejecuta su función `load_data()` al final del archivo. Esta función:

- Verifica si existe el archivo `data/war_planner.json`.
- Si existe, lo carga y convierte los diccionarios de recursos en objetos `Resource` (usando `Resource.create_robject_from_dict`), y los eventos en objetos `Event` (con `Event.create_event_from_dict`). La lista de eventos se ordena cronológicamente.
- Si no existe, carga `default_data.json` (que contiene los recursos y restricciones por defecto), inicializa la lista de eventos vacía y guarda ese estado como `war_planner.json`.
- En caso de error (archivo corrupto o ausencia de default_data), se crean estructuras vacías y se guarda un archivo de datos por defecto.

Los datos se almacenan en variables globales: `RESOURCES` (diccionario id->Resource), `RESTRICTIONS` (diccionario anidado), `EVENTS` (lista de Event ordenada) y `NEXT_EVENT_ID` (entero). Cualquier operación que modifique el estado llama a `save_data()` para persistir.

### 3.2 Agregar evento (`command_add`)

Este comando es el más complejo y sigue estos pasos:

1. **Recolección de datos básicos**: se pide nombre, descripción (opcional), tipo de evento (de una lista predefinida) y ubicación (opcional). La entrada se hace con `Prompt.ask` y `Confirm.ask` de `rich` para validar respuestas.

2. **Selección de recursos**: se listan todos los recursos disponibles con sus IDs, tipos y casas. El usuario introduce los IDs separados por comas. Se valida que cada ID exista en `RESOURCES`; si hay IDs inválidos, se muestra un mensaje y se repite la pregunta. También se eliminan duplicados.

3. **Fechas**: se piden año, mes, día, hora y minuto por separado para inicio y fin. Cada entrada se valida con `try-except` para asegurar que son números dentro de rangos válidos. Se comprueba que la fecha final sea posterior a la inicial.

4. **Búsqueda de hueco (opcional)**: si el usuario lo solicita, se calcula la duración en horas del evento propuesto y se llama a `find_next_available_time_slot` (explicada en detalle abajo). Si se encuentra un hueco, se muestra y se pregunta si se desea usar; si no, se notifica y se puede volver a intentar.

5. **Validación y guardado**: se invoca `add_event` en `data_manager.py`, que:
   - Crea un objeto `Event` con los datos (el ID se toma de `NEXT_EVENT_ID`).
   - Llama a `validate_restrictions` (que a su vez llama a las cinco funciones de validación descritas en la sección 2.3).
   - Llama a `resources_conflict_check` (que usa `overlap` para detectar solapamientos y comprueba que ningún recurso del nuevo evento esté ya en algún evento que solape).
   - Si ambas validaciones son exitosas, inserta el evento en `EVENTS` usando `bisect.insort` (para mantener el orden), incrementa `NEXT_EVENT_ID` y guarda en JSON.
   - Devuelve `(True, id)` o `(False, mensaje_error)`.

6. **Resultado**: se muestra un mensaje de éxito o error.

### 3.3 Búsqueda de huecos (`find_next_available_time_slot`)

Esta función, definida en `planner.py`, es el motor de sugerencia de horarios. Su implementación es clave:

- **Entrada**: lista de IDs de recursos, duración en horas, fecha de inicio desde la que buscar (start_from), número máximo de días a mirar hacia adelante (max_days), lista de eventos existentes, diccionario de recursos, restricciones y tipo de evento (para validar restricciones).

- **Algoritmo**:
  1. Ordena los eventos por fecha de inicio (ya están ordenados, pero se usa `sorted` por seguridad).
  2. Define un límite `end_limit = start_from + timedelta(days=max_days)`.
  3. Inicializa `current_time = start_from`.
  4. Itera sobre los eventos ordenados:
     - Si el evento termina antes o igual que `current_time`, se salta (ya pasó).
     - Si hay un hueco entre `current_time` y el inicio del evento (`event.start > current_time`), calcula la duración del hueco en horas.
     - Si el hueco es suficiente para la duración requerida, crea un candidato `candidate_end = current_time + duración`.
     - Comprueba que `candidate_end <= event.start` (cabe antes del siguiente evento).
     - Llama a `is_slot_valid(current_time, candidate_end, resource_ids, sorted_events)` que verifica que ningún recurso esté ocupado en ese intervalo (usando `overlap` y pertenencia).
     - Si es válido, crea un evento temporal con esos recursos y tipo, y llama a `validate_restrictions` para comprobar que también se cumplen las reglas de restricciones. Si todo ok, devuelve `(current_time, candidate_end)`.
     - Si no cabe o no es válido, avanza `current_time` al final del evento actual si el evento usa alguno de los recursos solicitados (esto es, si hay conflicto con ese evento, no podemos empezar antes de que termine). Si no usa los recursos, el hueco podría ser válido más adelante, pero ya hemos comprobado el hueco actual; para el siguiente bucle, el `current_time` se mantiene igual si no hay conflicto, lo que permite considerar el hueco tras el evento actual.
  5. Después del bucle, comprueba si hay suficiente tiempo desde `current_time` hasta `end_limit`. Si es así, verifica el hueco final con `is_slot_valid` y `validate_restrictions`, y devuelve el intervalo si es válido.
  6. Si no se encuentra nada, devuelve `(None, None)`.

- **Optimización**: al recorrer los eventos en orden, solo se avanza cuando es necesario (cuando un evento bloquea los recursos), lo que evita comprobar todos los huecos posibles de forma exhaustiva. La función `is_slot_valid` es O(n) para cada candidato, pero el número de candidatos es bajo (uno por evento más el final).

### 3.4 Listar eventos (`command_list_planned_events`)

Obtiene la lista de eventos con `list_events()` (que devuelve una copia de `EVENTS`) y la muestra en una tabla con columnas: ID, Nombre, Tipo, Era, Descripción, Estado, Inicio, Fin, Recursos (mostrando los IDs). La tabla se genera con `rich.table.Table`.

### 3.5 Ver detalles (`command_view_details`)

Ofrece dos subopciones:
- Ver detalles de un evento: pide un ID, busca el evento con `get_event_by_id` y muestra todos sus atributos en una tabla.
- Ver agenda de un recurso: pide un ID de recurso, comprueba que exista en `RESOURCES`, obtiene los eventos que lo usan con `get_event_by_resource` (que filtra `EVENTS` por `resource_id in event.resources_ids`) y muestra una tabla con los eventos, sus fechas y estado.

### 3.6 Eliminar evento (`command_delete_event`)

Muestra la lista de eventos existentes (con ID y nombre) y pide un ID. Llama a `delete_event`, que busca el evento en `EVENTS` por índice, lo elimina con `del`, guarda los cambios y devuelve `True` si se encontró. Se muestra mensaje de éxito o error.

### 3.7 Funciones auxiliares en data_manager

Además de las operaciones principales, `data_manager.py` proporciona funciones de filtrado que pueden ser útiles para futuras extensiones:
- `get_event_by_type(event_type)`: devuelve eventos de un tipo dado.
- `get_events_in_range(start, end)`: devuelve eventos que solapan un rango de fechas.
Estas funciones no se usan directamente en la interfaz actual, pero están disponibles para ampliar la funcionalidad (por ejemplo, generar reportes por período).

[Volver al inicio](#tabla-de-contenidos)

---

## 4. Cómo se usa el programa (ejemplos)

### Ejemplo 1: Agregar un evento simple

```
¡War is Coming!
¿Cuál es su nombre, milord? Arya
Hola Arya!. A continuación los comandos para realizar acciones:
a - agregar evento
l - listar eventos
d - eliminar evento
v - ver detalles de un evento
s - salir

¿Qué acción desea realizar Arya? a

Agregar nuevo evento
Nombre del evento: 
Defensa de Invernalia
¿Desea agregar descripción al evento? 
Sí
Descripción del evento: 
Defender las murallas de Invernalia contra los caminantes blancos

Tipos de evento disponibles: Asedio, Batalla naval, Asalto, Defensa, Emboscada, Batalla campal, Misión diplomática
Tipo de evento: Defensa

¿Desea especificar una locación para el evento? Sí
Ubicación: Invernalia

Recursos disponibles:
89: Infantería pesada Stark (tipo: Infantería pesada, casa: Stark)
90: Infantería ligera Stark (tipo: Infantería ligera, casa: Stark)
93: Arqueros Stark (tipo: Arqueros, casa: Stark)
101: Eddard Stark (tipo: Noble, casa: Stark)
... (más recursos)

Ingrese los IDs de los recursos que desea agregar (separados por comas): 89,93,101

Año - Inicio: 302
Mes - Inicio [1-12]: 1
Día - Inicio [1-31]: 15
Hora - Inicio [0-23]: 8
Minuto - Inicio [0-59]: 0
Año - Fin: 302
Mes - Fin [1-12]: 1
Día - Fin [1-31]: 15
Hora - Fin [0-23]: 20
Minuto - Fin [0-59]: 0

¿Desea buscar el próximo hueco disponible para estos recursos? No
Evento 'Defensa de Invernalia' agregado con ID: 1
```

### Ejemplo 2: Búsqueda de hueco

Supongamos que queremos planificar un asedio pero no sabemos cuándo hay disponibilidad. Tras elegir `a`, introducimos los datos del evento, seleccionamos recursos (por ejemplo, maquinaria de asedio e ingeniero) y fechas de inicio y fin. Luego respondemos "Sí" a la pregunta de buscar hueco. El sistema analizará el calendario y sugerirá, por ejemplo:

```
Hueco encontrado: 302-01-20 08:00 - 302-01-20 18:00
¿Desea usar este hueco? Sí
Evento 'Asedio a Harrenhal' agregado con ID: 2
```

Si no encuentra hueco, muestra: `No se encontró un hueco disponible en los próximos días`.

### Ejemplo 3: Listar eventos

```
¿Qué acción desea realizar Arya? l
Lista de Eventos
┌────┬─────────────────────┬──────────┬─────────────────────┬─────────────────────┬──────────┐
│ ID │ Nombre              │ Tipo     │ Inicio              │ Fin                 │ Recursos │
├────┼─────────────────────┼──────────┼─────────────────────┼─────────────────────┼──────────┤
│ 1  │ Defensa de Invernalia│ Defensa  │ 302-01-15 08:00     │ 302-01-15 20:00     │ 89,93,101│
│ 2  │ Asedio a Harrenhal  │ Asedio   │ 302-01-20 08:00     │ 302-01-20 18:00     │ 7,8      │
└────┴─────────────────────┴──────────┴─────────────────────┴─────────────────────┴──────────┘
```

### Ejemplo 4: Ver detalles de un evento

```
¿Qué acción desea realizar Arya? v
Seleccione una acción:
  e - ver detalles de un evento
  r - ver agenda de un recurso
  s - salir
Acción: e
Introduzca el ID del evento para mostrar los detalles: 1
Detalles del evento número 1
┌────────────┬──────────────────────────────┐
│ Campo      │ Valor                        │
├────────────┼──────────────────────────────┤
│ Nombre     │ Defensa de Invernalia        │
│ Descripción│ Defender las murallas...     │
│ Tipo       │ Defensa                      │
│ Era        │ DC                           │
│ Ubicación  │ Invernalia                   │
│ Inicio     │ 302-01-15 08:00              │
│ Fin        │ 302-01-15 20:00              │
│ Duración   │ 12:00:00                     │
│ Recursos   │ 89, 93, 101                  │
│ Estado     │ planned                      │
└────────────┴──────────────────────────────┘
```

### Ejemplo 5: Ver agenda de un recurso

```
Acción: r
Introduzca el id del recurso: 89
Agenda del recurso: Infantería pesada Stark (ID: 89)
┌───────────┬─────────────────────┬──────────┬──────┬─────────────────────┬─────────────────────┬─────────┐
│ Evento ID │ Nombre              │ Tipo     │ Era  │ Inicio              │ Fin                 │ Estado  │
├───────────┼─────────────────────┼──────────┼──────┼─────────────────────┼─────────────────────┼─────────┤
│ 1         │ Defensa de Invernalia│ Defensa  │ DC   │ 302-01-15 08:00     │ 302-01-15 20:00     │ planned │
└───────────┴─────────────────────┴──────────┴──────┴─────────────────────┴─────────────────────┴─────────┘
```

### Ejemplo 6: Eliminar evento

```
¿Qué acción desea realizar Arya? d
Eventos existentes:
ID: 1 - Defensa de Invernalia (302-01-15 08:00)
ID: 2 - Asedio a Harrenhal (302-01-20 08:00)
Introduzca el id del evento que desea eliminar o presione 's' para salir: 2
Evento 2 eliminado satisfactoriamente :)
```

[Volver al inicio](#tabla-de-contenidos)

---

## 5. Dificultades encontradas y cómo las resolví

### 5.1 Gestión de fechas y validación de intervalos
Al principio, el usuario introducía fechas como texto y era complejo validar el formato. Opté por pedir año, mes, día, hora y minuto por separado, con bucles que repiten la pregunta hasta que los datos sean válidos. Esto simplificó el código y mejoró la experiencia de usuario. Además, utilicé `datetime.fromisoformat` para cargar fechas desde JSON y `datetime.isoformat` para guardarlas, asegurando un formato estándar.

### 5.2 Restricciones genéricas vs. específicas
Inicialmente definí las restricciones con IDs de recursos concretos. Al añadir una nueva casa (por ejemplo, Targaryen), tenía que duplicar todas las reglas. Decidí usar el campo `tipo` del recurso en lugar de su ID. Así, la restricción "Maquinaria de asedio requiere Ingeniero de asedio" se aplica a cualquier recurso que tenga ese tipo, sea de la casa que sea. Esto hizo el sistema más escalable y redujo la duplicación.

### 5.3 Validación de restricciones durante la búsqueda de huecos
El algoritmo inicial solo comprobaba conflictos de recursos, pero no restricciones. Podía sugerir un hueco donde, por ejemplo, se mezclaran casas enemigas. Añadí una llamada a `validate_restrictions` dentro de la búsqueda, creando un evento temporal con los recursos y tipo solicitados. Si fallaba, se descartaba el hueco y se seguía buscando. Esto asegura que el hueco sugerido cumpla todas las reglas.

### 5.4 Indentación y typos en el código
En `planner.py`, el bucle de búsqueda de huecos tenía una indentación incorrecta: solo evaluaba el último evento. Además, había un typo en la clave de las restricciones de exclusión (`rreesource_type_exclusion_restrictions`). Corregir estos detalles fue esencial para que el motor funcionara. También ajusté la función `validate_event_type_inclusion_restriction` para que recibiera el diccionario `resources` como argumento, ya que lo necesitaba para obtener los tipos de los recursos.

### 5.5 Manejo de errores en la entrada de recursos
Cuando el usuario introducía IDs que no existían, el sistema fallaba. Añadí una validación previa en `add_event` que comprueba que todos los IDs existen en el diccionario `RESOURCES`, y si no, devuelve un mensaje de error claro. En la interfaz, el bucle repite la pregunta hasta que todos los IDs sean válidos.

### 5.6 Persistencia y carga de datos por defecto
Al principio, si no existía `war_planner.json`, el programa intentaba cargar `default_data` como cadena, lo que provocaba un error. Cambié la lógica para cargar `default_data.json` con `json.load()` y, si fallaba, usar un diccionario vacío. También implementé una función `load_default_data()` auxiliar para manejar casos de error. Además, aseguré que `save_data` serialice correctamente los objetos `Resource` y `Event` usando sus métodos `to_dict`, y que maneje fechas con `default=str` para evitar errores de serialización.

### 5.7 Uso de `bisect.insort` y `__lt__`
Para mantener la lista de eventos ordenada, usé `bisect.insort`. Pero necesitaba que los objetos `Event` fueran comparables. Implementé el método `__lt__` que compara `start`. Esto me permitió usar `bisect` sin una función `key`, y también usar `sort()` en `load_data` para ordenar los eventos cargados. Aprendí que el método `__lt__` debe ser consistente con otros operadores de comparación, pero para este caso es suficiente.

### 5.8 Interfaz de usuario con `rich`
Aprender a usar `rich` (tablas, prompts, colores) llevó algo de tiempo, pero valió la pena porque la interfaz quedó mucho más atractiva y clara. Los mensajes de error en rojo y los textos en verde para éxito mejoran la usabilidad. Además, los paneles y tablas hacen que la información sea más legible. También manejé correctamente la entrada con `Prompt.ask` y `Confirm.ask`, que simplifican la validación de opciones.

[Volver al inicio](#tabla-de-contenidos)

---

## 6. Aprendizajes durante el desarrollo

Este proyecto me ha permitido en general desarrollar habilidades de manejo de errores y gestión del tiempo, así como me ha permitido adquirir conocimientos de programación en Python. A continuación, agrupo los aprendizajes en dos categorías: las herramientas y módulos específicos que aprendí a usar, y las habilidades y conceptos generales que adquirí.

### Herramientas y módulos de Python que aprendí a usar

- **`datetime` y `timedelta`**: Aprendí a manejar fechas y horas, a calcular diferencias entre instantes (duraciones) y a formatear fechas para mostrarlas al usuario. Estos conocimientos eran esenciales para validar intervalos, detectar solapamientos y calcular la duración de los eventos. También entendí cómo comparar objetos `datetime` y cómo usar `fromisoformat` para cargar desde JSON.

- **`bisect`**: Descubrí cómo mantener una lista ordenada de forma eficiente usando `bisect.insort` en lugar de usar un algoritmo de búsqueda para la inserción (como originalmente había considerado), lo que me permitió insertar nuevos eventos en la posición cronológica correcta sin tener que reordenar toda la lista cada vez. Esto mejora el rendimiento cuando hay muchos eventos.

- **Método mágico `__lt__`**: Aprendí a usar este método (el cual conocí por recomendación de una Inteligencia Artificial al consultarle) estudiándolo por GeeksforGeeks y finalmente implementándolo en la clase `Event` para definir el criterio de ordenación de los eventos (por fecha de inicio). Este método me permitió usar `sort()` y `bisect` sin necesidad de especificar una clave de ordenación cada vez, haciendo el código más limpio y legible, y facilitándome el ordenamiento cronológico de los eventos.

- **`enumerate`**: Descubrí esta función en la documentación oficial de Python y la usé para iterar sobre listas obteniendo tanto el índice como el elemento, lo cual me facilitó la tarea de buscar y eliminar eventos por su posición.

- **`isinstance`**: Aprendí a comprobar el tipo de una variable en tiempo de ejecución, lo que me ayudó a manejar entradas del usuario que podían ser cadenas o fechas, y a convertirlas adecuadamente para evitar potenciales errores. Esta función la conocí por recomendación de una Inteligencia Artificial.

- **`rich`**: Esta librería me permitió crear una interfaz de consola atractiva y funcional, con tablas, colores, paneles y prompts interactivos. Aprender a usarla mejoró notablemente la experiencia de usuario de mi programa. Esta librería se usó en la cp08 de programación, de donde pude conocerla y empezar a aprender a usarla.

- **`datetime.fromisoformat` y `datetime.isoformat`**: Utilicé estos métodos para convertir cadenas con formato ISO en objetos `datetime` y viceversa, lo que facilitó la carga y guardado de fechas desde/hacia el archivo JSON, y la validación de fechas introducidas por el usuario. Este recurso también lo descubrí por recomendación de una Inteligencia Artificial.

- **Desempaquetado de tuplas**: Esta función que descubrí en clase y luego estudié por GeeksforGeeks me permitió asignar varios valores a la vez, en una sola línea, como en `start, end = slot`, lo que hace el código más conciso y legible al trabajar con funciones que devuelven múltiples valores.

- **Comprensión de listas en Python**: Aprendí a usar la sintaxis de comprensión de listas que ofrece Python para crear nuevas listas en una sola línea de código mediante la aplicación de una expresión a cada elemento en un iterable como una lista, tupla o rango. Esta funcionalidad de Python es mucho más útil para escribir código limpio, legible y eficiente en comparación con los bucles tradicionales. La estudié en GeeksforGeeks y luego la usé a lo largo del proyecto, por ejemplo en `get_event_by_resource` y `get_events_in_range`.

- **Operador ternario en Python**: Conocí y aprendí a usar el operador ternario de Python, o expresión condicional, que es una forma compacta (en una sola línea de código) de escribir una instrucción if-else simple. Se usa para asignar un valor a una variable en función de una condición. Uso operadores ternarios a lo largo de todo el proyecto, por ejemplo para construir cadenas de recursos en las tablas.

- **Manejo de errores con `try-except`**: Implementé bloques de captura de excepciones para gestionar entradas inválidas del usuario (fechas mal formadas, IDs no numéricos) y errores de archivo, mostrando mensajes claros sin que el programa colapse. Los conocimientos que desarrollé sobre manejo de excepciones los debo al libro Curso Intensivo de Python, de Eric Matthes.

- **Persistencia con JSON**: Aprendí a serializar objetos complejos (con fechas y listas) a un formato estándar y a guardarlos en un archivo, así como a cargarlos de vuelta. Esto me permitió que el estado de la aplicación se mantuviera entre ejecuciones. Además, aprendí a usar `json.dump` con `default=str` para manejar objetos no serializables. De nuevo el libro de Eric Matthes fue un gran apoyo en el proceso de aprender a trabajar con archivos en Python.

- **Manejo de intervalos de tiempo**: Comprendí a base de prueba y error cómo comparar y solapar intervalos ([inicio, fin]) usando la condición `max(start1, start2) < min(end1, end2)`, una técnica clave para detectar conflictos de recursos y buscar huecos disponibles. Esta funcionalidad fue de las primeras en las que trabajé, el primer código que escribí no cubría todos los casos y fui puliéndolo (de forma asistida) hasta llegar a la línea de arriba.

- **Uso de `set` para eliminar duplicados**: Para evitar que el usuario introduzca el mismo recurso varias veces, usé `list(set(resources_ids))` para eliminar duplicados de forma eficiente.

### Habilidades y conceptos generales de programación

- **Encapsulamiento y modularización**: Dividí el código en módulos y funciones con responsabilidades claras (modelos, servicios, interfaz). Esto me enseñó la importancia de separar la lógica de negocio de la presentación y la persistencia, lo que facilita el mantenimiento y la extensión del proyecto. También aprendí a usar `__init__.py` para crear paquetes y organizar las importaciones.

- **Diseño de datos y modelado de dominio**: Aprendí a abstraer un dominio real en entidades (eventos, recursos) y relaciones (restricciones), definiendo atributos y métodos que reflejan fielmente el problema a resolver. Un buen modelo de datos simplifica el código y evita complejidades innecesarias. El mismo flujo natural de funciones que iba necesitando en el proyecto fue imponiendo la necesidad de organizar mejor los archivos del proyecto y modelar mejor el dominio.

- **Validación en capas**: Aprendí que es más estratégico para el funcionamiento del programa aplicar reglas de validación sobre los datos en diferentes niveles del programa. Al principio lo encontré redundante pero después entendí la necesidad de esa redundancia para evitar errores imprevistos, de modo que he ido tratando de implementar y consolidar poco a poco una arquitectura sólida de validación en capas. Por ejemplo, valido la existencia de recursos tanto en la interfaz como en `add_event` para robustez.

- **Algoritmos de búsqueda en listas ordenadas**: la búsqueda de huecos me obligó a entender cómo manejar eficientemente listas ordenadas y comprobar solapamientos. Esto me enseñó a aprovechar el orden de los datos para optimizar la búsqueda, a manejar condiciones de extremo (huecos al principio, al final, entre eventos) y a recorrer eventos de forma secuencial para encontrar espacios libres. Tratar de desarrollar esta función me hizo pensar que debía ordenar cronológicamente los eventos para operar con ellos más fácilmente.

- **Manejo de errores y robustez**: Aprendí a anticipar entradas incorrectas del usuario y a gestionar situaciones excepcionales (archivos faltantes, datos corruptos) de forma controlada, mostrando mensajes informativos en lugar de dejar que el programa falle. Esto incluye el uso de `try-except` al cargar el archivo JSON y al parsear fechas.

- **Iteración y refinamiento**: Desarrollé el proyecto de forma incremental: primero una versión básica que funcionaba, luego añadí restricciones, después la búsqueda de huecos, y finalmente estoy puliendo la interfaz y corrigiendo errores. Esto me enseñó a no buscar la perfección desde el principio, sino a construir sobre una base sólida y mejorar paso a paso.

- **Importancia de la documentación**: Escribir docstrings (para algunas funciones), comentarios y el propio informe me ayudó a esclarecer mi pensamiento y entender mejor lo que estaba haciendo y lo que no debía. Comprendí que un código bien documentado es más fácil de mantener, leer y de compartir. Tanto así que he tratado de escribir código autodocumento (self-documenting code) en todo el proyecto desde que descubrí qué era, aunque no conociendo del todo todavía las prácticas estándar al respecto.

- **Pensamiento crítico y resolución de problemas**: Enfrentarme a errores como typos en nombres de claves, indentaciones incorrectas o funciones que no retornaban lo esperado, me obligó a depurar meticulosamente y a desarrollar una actitud de análisis sistemático. Aprendí a usar el depurador y a leer los mensajes de error de Python para localizar problemas rápidamente.

- **Trabajo con Git y control de versiones**: Utilicé Git para gestionar los cambios, lo que me permitió experimentar con seguridad y volver atrás si algo salía mal. Aprendí varios comandos al enfrentar diversas situaciones en el control de versiones de mi proyecto y entendí la necesidad del uso de sistemas de control de versiones en reemplazo de carpetas con nombre "proyecto final final - ahora si".

- **Interacción con el usuario**: Diseñar una CLI amigable con `rich` me ha mostrado que incluso una consola puede ofrecer una experiencia atractiva. Los colores y tablas mejoran la legibilidad. También aprendí a usar bucles para validar entradas y a ofrecer opciones claras al usuario.

- **Uso de constantes y valores por defecto**: Definí `DEFAULT_DATA` y `FILEPATH` como constantes al inicio de `data_manager.py`, lo que facilita cambiar la ubicación de los archivos sin modificar la lógica. También usé valores por defecto en funciones como `find_next_available_time_slot` para hacerlas más flexibles.

- **Manejo de dependencias**: Aprendí a crear un archivo `requirements.txt` y un `pyproject.toml` para gestionar las dependencias del proyecto (en este caso, `rich`). Esto permite a otros usuarios instalar las dependencias fácilmente con `pip`.

En resumen, este proyecto me ha servido como un campo de prácticas para aprender habilidades esenciales de la programación, de la gestión del tiempo y de la programación en Python y me ha enseñado a abordar problemas complejos de manera estructurada y modular, pensando en la escalabilidad, la usabilidad y la robustez desde el diseño inicial.

[Volver al inicio](#tabla-de-contenidos)

---

## 7. Conclusión

*War is Coming* es un sistema funcional y coherente que cumple con todos los requisitos mínimos del proyecto:

- **Planificación de eventos** con recursos limitados.
- **Validación de restricciones** (co‑requisitos, exclusiones, por tipo de evento y por casas).
- **Búsqueda automática de huecos** que respeta conflictos y restricciones.
- **Interfaz de consola** completa y usable.
- **Persistencia** en JSON para guardar y cargar el estado.

El sistema es extensible: se pueden añadir nuevos recursos, nuevas casas, nuevas restricciones sin modificar el núcleo de la lógica. El uso de tipos en lugar de IDs hace que las reglas sean genéricas y escalables. La arquitectura en capas facilita el mantenimiento y la adición de nuevas funcionalidades.

En el futuro, me gustaría implementar funcionalidades opcionales como **recursos con cantidad** (ej. tener 5 unidades de Infantería pesada) o **eventos recurrentes** (planificar misiones diplomáticas con cierta regularidad). También podría añadir la función `update_event_status` para cambiar el estado de los eventos (ej. de "planned" a "completed") y permitir filtrar por estado. Otra mejora sería generar reportes estadísticos de uso de recursos.

En definitiva, este proyecto me ha permitido poner en práctica todos los conocimientos adquiridos durante el curso, vía clase o internet, y me ha dado la confianza para abordar sistemas más complejos en el futuro. La combinación de diseño, lógica de negocio, interfaz de usuario y persistencia ha sido un desafío completo que me ha enseñado mucho sobre el desarrollo de software.

[Volver al inicio](#tabla-de-contenidos)