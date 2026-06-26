# Informe del Proyecto – War is Coming

**Autor:** Cynthia Moreno Miranda  
**Curso:** MATCOM, 2025-26

---

## 1. Introducción y dominio elegido

*War is Coming* es un sistema de planificación de eventos bélicos ambientado en el universo de *Canción de Hielo y Fuego* (la saga de George R. R. Martin). El objetivo principal es gestionar campañas militares –asedios, batallas navales, asaltos, defensas, emboscadas y batallas campales– asignando recursos limitados (tropas de distintas casas, maquinaria de asedio, elementos especiales como Fuego Valyrio, personajes clave y recursos económicos) de forma que no se produzcan conflictos temporales ni violaciones de las reglas del universo.

Se eligió este dominio porque permite modelar con claridad las nociones de **eventos** (acciones bélicas), **recursos** (unidades, personajes, suministros) y **restricciones** (co‑requisitos, exclusiones, enemistades entre casas) de una manera rica y coherente. Además, el trasfondo de la saga proporciona un conjunto de reglas narrativas que hacen el proyecto más atractivo y fácil de entender para cualquier aficionado a la serie.

La aplicación está diseñada para ser utilizada por un comandante o estratega que desee organizar sus ejércitos, evitando que dos eventos usen el mismo recurso a la vez y asegurando que las alianzas y combinaciones de tropas respeten la lógica de Poniente. El sistema también ofrece una función de búsqueda automática de huecos, que sugiere el próximo intervalo de tiempo disponible para un conjunto de recursos, facilitando la planificación.

---

## 2. Modelado del dominio

### 2.1 Eventos

Un **evento** representa una operación militar planificada. En el código, la clase `Event` (en `src/models/event.py`) contiene:

- **ID** único (entero autoincrementado).
- **Nombre** y **descripción** (opcional).
- **Intervalo de tiempo**: `start` y `end` (objetos `datetime` de la librería estándar de Python).
- **Tipo de evento**: entre *Asedio*, *Batalla Naval*, *Asalto*, *Defensa*, *Emboscada* y *Batalla Campal*.
- **Ubicación** (opcional).
- **Lista de IDs de recursos** que utiliza.
- **Estado**: *planned* (por defecto), aunque se puede extender a otros estados (ej. *en curso*, *finalizado*).

Cada evento se almacena en una lista global que se mantiene ordenada cronológicamente gracias al método `__lt__` de la clase `Event`, que compara las fechas de inicio. Esto facilita la búsqueda de huecos y la detección de conflictos, ya que los eventos se recorren en orden temporal.

### 2.2 Recursos

Los recursos son las unidades y elementos necesarios para llevar a cabo los eventos. En `src/models/resource.py`, la clase `Resource` tiene:

- **ID** único.
- **Nombre** (ej. *Infantería pesada Lannister*).
- **Tipo**: cadena que clasifica el recurso (*Infantería pesada*, *Caballería ligera*, *Maquinaria de asedio*, *Arqueros*, *Almirante*, *Maestro de espías*, *Mercenarios*, *Oro*, *Dragón*, *Fuego Valyrio*, *Piromante*, *Personaje*, *Jinete de dragón*, etc.).
- **Casa** (opcional): a qué casa noble pertenece (*Lannister*, *Stark*, *Targaryen*, *Baratheon*, *Tully*, *Martell*, *Greyjoy*, *Bolton*, *Frey*, *Arryn*).

Los recursos son **compartidos y reutilizables**: un mismo recurso no puede asignarse a dos eventos que se solapen en el tiempo. El sistema mantiene un inventario (diccionario `RESOURCES` en `data_manager.py`) que se carga desde un archivo JSON. Se han definido más de cien recursos, incluyendo diez tipos diferentes para cada casa, más recursos especiales sin casa (Mercenarios, Oro, Dragón, Fuego Valyrio) y varios personajes clave (Eddard Stark, Robb Stark, Tywin Lannister, Jaime Lannister, Cersei Lannister, Daenerys Targaryen, Jon Snow).

### 2.3 Restricciones implementadas

El corazón del proyecto son las restricciones, que garantizan que las combinaciones de recursos sean coherentes con la trama y las tácticas militares. Se han definido **cinco tipos de restricciones**, todas evaluadas en el momento de agregar un evento y también durante la búsqueda de huecos. Estas reglas son:

#### 2.3.1 Inclusiones entre recursos (co‑requisitos)

