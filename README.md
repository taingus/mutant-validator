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

## Infraestructura

## Puntos de mejora

## Documentación de la API

FastAPI provee un sistema de documentación automática de una API cuando las
funciones están anotadas tanto en los modelos de entrada, salida, y
queryparams.

Para conseguir esto, se basa en la especificación de OpenAPI disponible en:

`http://localhost:8000/openapi.json`

También se provee una interfaz simple que se puede acceder desde

- `http://localhost:8000/docs` para ver la documentación al estilo Swagger
- `http://localhost:8000/redoc` para verla como [ReDoc](https://github.com/Redocly/redoc)

Esta documentación también está disponible en producción, en la URL:

https://meli-xmen-agustincignetti.rj.r.appspot.com
