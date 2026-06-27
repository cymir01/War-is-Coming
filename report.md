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

- **Agregar eventos**: el usuario introduce el nombre, tipo, ubicación, lista de recursos (por ID) y fechas de inicio y fin. El sistema valida automáticamente que los recursos existan, que las fechas sean coherentes, que no haya conflictos de recursos (ningún recurso asignado a otro evento en ese horario) y que se cumplan todas las restricciones del dominio (co‑requisitos, exclusiones mutuas, enemistades entre casas y exigencias por tipo de evento). Si todo es correcto, el evento se guarda y se asigna un ID único.
- **Búsqueda automática de huecos**: el usuario puede solicitar que el sistema encuentre el próximo intervalo de tiempo disponible para un conjunto de recursos y una duración determinada. El motor analiza el calendario existente, respetando tanto los conflictos de recursos como todas las restricciones, y sugiere una franja horaria válida.
- **Listar eventos**: muestra una tabla con todos los eventos planificados, incluyendo ID, nombre, tipo, fechas y recursos asignados.
- **Ver detalles de un evento**: a partir de un ID, muestra toda la información del evento (nombre, descripción, fechas, tipo, ubicación, recursos, estado).
- **Eliminar eventos**: elimina un evento por su ID, liberando automáticamente los recursos que ocupaba.
- **Persistencia**: todos los datos (recursos, restricciones, eventos, ID siguiente) se guardan en un archivo JSON, de modo que el estado se mantiene entre ejecuciones.

El programa está diseñado para ser usado desde la línea de comandos, con una interfaz enriquecida que utiliza colores y tablas para mejorar la experiencia de usuario.