Estas reglas obligan a que, si se usa un recurso de cierto tipo, también se incluyan otros tipos complementarios. He elegido estas cinco inclusiones porque reflejan necesidades logísticas y narrativas del mundo de *Canción de Hielo y Fuego*:

| Si usas... | también debes incluir... | Razón |
|------------|--------------------------|-------|
| `Maquinaria de asedio` | `Ingeniero de asedio` | Una máquina de asedio (ariete, torre, catapulta) no puede operarse sin un experto que la construya, la mantenga y la dirija. Es un co‑requisito técnico y táctico. |
| `Fuego Valyrio` | `Piromante` | El fuego valyrio es una sustancia extremadamente volátil y peligrosa. Solo los piromantes de la Alquimia (como los de la Logia de los Piromantes) saben manejarlo con seguridad. Sin ellos, el recurso es inútil o incluso letal. |
| `Maestro de espías` | `Oro` | Un maestro de espías necesita financiación para sobornar, pagar informantes y mantener una red de agentes. Sin oro, su labor es inviable. Esta regla conecta la inteligencia con la economía. |
| `Mercenarios` | `Oro` | Las compañías de mercenarios (como la Compañía Dorada o los Segunda Espada) solo luchan por dinero. Sin pago, no hay contrato. Es una relación directa entre recurso humano y recurso monetario. |
| `Dragón` | `Jinete de dragón` | Un dragón salvaje es incontrolable. Solo una persona con sangre valyria (y entrenamiento) puede montarlo y dirigirlo en batalla. Daenerys Targaryen es el ejemplo claro; por eso se le asigna el tipo `Jinete de dragón`. |

Estas inclusiones no solo son lógicas, sino que añaden profundidad al juego, ya que fuerzan al usuario a planificar sus recursos con cuidado.

#### 2.3.2 Exclusiones entre recursos

Impiden combinar ciertos tipos de recursos en un mismo evento. He definido cuatro exclusiones mutuas que reflejan conflictos temáticos y tácticos:

| No se pueden combinar... | Razón |
|--------------------------|-------|
| `Fuego Valyrio` con `Maquinaria de asedio` | Riesgo de explosión / combustión. |
| `Mercenarios` con `Caballero` | Los mercenarios desconfían de los caballeros (códigos opuestos). |
| `Dragón` con `Maquinaria de asedio` | Un dragón destruye fácilmente la maquinaria, no se combinan. |
| `Maestro de espías` con `Caballero` | Los maestros de espías representan el sigilo y el engaño; los caballeros encarnan el honor y la lealtad. Son polos opuestos y rara vez colaboran en la saga. |

He descartado otras combinaciones (como la de maestros de espías con mercenarios o almirantes) porque no eran tan representativas o se solapaban con otras reglas. La elección final busca variedad y coherencia narrativa.

#### 2.3.3 Exclusiones entre casas

Reflejan las enemistades históricas del universo:

- **Lannister** no se alía con *Stark*, *Targaryen*, *Tully* ni *Martell*.
- **Stark** no se alía con *Lannister*, *Bolton* ni *Greyjoy*.
- **Targaryen** no se alía con *Baratheon* ni *Lannister*.
- **Tully** no se alía con *Lannister* ni *Frey*.
- **Martell** no se alía con *Lannister*.
- **Greyjoy** no se alía con *Stark*.
- **Bolton** no se alía con *Stark*.
- **Frey** no se alía con *Stark* ni *Tully*.

Si un evento incluye recursos de dos casas enemigas, el sistema lo rechaza. Esta regla es fundamental para mantener la coherencia del universo, donde las alianzas son complejas y cambiantes.

#### 2.3.4 Exclusiones entre personajes

Basadas en las relaciones personales de la saga:

| Personaje | No puede coincidir con... |
|-----------|---------------------------|
| `Eddard Stark` | `Jaime Lannister`, `Cersei Lannister` |
| `Robb Stark` | `Jaime Lannister` |
| `Tywin Lannister` | `Robb Stark`, `Eddard Stark` |
| `Jon Snow` | `Cersei Lannister` |
| `Daenerys Targaryen` | `Cersei Lannister` |

Estas exclusiones evitan que personajes enemigos compartan un mismo evento, reflejando conflictos personales que son clave en la trama.

#### 2.3.5 Restricciones por tipo de evento

Cada tipo de evento **obliga** a incluir ciertos recursos y **prohíbe** otros:

**Inclusiones forzosas:**

