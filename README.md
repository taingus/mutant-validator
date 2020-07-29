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

### Correr tests e integración continua

Si bien las GitHub Actions están configuradas para correr los tests de forma
automática en cada push a master, los tests pueden correrse de forma local
con [pytest](https://docs.pytest.org/en/latest/), el comando es:

```
pytest
```
