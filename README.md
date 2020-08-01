![Mutant Validator](https://github.com/taingus/mutant-validator/workflows/Mutant%20Validator/badge.svg)

# Mutant Validator

Este proyecto expone una API simple utilizando [FastAPI](https://fastapi.tiangolo.com/)
para la capa de API, [pydantic](https://pydantic-docs.helpmanual.io/) para
validación del request y documentación, y [uvicorn](https://www.uvicorn.org/)
para manejar las peticiones al servidor, ya que FastAPI no ofrece eso.

uvicorn es la versisón asíncrona de [gunicorn](https://gunicorn.org/), lo que
permite utilizar las palabras reservadas `async` y `await` disponibles a partir
de python 3.6.

## Configuración del entorno de desarrollo

### Instalación de dependencias

El gestor de paquetes utilizado y recomendado es [poetry](https://python-poetry.org/),
pero también se puede instalar mediante `pip`.

¿Por qué Poetry en vez de sólo pip? Al momento de resolver dependencias y
conflictos, poetry es lo suficientemente inteligente como para encontrar las
versiones más nuevas que no tengan conflictos entre si.

Además, Poetry genera un entorno virtual para aislar los paquetes de lo que
está disponible de forma global, que es diferente a lo que ofrece pip

#### Instalación mediante poetry

```
pip install poetry
poetry install
```

#### Instalación mediante pip

```
pip install -r requirements-dev.txt
```

### Correr el servidor de forma local

Una vez instaladas todas las dependencias, si se optó por utilizar Poetry, se
debe entrar dentro del entorno virtual primero:

```
poetry shell
```

Después se ejecuta:

```
uvicorn mutant_validator.main:app
```

El server se va a levantar escuchando en el puerto `8000` y sólo para
`localhost`.

### Actualización de dependencias

En caso de ser necesario actualizar las dependencias, es aconsejable hacerlo
mediante Poetry corriendo el comando

```
poetry update
```

Y luego exportar las nuevas versiones para que GitHub tome las mismas al
correr la integración contínua con:

```
poetry export -f requirements.txt --dev > requirements-dev.txt
poetry export -f requirements.txt > requirements.txt
```

¿Por qué dos archivos requirements? Porque algunos proveedores de PaaS están
configurados para procesar esos archivosn únicamente. Con un Dockerfile no es
necesario

### Tests e integración continua

Si bien las GitHub Actions están configuradas para correr los tests de forma
automática en cada push a master, los tests pueden correrse de forma local
con [pytest](https://docs.pytest.org/en/latest/), el comando es:

```
pytest
```

## Estructura del proyecto

El proyecto tiene en su raiz dos archivos:

- `main.py`: Es el punto de entrada del proyecto, donde está expuesta la API.
  Desde este archivo se importa la sección del backend propiamente dicho.
- `config.py`: Donde se guardan las configuraciones relacionadas al proyecto,
  que se terminarán sacando desde las variables de entorno

Después una subcarpeta `backend` que está separado en:

- `containers.py`: Acá se definen los contenedores que heredan de los modelos
  base de `pydantic` ya que pueden utilizarse para exportar datos desde un
  modelo de base de datos, o parsear y validar datos que se reciban en la API
- `models.py`: Define los modelos de base de datos con los que termina
  interactuando el proyecto.
- `query.py`: Contiene una definición de queries que devuelven resultados de
  una base de datos, el definirlas acá permite que sean reutilizadas en otros
  lugares, y agrupar la lógica de queries en un único lugar.
- `validator.py`: Es donde está la lógica principal del proyecto, donde se
  generan los nodos que luego serán validados, pero no guardados en la base
  de datos.

## Funcionamiento

Desde un punto de vista macro, el funcionamiento de la API de validación de
ADN es simple:

1. Recibe una petición
2. Valida que la petición contenga sólo cadenas de ADN válidas y de la misma
   longitud, ya que es una matriz
3. Si la petición es válida, controla si existe alguna cadena de ADN mutante.
   En caso de que el ADN esté mal formado o tenga caracteres inválidos, se
   responde con un 422.
4. En caso de ser mutante, prepara una respuesta con un resultado 200, o 403
   si el ADN es de un humano normal.
5. Guarda el ADN recibido haciendo un hash sobre lo que se recibió para que
   no existan repetidos dentro de la base de datos
6. Devuelve el resultado al usuario

[[Diagrama de flujo]]

Como el flujo general es bastante simple se seguir, a continuación se muestra
cómo trabaja de forma interna la función `is_mutant` que contiene la mayor
complejidad:

Suponiendo que recibimos un ADN de la siguiente forma:

```
+---+---+---+---+---+
| A | C | G | T | A |
+---+---+---+---+---+
| C | A | T | G | C |
+---+---+---+---+---+
| G | T | A | C | G |
+---+---+---+---+---+
| A | T | C | G | T |
+---+---+---+---+---+
| A | C | G | G | A |
+---+---+---+---+---+
| G | A | T | C | C |
+---+---+---+---+---+
| A | C | T | T | G |
+---+---+---+---+---+
```

La función va a generar un objeto [Node](https://github.com/taingus/mutant-validator/blob/master/mutant_validator/backend/containers.py#L14)
por cada línea horizontal, y va a agregar además, siempre que la longitud
vertical lo permita, dos líneas diagonales, una hacia abajo, y otra hacia
arriba. ese objeto nodo, una vez creado, va a evaluar si en alguna de esas
una a tres líneas contiene alguna de las cadenas que delatan que el ADN es en
realidad el de un mutante.

Por ejemplo, estos son nodos horizontales

[[Imagen de Node de ejemplo primer línea]]
[[Imagen de Node de ejemplo línea intermedia]]
[[Imagen de Node de ejemplo última línea]]

Una vez evaluados esos nodos, El resultado de las líneas posibles evaluadas
queda de la siguiente forma:

[[Imagen ADN líneas horizontales]]
[[Imagen ADN líneas diagonales hacia arriba]]
[[Imagen ADN líneas diagonales hacia abajo]]

La siguiente iteración se hace sobre las columnas del ADN de una forma
similar. Primero se generan objetos `Node` para cada columna, incluyendo las
líneas diagonales hacia atrás y adelante, para evaluar el resto de las
diagonales que quedaron afuera en la evaluación anterior.

Una vez mas, ejemplos de la evaluación de las columnas es:

[[Imagen de Node de ejemplo primer línea]]
[[Imagen de Node de ejemplo línea intermedia]]
[[Imagen de Node de ejemplo última línea]]

Una vez evaluados estos nodos finales, el resultado de las columnas posibles
evaluadas queda de la siguiente forma:

[[Imagen ADN líneas horizontales]]
[[Imagen ADN líneas diagonales hacia arriba]]
[[Imagen ADN líneas diagonales hacia abajo]]

    NOTA: El programa va a cortar la evaluación al primer indicio de que el
    ADN es de un mutante, ya que no es necesario controlar el ADN por completo

## Infraestructura



## Areas de mejora

Al correr el test de performance con un ADN de 7000 x 4000 de un humano no
mutante, el tiempo de ejecución muestra lo siguiente:

```
tests/backend/test_validator.py::test_performance_valid_DNA_sequence_human

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     7000    5.552    0.001    5.552    0.001 /mutant_validator/backend/validator.py:56(<listcomp>)
     7000    3.945    0.001    3.945    0.001 /mutant_validator/backend/validator.py:49(<listcomp>)
     7000    3.394    0.000    3.394    0.000 /mutant_validator/backend/validator.py:63(<listcomp>)
     4000    2.089    0.001    2.089    0.001 /mutant_validator/backend/validator.py:32(<listcomp>)
     4000    2.013    0.001    2.013    0.001 /mutant_validator/backend/validator.py:25(<listcomp>)
     .
     .
    11000    0.024    0.000    0.461    0.000 /mutant_validator/backend/containers.py:25(is_mutant)
    44000    0.029    0.000    0.434    0.000 /mutant_validator/backend/containers.py:35(_check_line)
   220000    0.365    0.000    0.365    0.000 /mutant_validator/backend/containers.py:36(<genexpr>)
```

    NOTA: Se omitió el resto porque el tiempo era de librerías y no representaban
    un valor significativo

Como se ve, donde más tiempo pasa el proceso es en los generadores de strings
que luego serán usados para controlar si el ADN es de un mutante, esa es el
área donde más podría optimizarse el código si se tuviera a disposición un
procesador con más de un único núcleo, ya que en Python estamos restringidos
por el [GIL](https://wiki.python.org/moin/GlobalInterpreterLock).

Las últimas 3 líneas se incluyeron para mostrar el tiempo que toma evaluar
cada una de los strings buscando las cadenas de ADN mutante. En el código
[son estas](https://github.com/taingus/mutant-validator/blob/master/mutant_validator/backend/containers.py#L25-L36).
Esto se debe a que la comparación se realiza en un módulo especializado
de Python escrito en C.

### Cambios simples que podrían implementarse

Uno de los cambios que implica no tocar el código, es cambiar el intérprete
de Python por PyPy.

Otra posible mejora es convertir la API en asíncrona, devolviendo una URL
donde buscar el resultado, pero esto alteraría el funcionamiento esperado.

## Documentación de la API

FastAPI provee un sistema de documentación automática de una API cuando las
funciones están anotadas tanto en los modelos de entrada, salida, y
queryparams.

Para conseguir esto, se basa en la especificación de OpenAPI disponible en:

`http://localhost:8000/openapi.json`

También se provee una interfaz autogenerada que se puede acceder desde

- `http://localhost:8000/docs`: Documentación al estilo [SwaggerUI](https://github.com/swagger-api/swagger-ui)
- `http://localhost:8000/redoc`: Documentación al estilo [ReDoc](https://github.com/Redocly/redoc)

## Endpoints

- [API](https://meli-xmen-agustincignetti.rj.r.appspot.com/)

### Documentación

- [SwaggerUi](https://meli-xmen-agustincignetti.rj.r.appspot.com/docs)
- [ReDoc](https://meli-xmen-agustincignetti.rj.r.appspot.com/redoc)
- [OpenAPI schema](https://meli-xmen-agustincignetti.rj.r.appspot.com/openapi.json)
