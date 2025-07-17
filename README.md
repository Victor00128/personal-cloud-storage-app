# Personal Cloud Storage

Una aplicación web de almacenamiento personal en la nube que permite a los usuarios subir, gestionar y descargar archivos de forma segura desde cualquier dispositivo.

## Características

- 🔐 **Autenticación segura** con JWT y refresh tokens
- 📁 **Gestión de archivos** - subir, descargar, eliminar archivos
- 💾 **Soporte para archivos grandes** - hasta 1GB por archivo
- 🌙 **Modo oscuro/claro** - interfaz adaptable
- 📱 **Diseño responsivo** - funciona en PC y móvil
- 🔄 **Persistencia de sesión** - mantiene la sesión activa automáticamente
- 🛡️ **Seguridad** - contraseñas cifradas y tokens seguros

## Tecnologías

### Backend
- **Flask** - Framework web de Python
- **SQLAlchemy** - ORM para base de datos
- **JWT** - Autenticación con tokens
- **SQLite** - Base de datos
- **Flask-CORS** - Soporte para CORS

### Frontend
- **React** - Biblioteca de interfaz de usuario
- **Vite** - Herramienta de construcción
- **Tailwind CSS** - Framework de CSS
- **Lucide React** - Iconos
- **shadcn/ui** - Componentes de UI

## Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- Node.js 20+
- pnpm

### Backend

1. Navega al directorio del backend:
```bash
cd backend
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
python src/main.py
```

El backend estará disponible en `http://localhost:5000`

### Frontend

1. Navega al directorio del frontend:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
pnpm install
```

3. Ejecuta el servidor de desarrollo:
```bash
pnpm run dev
```

El frontend estará disponible en `http://localhost:5173`

### Construcción para Producción

#### Frontend
```bash
cd frontend
pnpm run build
```

#### Despliegue Completo
1. Construye el frontend
2. Copia los archivos construidos a `backend/src/static/`
3. Ejecuta el backend que servirá tanto la API como los archivos estáticos

## Uso

1. **Registro**: Crea una cuenta con usuario, email y contraseña
2. **Inicio de sesión**: Accede con tus credenciales
3. **Subir archivos**: Usa el botón "Seleccionar Archivo" para subir archivos (hasta 1GB)
4. **Gestionar archivos**: Descarga o elimina archivos desde la lista
5. **Modo oscuro**: Usa el botón en la esquina superior derecha para cambiar el tema

## Estructura del Proyecto

```
personal-cloud-storage/
├── backend/                 # Aplicación Flask
│   ├── src/
│   │   ├── models/         # Modelos de base de datos
│   │   ├── routes/         # Rutas de la API
│   │   ├── database/       # Archivos de base de datos
│   │   ├── static/         # Archivos estáticos del frontend
│   │   └── main.py         # Punto de entrada
│   └── requirements.txt    # Dependencias de Python
├── frontend/               # Aplicación React
│   ├── src/
│   │   ├── components/     # Componentes de React
│   │   ├── services/       # Servicios (autenticación, etc.)
│   │   └── App.jsx         # Componente principal
│   ├── package.json        # Dependencias de Node.js
│   └── vite.config.js      # Configuración de Vite
└── README.md              # Este archivo
```

## API Endpoints

### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Inicio de sesión
- `POST /api/auth/refresh` - Renovar token de acceso

### Archivos
- `GET /api/files` - Listar archivos del usuario
- `POST /api/upload` - Subir archivo
- `GET /api/files/{id}` - Descargar archivo
- `DELETE /api/files/{id}` - Eliminar archivo

## Seguridad

- Las contraseñas se cifran usando bcrypt
- Autenticación basada en JWT con refresh tokens
- Renovación automática de tokens
- Validación de archivos y límites de tamaño
- CORS configurado para desarrollo y producción

## Despliegue

### Netlify (Recomendado para Frontend)

Este proyecto está configurado para desplegarse fácilmente en Netlify:

1. **Fork o clona este repositorio** en tu cuenta de GitHub
2. **Conecta tu repositorio a Netlify**:
   - Ve a [netlify.com](https://netlify.com) y crea una cuenta
   - Haz clic en "New site from Git"
   - Conecta tu cuenta de GitHub y selecciona este repositorio
   - Netlify detectará automáticamente la configuración desde `netlify.toml`
3. **Configura las variables de entorno** (si es necesario):
   - En el dashboard de Netlify, ve a Site settings > Environment variables
   - Añade cualquier variable de entorno necesaria para tu backend
4. **Despliega**: Netlify construirá y desplegará automáticamente tu aplicación

### Backend (Separado)

Para el backend, puedes usar servicios como:
- **Heroku**: Para aplicaciones Flask
- **Railway**: Para aplicaciones Python
- **Render**: Para aplicaciones web
- **DigitalOcean App Platform**: Para aplicaciones containerizadas

### Configuración para Producción

1. **Variables de entorno**: Configura las variables necesarias en tu servicio de hosting
2. **Base de datos**: Usa PostgreSQL o MySQL en lugar de SQLite para producción
3. **CORS**: Actualiza la configuración de CORS en el backend para permitir tu dominio de Netlify
4. **API URL**: Actualiza la URL base de la API en el frontend para apuntar a tu backend desplegado

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