| Tipo de evento | Tipos de recurso obligatorios |
|----------------|-------------------------------|
| `Asedio` | `Maquinaria de asedio`, `Ingeniero de asedio` |
| `Batalla Naval` | `Almirante`, `Fuego Valyrio` |
| `Asalto` | `Infantería pesada`, `Caballería pesada` |
| `Defensa` | `Infantería pesada`, `Arqueros` |
| `Emboscada` | `Infantería ligera`, `Arqueros` |

**Exclusiones obligatorias:**

| Tipo de evento | Tipos de recurso prohibidos |
|----------------|-----------------------------|
| `Emboscada` | `Maquinaria de asedio` |
| `Batalla Naval` | `Caballería pesada`, `Caballería ligera` |
| `Asedio` | `Caballería pesada`, `Caballería ligera` |
| `Defensa` | `Caballería pesada`, `Caballería ligera` |
| `Asalto` | `Maquinaria de asedio` |

Estas reglas tienen sentido táctico: una emboscada debe ser sigilosa y no puede llevar maquinaria pesada; una batalla naval no necesita caballería; un asedio es estático, no requiere caballería; una defensa es similar; y un asalto rápido no da tiempo a montar maquinaria de asedio.

Todas estas restricciones se implementan mediante funciones de validación en `planner.py`, que recorren los tipos de los recursos seleccionados y los comparan con las tablas de restricciones. La ventaja de usar **tipos** (y no IDs) es que las reglas son genéricas y se aplican automáticamente a cualquier recurso de ese tipo, independientemente de la casa a la que pertenezca. Esto hace el sistema fácilmente extensible.

---

## 3. Arquitectura del software

La aplicación sigue una arquitectura en capas, con separación clara de responsabilidades.

### 3.1 Capas y módulos

- **`src/models/`**: contiene las clases `Event` y `Resource`, que definen la estructura de los datos. No contienen lógica de negocio, solo métodos de conversión a/desde diccionarios para la persistencia. Esto sigue el principio de *Single Responsibility*.
- **`src/services/`**: alberga la lógica de negocio.
  - `data_manager.py`: gestiona la carga/guardado del estado global (recursos, eventos, restricciones, ID siguiente) y ofrece funciones CRUD (`add_event`, `delete_event`, `list_events`, etc.). Es el punto de acceso al estado.
  - `planner.py`: contiene el motor de validación de restricciones (`validate_restrictions`), la comprobación de conflictos de recursos (`resources_conflict_check`) y el algoritmo de búsqueda de huecos (`find_next_available_time_slot`). Esta separación permite probar y modificar la lógica de planificación sin afectar a la persistencia.
- **`src/interface/`**: comandos CLI y menú principal, utilizando la librería `rich` para interfaces enriquecidas (tablas, paneles, colores). Cada comando (`add`, `list`, `delete`, `view`) está en un archivo separado, facilitando el mantenimiento.
- **`src/data/`**: contiene `default_data.py`, que define la configuración inicial de recursos y restricciones en caso de que no exista el archivo JSON. Esto proporciona un conjunto de datos de ejemplo para empezar a probar el sistema.
- **Persistencia**: se gestiona directamente en `data_manager.py` con `json`. Se guarda todo el estado en un único archivo `war_planner.json`, cumpliendo con el requisito del enunciado.

### 3.2 Decisiones de diseño

#### 3.2.1 Uso de tipos de recurso en lugar de IDs
Inicialmente, las restricciones se definían usando IDs de recursos específicos (ej. `recurso 3` y `recurso 7`). Esto obligaba a actualizar las reglas cada vez que se añadía un nuevo recurso de la misma clase (por ejemplo, una nueva maquinaria de asedio para otra casa). Decidí cambiar a **tipos de recurso** para que las reglas sean genéricas. Así, la restricción "Caballería pesada no se combina con Maquinaria de asedio" se aplica a todos los recursos que tengan esos tipos, sean de la casa que sean. Esto hace el sistema mucho más escalable y reduce el mantenimiento.

#### 3.2.2 Validación en el momento de agregar
Todas las validaciones (restricciones y conflictos) se realizan en `add_event` antes de guardar el evento. Si algo falla, se devuelve un mensaje de error y el evento no se crea. Esto garantiza que el estado siempre sea consistente y evita tener que corregir datos incorrectos posteriormente.

