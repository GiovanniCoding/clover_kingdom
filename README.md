# Clover Kingdom Sistem

## Descripción del Proyecto

En el Reino del Trébol, el Rey Mago requiere un sistema eficiente para gestionar las solicitudes de ingreso de estudiantes a la academia de magia y la asignación aleatoria de Grimorios a los solicitantes aceptados. Este sistema permite:

- Crear y actualizar solicitudes de ingreso de estudiantes.
- Consultar y eliminar solicitudes.
- Asignar Grimorios a los estudiantes basándose en afinidades mágicas específicas y ponderación de la rareza de los Grimorios.

## Tecnologias
- Python 3.12.4
- PostgreSQL
- Fastapi
- Alembic
- Pytest
- Flake8
- Docker
- Kubernetes [k0s]

## CI
Para controlar el CI se utilizó Github Actions, para ello se crearon 2 tareas:

- Poder mantener la calidad del código usando Linter (Flake8).
- Se creó una acción para ejecutar las pruebas unitarias y verificar la funcionalidad del código.


### Requisitos
* Docker and Docker Compose
* Make (Optional)


### Configuración
1. **Clona el repositorio**:
    ```bash
    git clone git@github.com:GiovanniCoding/clover_kingdom.git
    cd clover_kingdom
    ```

2. **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configura las variables de entorno**:
    En sistemas basados en unix, por defecto es posible usar make, se puede usar make para crear el archivo `.env` y crear las imagenes en local usando `docker compose`.
    ```env
    make setup
    ```

4. **Ejecución**:
    Los comandos principales, son los siguientes, todos los comandos pueden ser encontrados en el archivo `Makefile`
    ```env
    make build     # Build Docker images
    make up        # Start services
    make down      # Stop services
    ```

5. **Pruebas Unitarias**:
    Las pruebas unitarias pueden ser ejecutadas usando make:
    ```env
    make up
    make test
    ```

## Accediendo a la API

Una vez que la aplicación se esté ejecutando, puede acceder a la documentación de la API en:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

### API Online
Se optó por desplegar en linea usando kubernetes, para esto se hizo uso de un servidor personal, usando una implementación de [k0s](https://k0sproject.io/), de igual forma se agregan al repositorio los archivos para el despliegue:

* Swagger UI: http://158.220.123.31:30000/docs
* ReDoc: http://158.220.123.31:30000/redoc

En el despliegue, se hizo un despliegue directo a traves del puerto 30000, lo ideal sería usar un ingress como nginx para poder hacer un cifrado SSL, pero esto se sale del alcance del projecto.

## Modelos
Para el diseño de la base de datos se optó por la creación de dos tablas
- applications
- students

Pensando a futuro, se optó por separar la información de los estudiantes (o aspirantes) de las aplicaciones.

## Endpoints

### Health
- **GET /api/v1/health/**: Verificar el estado de la API.

### Solicitudes
- **GET /api/v1/solicitudes/**: Obtener todas las solicitudes de ingreso.
- **POST /api/v1/solicitudes/**: Crear una solicitud de ingreso.
- **PUT /api/v1/solicitudes/{id}**: Actualizar una solicitud de ingreso por ID.
- **PATCH /api/v1/solicitudes/{id}**: Aceptar una solicitud de ingreso por ID.
- **DELETE /api/v1/solicitudes/{id}**: Eliminar una solicitud de ingreso por ID.

### Asignaciones (Grimorios)
- **GET /api/v1/asignaciones/**: Obtener todas las asignaciones de Grimorios.

## Puntos importantes
- Aunque los aspirantes traen su propio ID, se optó por usar un ID generado por la base de datos, esto para evitar problemas de integridad en la base de datos.
    - Por este motivo, todas las solicitudes son usando el ID generado por la base de datos.