[Volver al inicio](#tabla-de-contenidos)

---

## 2. Diseño del programa y decisiones tomadas

### 2.1 Arquitectura en capas

He organizado el código en tres capas bien diferenciadas:

- **Capa de modelos** (`src/models/`): contiene las clases `Event` y `Resource`, que representan las entidades del dominio. Estas clases solo definen la estructura y métodos de conversión a/desde diccionarios, sin lógica de negocio. Esto sigue el principio de *responsabilidad única* y facilita la serialización.

- **Capa de servicios** (`src/services/`): contiene la lógica de negocio.  
  - `data_manager.py` gestiona el estado global (carga/guardado de datos, operaciones CRUD). Es el punto de acceso a los datos.  
  - `planner.py` alberga el motor de validación de restricciones y el algoritmo de búsqueda de huecos. Separar esta lógica de la persistencia permite probar y modificar el planificador sin afectar al almacenamiento.

- **Capa de interfaz** (`src/interface/`): contiene los comandos CLI y el menú principal. Cada comando (`add`, `list`, `view`, `delete`) está en un archivo independiente, lo que facilita el mantenimiento y la extensión.

Esta separación de responsabilidades hace que el código sea más comprensible, mantenible y escalable.

### 2.2 Elección del dominio y modelado

Elegí el universo de *Canción de Hielo y Fuego* porque ofrece un trasfondo rico en reglas y conflictos que se prestan naturalmente a un sistema de planificación con restricciones. Los eventos son acciones militares o diplomáticas, los recursos son unidades y personajes, y las restricciones reflejan las alianzas y enemistades de la saga. Esto hace que el proyecto sea atractivo y fácil de entender para cualquier aficionado.

**Decisiones clave en el modelado:**

- **Uso de tipos de recurso en lugar de IDs**: inicialmente definí las restricciones con IDs concretos (ej. `recurso 3` requiere `recurso 7`). Esto obligaba a actualizar las reglas al añadir nuevos recursos de la misma clase (por ejemplo, una nueva maquinaria de asedio para otra casa). Opté por usar el campo `tipo` del recurso, de modo que las restricciones se aplican a cualquier recurso que tenga ese tipo, independientemente de su casa. Esto hace el sistema genérico y escalable.

- **Validación en el momento de agregar**: todas las validaciones (restricciones y conflictos) se realizan antes de guardar el evento. Si algo falla, se devuelve un mensaje de error y el evento no se crea. Esto garantiza que el estado siempre sea consistente y evita tener que corregir datos incorrectos posteriormente.

- **Mantenimiento de orden cronológico**: la lista de eventos se mantiene ordenada por fecha de inicio mediante `bisect.insort`. Esto acelera la búsqueda de huecos y la detección de conflictos, ya que se recorren los eventos en orden temporal.

- **Persistencia automática**: cada cambio en el estado (agregar o eliminar evento) se guarda inmediatamente en el archivo JSON. Esto evita pérdidas de datos y permite retomar la planificación en cualquier momento.

- **Interfaz de consola enriquecida**: elegí la librería `rich` porque ofrece tablas, colores y paneles sin la complejidad de una GUI. Los mensajes de error en rojo y los textos en verde para éxito mejoran la usabilidad. Además, los prompts interactivos guían al usuario paso a paso.

### 2.3 Restricciones implementadas

El corazón del proyecto son las reglas que dictan cómo se pueden combinar los recursos. He definido tres tipos de restricciones, todas evaluadas al agregar un evento y durante la búsqueda de huecos:

1. **Inclusiones entre recursos (co‑requisitos)**: si se usa un recurso de cierto tipo, debe incluirse otro tipo complementario. Por ejemplo:
   - `Maquinaria de asedio` requiere `Ingeniero de asedio`.
   - `Fuego Valyrio` requiere `Piromante`.
   - `Maestro de espías` requiere `Oro`.
   - `Mercenarios` requiere `Oro`.
   - `Dragón` requiere `Noble de sangre valyria`.

   Estas reglas reflejan necesidades logísticas y narrativas (un dragón necesita un jinete, el fuego valyrio necesita un piromante para manejarlo, etc.).

2. **Exclusiones entre recursos**: impiden combinar ciertos tipos en un mismo evento. Por ejemplo:
   - `Fuego Valyrio` no puede usarse con `Maquinaria de asedio` (riesgo de explosión).
   - `Mercenarios` no pueden coincidir con `Caballero` (códigos opuestos).
   - `Dragón` no se combina con `Maquinaria de asedio` (el dragón destruiría la maquinaria).
   - `Maestro de espías` no puede estar con `Caballero` (sigilo vs. honor).

3. **Exclusiones entre casas**: reflejan las enemistades históricas del universo. Por ejemplo, Lannister no se alía con Stark, Targaryen, Tully ni Martell; Stark no se alía con Lannister, Bolton ni Greyjoy; etc. Si un evento incluye recursos de dos casas enemigas, el sistema lo rechaza.

4. **Restricciones por tipo de evento**: cada tipo de evento obliga a incluir ciertos recursos y prohíbe otros. Por ejemplo, un *Asedio* debe incluir `Maquinaria de asedio` e `Ingeniero de asedio`, y no puede usar caballería. Una *Batalla Naval* debe incluir `Almirante` y `Fuego Valyrio`, y no puede usar caballería. Estas reglas tienen sentido táctico y hacen que la planificación sea más realista.

No se implementaron restricciones entre personajes porque quedaban redundantes con las de casas (por ejemplo, si Stark y Lannister ya no pueden aliarse, no hace falta prohibir a Eddard Stark con Jaime Lannister).

Todas estas restricciones se aplican de forma genérica usando los tipos de recurso, lo que facilita la adición de nuevos recursos sin modificar el código de validación.

[Volver al inicio](#tabla-de-contenidos)

---

## 3. Flujo del programa

El programa comienza en `main_menu.py`, que muestra un panel de bienvenida y un menú con las opciones. Dependiendo de la tecla pulsada (`a`, `l`, `v`, `d`, `s`), se invoca al comando correspondiente.

### 3.1 Agregar evento (`command_add`)

1. Se pide el nombre, descripción (opcional), tipo de evento (de una lista predefinida) y ubicación (opcional).
2. Se listan todos los recursos disponibles con sus IDs, tipos y casas.
3. El usuario introduce los IDs de los recursos separados por comas.
4. Se solicitan la fecha y hora de inicio y fin. Se valida que la fecha final sea posterior a la inicial.
5. Opcionalmente, el usuario puede pedir al sistema que busque un hueco disponible. Si se solicita, se llama a `find_next_available_time_slot` con los recursos, duración, fecha de inicio, el listado de eventos existentes, el diccionario de recursos y restricciones, y el tipo de evento. Si se encuentra un hueco, se muestra y se pregunta si se desea usar.
6. Se llama a `add_event` en `data_manager.py`, que:
   - Valida que todos los recursos existan.
   - Elimina duplicados en la lista de recursos.
   - Crea un objeto `Event`.
   - Llama a `validate_restrictions` (que comprueba inclusiones, exclusiones, casas y restricciones por tipo de evento).
   - Llama a `resources_conflict_check` para verificar que ningún recurso esté ocupado en ese horario.
   - Si todo es correcto, inserta el evento en la lista ordenada, incrementa el ID y guarda en JSON.
   - Devuelve `(True, id)` o `(False, mensaje_error)`.
7. Se muestra el resultado al usuario.

### 3.2 Búsqueda de huecos (`find_next_available_time_slot`)

Esta función, en `planner.py`, realiza los siguientes pasos:

- Ordena los eventos existentes por fecha de inicio.
- Inicia desde la fecha `start_from` y avanza hasta `max_days` días después.
- Recorre los eventos en orden. Para cada evento, si hay un hueco entre el tiempo actual y el inicio del evento, comprueba si la duración del nuevo evento cabe y si no hay conflictos de recursos (usando `is_slot_valid`). Si todo está bien, **además** crea un evento temporal con los recursos y tipo solicitados y llama a `validate_restrictions` para asegurar que se cumplen todas las reglas. Si es válido, devuelve el intervalo `(start, end)`.
- Si el hueco no es válido, avanza el tiempo actual al final del evento si el evento usa alguno de los recursos solicitados.
- Al final del horizonte, comprueba si hay espacio suficiente y repite la validación.
- Si no encuentra ningún hueco, devuelve `(None, None)`.

### 3.3 Listar eventos (`command_list_planned_events`)

Obtiene la lista de eventos con `list_events()` y la muestra en una tabla con ID, nombre, tipo, fechas y recursos (IDs).

### 3.4 Ver detalles (`command_view_details`)

Pide un ID, busca el evento con `get_event_by_id` y muestra todos sus atributos en una tabla.

### 3.5 Eliminar evento (`command_delete_event`)

Pide un ID, llama a `delete_event` que lo busca y lo elimina de la lista, guardando los cambios.

[Volver al inicio](#tabla-de-contenidos)

---

## 4. Cómo se usa el programa (ejemplos)

### Ejemplo 1: Agregar un evento simple

```
¡War is Coming!
¿Cuál es tu nombre? Arya
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

Tipos de evento disponibles: Asedio, Batalla Naval, Asalto, Defensa, Emboscada, Batalla Campal, Misión diplomática
Tipo de evento: Defensa

¿Desea especificar una locación para el evento? Sí
Ubicación: Invernalia

Recursos disponibles:
89: Infantería pesada Stark (tipo: Infantería pesada, casa: Stark)
90: Infantería ligera Stark (tipo: Infantería ligera, casa: Stark)
93: Arqueros Stark (tipo: Arqueros, casa: Stark)
... (más recursos)

Ingrese los IDs de los recursos que desea separados por comas: 89,93,101
Año - Inicio: 302
Mes - Inicio: 1
Día - Inicio: 15
Hora - Inicio: 8
Minuto - Inicio: 0
Año - Fin: 302
Mes - Fin: 1
Día - Fin: 15
Hora - Fin: 20
Minuto - Fin: 0

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

### Ejemplo 4: Ver detalles

```
¿Qué acción desea realizar Arya? v
Introduzca el ID del evento para mostrar detalles o 's' para salir: 1
Detalles del evento #1
┌────────────┬──────────────────────────────┐
│ Campo      │ Valor                        │
├────────────┼──────────────────────────────┤
│ Nombre     │ Defensa de Invernalia        │
│ Descripción│ Defender las murallas...     │
│ Tipo       │ Defensa                      │
│ Ubicación  │ Invernalia                   │
│ Inicio     │ 302-01-15 08:00              │
│ Fin        │ 302-01-15 20:00              │
│ Duración   │ 12:00:00                     │
│ Recursos   │ 89, 93, 101                  │
│ Estado     │ planned                      │
└────────────┴──────────────────────────────┘
```

### Ejemplo 5: Eliminar evento

```
¿Qué acción desea realizar Arya? d
Eventos existentes:
ID: 1 - Defensa de Invernalia (302-01-15 08:00)
ID: 2 - Asedio a Harrenhal (302-01-20 08:00)
Introduzca el ID del evento a eliminar o 's' para salir: 2
Evento 2 eliminado correctamente.
```

[Volver al inicio](#tabla-de-contenidos)

---

## 5. Dificultades encontradas y cómo las resolví

### 5.1 Gestión de fechas y validación de intervalos
Al principio, el usuario introducía fechas como texto y era complejo validar el formato. Opté por pedir año, mes, día, hora y minuto por separado, con bucles que repiten la pregunta hasta que los datos sean válidos. Esto simplificó el código y mejoró la experiencia de usuario.

### 5.2 Restricciones genéricas vs. específicas
Inicialmente definí las restricciones con IDs de recursos concretos. Al añadir una nueva casa (por ejemplo, Targaryen), tenía que duplicar todas las reglas. Decidí usar el campo `tipo` del recurso en lugar de su ID. Así, la restricción "Maquinaria de asedio requiere Ingeniero de asedio" se aplica a cualquier recurso que tenga ese tipo, sea de la casa que sea. Esto hizo el sistema más escalable.

### 5.3 Validación de restricciones durante la búsqueda de huecos
El algoritmo inicial solo comprobaba conflictos de recursos, pero no restricciones. Podía sugerir un hueco donde, por ejemplo, se mezclaran casas enemigas. Añadí una llamada a `validate_restrictions` dentro de la búsqueda, creando un evento temporal con los recursos y tipo solicitados. Si fallaba, se descartaba el hueco y se seguía buscando.

### 5.4 Indentación y typos en el código
En `planner.py`, el bucle de búsqueda de huecos tenía una indentación incorrecta: solo evaluaba el último evento. Además, había un typo en la clave de las restricciones de exclusión (`rreesource_type_exclusion_restrictions`). Corregir estos detalles fue esencial para que el motor funcionara. También ajusté la función `validate_event_type_inclusion_restriction` para que recibiera el diccionario `resources` como argumento, ya que lo necesitaba para obtener los tipos de los recursos.

### 5.5 Manejo de errores en la entrada de recursos
Cuando el usuario introducía IDs que no existían, el sistema fallaba. Añadí una validación previa en `add_event` que comprueba que todos los IDs existen en el diccionario `RESOURCES`, y si no, devuelve un mensaje de error claro.

### 5.6 Persistencia y carga de datos por defecto
Al principio, si no existía `war_planner.json`, el programa intentaba usar `default_data` como cadena, lo que provocaba un error. Cambié la lógica para cargar `default_data.json` con `json.load()` y, si fallaba, usar un diccionario vacío. También implementé una función `load_default_data()` auxiliar para manejar casos de error.

### 5.7 Interfaz de usuario con `rich`
Aprender a usar `rich` (tablas, prompts, colores) llevó algo de tiempo, pero valió la pena porque la interfaz quedó mucho más atractiva y clara. Los mensajes de error en rojo y los textos en verde para éxito mejoran la usabilidad. Además, los paneles y tablas hacen que la información sea más legible.

[Volver al inicio](#tabla-de-contenidos)

---

## 6. Aprendizajes durante el desarrollo

Este proyecto me ha permitido adquirir y afianzar múltiples habilidades:

- **Modelado de dominios**: aprender a abstraer un problema real en entidades y reglas me ha enseñado la importancia de un buen diseño de datos. Un modelo claro simplifica el código y facilita la extensión.

- **Validación en capas**: separar la lógica de validación (restricciones) de la gestión de datos y de la interfaz ha hecho que el código sea más mantenible y fácil de depurar. Pude probar el planificador de forma aislada.

- **Algoritmos de búsqueda en intervalos**: la búsqueda de huecos me obligó a entender cómo manejar eficientemente listas ordenadas y comprobar solapamientos. Aprendí a usar `bisect` y a recorrer eventos de forma secuencial para encontrar espacios libres.

- **Persistencia con JSON**: trabajar con archivos JSON me ha enseñado la importancia de la serialización y cómo manejar fechas y objetos complejos. Aprendí a estructurar el archivo de datos de forma coherente.

- **Interacción con el usuario**: diseñar una CLI amigable con `rich` me ha mostrado que incluso una consola puede ofrecer una experiencia atractiva si se cuidan los detalles. Los colores y tablas mejoran la legibilidad.

- **Iteración y refinamiento**: he ido mejorando el proyecto paso a paso, añadiendo restricciones, corrigiendo errores y puliendo la interfaz. Esto me ha enseñado a no buscar la perfección desde el principio, sino a construir de forma incremental.

- **Importancia de las restricciones**: entender cómo las reglas de negocio pueden hacer que un sistema sea mucho más interesante y desafiante. Las restricciones no solo son requisitos, sino que añaden profundidad al dominio y lo hacen más realista.

- **Manejo de errores**: he aprendido a anticipar entradas incorrectas del usuario (fechas inválidas, IDs inexistentes) y a mostrar mensajes claros en lugar de dejar que el programa falle. Esto mejora la robustez de la aplicación.

Además, el hecho de haber elegido un dominio que me apasiona (el universo de ASOIAF) ha hecho que el proceso sea mucho más divertido y motivador. Cada nueva restricción que añadía me recordaba una escena de los libros o la serie, lo que daba coherencia al proyecto.

[Volver al inicio](#tabla-de-contenidos)

---

## 7. Conclusión

*War is Coming* es un sistema funcional y coherente que cumple con todos los requisitos mínimos del proyecto:

- **Planificación de eventos** con recursos limitados.
- **Validación de restricciones** (co‑requisitos, exclusiones, por tipo de evento y por casas).
- **Búsqueda automática de huecos** que respeta conflictos y restricciones.
- **Interfaz de consola** completa y usable.
- **Persistencia** en JSON para guardar y cargar el estado.

El sistema es extensible: se pueden añadir nuevos recursos, nuevas casas, nuevas restricciones sin modificar el núcleo de la lógica. El uso de tipos en lugar de IDs hace que las reglas sean genéricas y escalables.

En el futuro, me gustaría implementar funcionalidades opcionales como **recursos con cantidad** (ej. tener 5 unidades de Infantería pesada) o **eventos recurrentes** (planificar una serie de escaramuzas diarias). También podría explorar una interfaz web con Streamlit para hacerla más visual y accesible.

En definitiva, este proyecto me ha permitido poner en práctica todos los conocimientos adquiridos durante el curso y me ha dado la confianza para abordar sistemas más complejos en el futuro.

[Volver al inicio](#tabla-de-contenidos)