#### 3.2.3 Búsqueda de huecos
La función `find_next_available_time_slot` recorre los eventos ordenados cronológicamente y detecta los intervalos libres. Para cada intervalo candidato, comprueba que no haya conflictos con los recursos solicitados. Utiliza `is_slot_valid`, que verifica solapamiento con eventos existentes. Esta función es clave para la usabilidad, ya que permite al usuario encontrar rápidamente un momento disponible sin tener que probar manualmente. La búsqueda se limita a un número configurable de días hacia adelante (por defecto 30) para evitar bucles infinitos.

#### 3.2.4 Persistencia automática
Cada cambio en el estado (agregar, eliminar evento) se guarda inmediatamente en el archivo JSON. Esto evita pérdidas de datos y permite retomar la planificación en cualquier momento, cumpliendo con el requisito de persistencia del enunciado.

#### 3.2.5 Interfaz de consola enriquecida
Se eligió la librería `rich` porque ofrece tablas, colores, paneles y prompts interactivos sin la complejidad de una GUI. La interfaz es clara y usable, y los mensajes de error se muestran en rojo para llamar la atención. Esto mejora la experiencia de usuario sin añadir dependencias pesadas.

### 3.3 Principios SOLID aplicados (de forma implícita)
Aunque no se ha hecho un diseño explícito con interfaces y herencia, se han seguido buenas prácticas que se alinean con SOLID:

- **Single Responsibility**: cada módulo tiene una tarea: `data_manager` gestiona el estado, `planner` valida, `interface` se ocupa de la interacción con el usuario. Las clases `Event` y `Resource` solo representan datos.
- **Open/Closed**: el sistema de restricciones es extensible: se pueden añadir nuevas reglas simplemente agregando nuevas entradas en los diccionarios de restricciones, sin modificar el código de validación (las funciones genéricas recorren los diccionarios). Esto permite añadir nuevas reglas sin tocar el código existente.
- **Dependency Inversion**: la interfaz no depende de la implementación concreta de la persistencia; llama a funciones de `data_manager`, que podrían ser reemplazadas fácilmente si se decidiera usar otro sistema de almacenamiento.

### 3.4 Otras buenas prácticas
- **Nomenclatura**: las variables, funciones y clases están en inglés, mientras que la interfaz de usuario se presenta en español para facilitar el uso.
- **Type hints**: todas las funciones públicas incluyen anotaciones de tipo, lo que mejora la legibilidad y ayuda a detectar errores.
- **Docstrings**: cada función y clase relevante tiene una breve documentación.
- **Código limpio**: se evita la duplicación y se utilizan estructuras de datos y bucles de forma clara.

---

## 4. Funcionamiento del planificador

### 4.1 `add_event`

La función principal de planificación es `add_event` en `data_manager.py`. Realiza los siguientes pasos:

1. **Valida que los recursos existen** en el diccionario `RESOURCES`.
2. **Comprueba que la fecha final sea posterior a la inicial**.
3. **Elimina duplicados** en la lista de IDs de recursos (por si el usuario los repite).
4. **Crea un objeto `Event`** con los datos proporcionados.
5. **Valida restricciones** llamando a `validate_restrictions` (que a su vez evalúa todos los tipos de restricciones descritos anteriormente). Si alguna falla, devuelve un mensaje de error.
6. **Valida conflictos de recursos** con `resources_conflict_check` (comprueba que ningún recurso esté ocupado en ese horario). Para ello, compara el nuevo evento con todos los existentes y detecta solapamientos.
7. Si todo es correcto, inserta el evento en la lista ordenada (`bisect.insort`), incrementa el ID y guarda el estado en JSON.
8. Devuelve `(True, id)` o `(False, mensaje_error)`.

### 4.2 `find_next_available_time_slot`

Esta función busca el próximo hueco libre para un conjunto de recursos y una duración dada:

- Parte de una fecha `start_from` (por defecto, el momento actual) y mira hasta `max_days` días después.
- Ordena los eventos existentes por inicio.
- Recorre los eventos y, para cada espacio entre ellos, comprueba si la duración cabe y si no hay conflictos con los recursos. Si hay un hueco, lo devuelve.
- Si no encuentra ningún hueco, devuelve `None`.

### 4.3 `delete_event`

Elimina un evento por su ID. Busca en la lista, lo elimina y guarda el estado. Libera automáticamente los recursos, ya que la lista de eventos se actualiza y el recurso ya no estará ocupado.

### 4.4 Control de colisiones

