# [Preguntas](https://github.com/Dmoga31/Inventario2/blob/main/Preguntas.md)
# Instalación y Configuración
### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/inventario-vue.git
cd inventario-vue
```

## Configurar Backend

```bash 
cd inventario-backend
```

### Crear entorno virtual (Windows)
```bash
python -m venv venv
```
``` bash
venv\Scripts\activate
```

### Instalar dependencias
``` bash
pip install flask flask-graphql graphene flask-cors
```

### Iniciar servidor
```bash
python app.py
```

El backend estará disponible en: ```http://localhost:5000/graphql```

## Configurar Frontend
```bash
cd ../inventario-vue
```

### Instalar dependencias
```bash
npm install
```

### Iniciar aplicación
```bash
npm run serve
```

El frontend estará disponible en: ```http://localhost:8080```

## Para ejecución de pruebas `test.py`
### 1. Entrar al directorio del backend
```bash
cd inventario-backend
```

### 2. Instalar dependencias de testing
```bash
pip install pytest
```

### 3. Ejecutar las pruebas
```bash
python -m pytest test.py -v```


