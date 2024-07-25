# VivaControl-Web
Viva Control es un software para el control de inventario de productos para negocios pequeños o medianos.

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local:

### 1. Clona el Repositorio

```bash
git clone https://github.com/elrichardby11/VivaControl-Web.git
cd VivaControl-Web
```

### 2. Crea y Activa el Entorno Virtual

Para mantener las dependencias del proyecto aisladas, se recomienda utilizar un entorno virtual de Python. Sigue estos pasos para crear y activar el entorno virtual:

#### En Windows

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

#### En macOS y Linux

```bash
python3 -m venv .venv
source .\.venv/bin/activate
```

### 3. Instala las Dependencias

Una vez activado el entorno virtual, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### 4. Ejecuta las migraciones

Antes de ejecutar el proyecto es necesario crear la base de datos, comando para crear la base de datos:

```bash
python manage.py migrate
```

### 5. Ejecuta el Proyecto

Ahora estás listo para ejecutar el proyecto, puedes iniciar la aplicación con:

```bash
python manage.py runserver
```

## Demo

![2024-07-25 16-44-54](https://github.com/user-attachments/assets/c25b59d1-8a19-4949-b1d7-98da862ae66d)

![2024-07-25 16-45-33](https://github.com/user-attachments/assets/42f57cfc-b8ee-42af-9c42-b5ab0ab5cf41)

![Sobre nosotros - Viva Control](https://github.com/elrichardby11/VivaControl-Web/assets/76932746/a9e6b28d-f88a-44c7-a5f9-88db581550df)