El conflicto se detecta mediante la función `overlap` (que comprueba solapamiento de intervalos) y luego se verifica que los recursos del nuevo evento no estén en los recursos del evento solapado. Si ambas condiciones se cumplen, se considera conflicto y se rechaza el nuevo evento.

---

## 5. Interfaz de usuario

La interfaz es de línea de comandos (CLI) con la librería `rich`. Al iniciar, se muestra un panel de bienvenida y un menú con los comandos:

- **`a` (Agregar evento)**: asistente paso a paso que pregunta nombre, descripción, tipo de evento, ubicación, IDs de recursos (se muestra el inventario con sus tipos y casas), fechas de inicio y fin, y ofrece la opción de buscar hueco. Tras validar, muestra el resultado.
- **`l` (Listar eventos)**: muestra una tabla con ID, nombre, tipo, fechas y recursos de todos los eventos planificados.
- **`v` (Ver detalles)**: pide un ID y muestra toda la información del evento.
- **`d` (Eliminar evento)**: pide un ID y lo elimina, liberando recursos.
- **`s` (Salir)**: cierra la aplicación.

Todos los comandos manejan errores de entrada (fechas inválidas, IDs no numéricos, recursos inexistentes) mostrando mensajes claros en rojo. La experiencia de usuario es fluida y los colores ayudan a distinguir información importante.

### Ejemplo de uso

Supongamos que el usuario quiere planificar un asedio. Tras iniciar la aplicación y elegir la opción `a`, se le irán pidiendo los datos. Si elige un tipo de evento que requiere ciertos recursos (ej. Asedio), el sistema validará que los incluya. Si además mezcla recursos de casas enemigas, se mostrará un error:

```
Error: Las casas 'Lannister' y 'Stark' no pueden aliarse
```

Si, por el contrario, todo es correcto, se mostrará un mensaje de éxito:

```
Evento 'Asedio a Invernalia' agregado con ID 1
```

La búsqueda de huecos se activa opcionalmente, y si se encuentra un intervalo, se muestra al usuario y se le pregunta si desea usarlo.

---

## 6. Persistencia

El estado se guarda en un único archivo `war_planner.json` con el siguiente esquema:

- `"resources"`: diccionario {id: {id, name, type, house}}.
- `"restrictions"`: diccionario con todas las reglas (inclusiones, exclusiones, por evento, casas, personajes).
- `"events"`: lista de eventos serializados (con fechas en formato ISO).
- `"next_event_id"`: entero autoincrementado.

Al iniciar, `load_data()` busca el archivo; si no existe, crea uno con los datos por defecto de `default_data.py`. Tras cada operación que modifica el estado, se llama a `save_data()`, que sobrescribe el archivo. Esto asegura que la planificación sea persistente entre ejecuciones.

---

## 7. Dificultades encontradas y soluciones

### 7.1 Gestión de fechas y validación de intervalos
Al principio, el usuario introducía fechas como texto y la validación era compleja. Opté por dividir la entrada en año, mes, día, hora y minuto, con bucles que repiten la pregunta hasta que los datos sean válidos. Esto simplificó el código y mejoró la experiencia de usuario.

### 7.2 Restricciones genéricas vs específicas
Inicialmente definí restricciones con IDs de recursos concretos, lo que hacía que añadir un nuevo recurso de una casa diferente (por ejemplo, maquinaria de asedio Targaryen) requiriera actualizar todas las reglas. La solución fue **usar el campo `type`** del recurso en lugar de su ID. Esto permitió que las reglas se apliquen automáticamente a cualquier recurso con ese tipo.

### 7.3 Validación de personajes
Quería que los personajes (Eddard, Jaime, etc.) tuvieran exclusiones basadas en su nombre, pero no quería que el sistema filtrara por tipo `Personaje` porque Daenerys es `Jinete de dragón`. La solución fue modificar la función de validación para que recoja **todos los nombres** de los recursos seleccionados, sin importar su tipo, y los compare con las claves de la restricción. Así, Daenerys también participa en las exclusiones.

### 7.4 Búsqueda de huecos
El algoritmo inicial era demasiado simple y no consideraba correctamente los conflictos de recursos. Lo reescribí para que recorriera todos los eventos y, para cada hueco, verificara con `is_slot_valid` que ningún recurso estuviera ocupado. También tuve que asegurarme de que el candidato `end` no sobrepasara el límite de días.

### 7.5 Interfaz de consola con `rich`
Aprender a usar `rich` (tablas, prompts, colores) llevó algo de tiempo, pero valió la pena porque la interfaz quedó mucho más atractiva y clara. Los mensajes de error en rojo y los textos en verde para éxito mejoran la usabilidad.

### 7.6 Gestión de errores en la entrada de recursos
Cuando el usuario introducía IDs de recursos que no existían, el sistema fallaba. Añadí una validación previa en `add_event` que comprueba que todos los IDs existen en el diccionario de recursos, y si no, devuelve un mensaje de error claro.

---

## 8. Pruebas y validación

Aunque no se han desarrollado pruebas unitarias formales, se ha realizado una validación manual exhaustiva:

- **Pruebas de restricciones**: se intentaron crear eventos con combinaciones prohibidas (ej. Asedio con caballería) y se comprobó que el sistema las rechazara con el mensaje adecuado.
- **Pruebas de conflictos**: se crearon dos eventos con el mismo recurso en horarios solapados y se verificó que el segundo fuera rechazado.
- **Pruebas de búsqueda de huecos**: con una agenda cargada, se pidió un hueco para un conjunto de recursos y se comprobó que el intervalo sugerido era realmente libre.
- **Pruebas de persistencia**: se agregaron eventos, se cerró el programa y al volver a abrir los eventos seguían presentes.

El sistema se comporta como se espera, y los mensajes de error guían al usuario para corregir las entradas.

---

## 9. Aprendizajes y reflexión personal

Durante el desarrollo de *War is Coming* he adquirido una comprensión mucho más profunda de varios conceptos clave:

- **Modelado de dominios**: aprender a abstraer un problema real (planificación militar) en entidades (eventos, recursos) y reglas ha sido muy enriquecedor. Me he dado cuenta de que un buen modelo de datos simplifica enormemente el código.
- **Validación en capas**: separar la lógica de validación (restricciones) de la gestión de datos y de la interfaz ha hecho que el código sea más mantenible y fácil de depurar.
- **Algoritmos de búsqueda en intervalos**: la búsqueda de huecos me obligó a entender cómo manejar eficientemente listas ordenadas y comprobar solapamientos, una habilidad muy útil para cualquier sistema de planificación.
- **Persistencia con JSON**: trabajar con archivos JSON me ha enseñado la importancia de la serialización y cómo manejar fechas y objetos complejos.
- **Interacción con el usuario**: diseñar una CLI amigable con `rich` me ha mostrado que incluso una consola puede ofrecer una experiencia atractiva si se cuidan los detalles.
- **Iteración y refinamiento**: he ido mejorando el proyecto paso a paso, añadiendo restricciones, corrigiendo errores y puliendo la interfaz. Esto me ha enseñado a no buscar la perfección desde el principio, sino a construir de forma incremental.
- **Importancia de las restricciones**: entender cómo las reglas de negocio pueden hacer que un sistema sea mucho más interesante y desafiante. Las restricciones no solo son requisitos, sino que añaden profundidad al dominio.

Además, el hecho de haber elegido un dominio que me apasiona (el universo de ASOIAF) ha hecho que el proceso sea mucho más divertido y motivador. Cada nueva restricción que añadía me recordaba una escena de los libros o la serie, lo que daba coherencia al proyecto.

---

## 10. Conclusión

*War is Coming* es un sistema funcional y coherente que cumple con todos los requisitos mínimos del proyecto:

- **Planificación de eventos** con recursos limitados.
- **Validación de restricciones** (co‑requisitos, exclusiones, por tipo de evento, por casas y por personajes).
- **Búsqueda automática de huecos** para facilitar la organización.
- **Interfaz de consola** completa y usable.
- **Persistencia** en JSON para guardar y cargar el estado.

El sistema es extensible: se pueden añadir nuevos recursos, nuevas casas, nuevas restricciones sin modificar el núcleo de la lógica. El uso de tipos en lugar de IDs hace que las reglas sean genéricas y escalables.

En el futuro, me gustaría implementar algunas de las funcionalidades opcionales, como **recursos con cantidad** (ej. tener 5 unidades de Infantería pesada en lugar de una única) o **eventos recurrentes** (planificar una serie de escaramuzas diarias). También podría explorar una interfaz web con Streamlit para hacerla más visual y accesible.

En definitiva, este proyecto me ha permitido poner en práctica todos los conocimientos adquiridos durante el curso y me ha dado la confianza para abordar sistemas más complejos en el futuro.
