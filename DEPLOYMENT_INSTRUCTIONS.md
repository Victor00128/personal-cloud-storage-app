# 🚀 Instrucciones de Despliegue en GitHub y Netlify

## Paso 1: Crear Repositorio en GitHub

1. **Ve a GitHub.com** y inicia sesión en tu cuenta
2. **Crea un nuevo repositorio**:
   - Haz clic en el botón "+" en la esquina superior derecha
   - Selecciona "New repository"
   - Nombre: `personal-cloud-storage`
   - Descripción: `Personal cloud storage application with React frontend and Flask backend`
   - Marca como **Público**
   - **NO** inicialices con README (ya tenemos uno)
   - Haz clic en "Create repository"

## Paso 2: Subir el Código a GitHub

Ejecuta estos comandos en tu terminal local (después de descargar este proyecto):

```bash
# Navegar al directorio del proyecto
cd personal-cloud-storage

# Añadir el repositorio remoto (reemplaza TU_USUARIO con tu nombre de usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/personal-cloud-storage.git

# Subir el código
git push -u origin main
```

## Paso 3: Desplegar en Netlify

### Opción A: Desde GitHub (Recomendado)

1. **Ve a [netlify.com](https://netlify.com)** y crea una cuenta gratuita
2. **Conecta tu repositorio**:
   - Haz clic en "New site from Git"
   - Selecciona "GitHub" y autoriza la conexión
   - Busca y selecciona tu repositorio `personal-cloud-storage`
3. **Configuración automática**:
   - Netlify detectará automáticamente la configuración desde `netlify.toml`
   - Base directory: `frontend/`
   - Build command: `pnpm install && pnpm run build`
   - Publish directory: `frontend/dist/`
4. **Despliega**:
   - Haz clic en "Deploy site"
   - Netlify construirá y desplegará tu aplicación automáticamente

### Opción B: Despliegue Manual

1. **Construye el proyecto localmente**:
   ```bash
   cd frontend
   pnpm install
   pnpm run build
   ```
2. **Sube manualmente**:
   - Ve a Netlify y arrastra la carpeta `frontend/dist/` al área de despliegue

## Paso 4: Configurar el Backend (Opcional)

Para que la aplicación funcione completamente, necesitas desplegar el backend por separado:

### Opciones de Hosting para Backend:

1. **Heroku** (Recomendado para principiantes):
   - Crea una cuenta en heroku.com
   - Instala Heroku CLI
   - Despliega el directorio `backend/`

2. **Railway**:
   - Conecta tu repositorio de GitHub
   - Selecciona el directorio `backend/`

3. **Render**:
   - Conecta tu repositorio
   - Configura como servicio web Python

### Configurar Variables de Entorno

Una vez que tengas el backend desplegado:

1. **En Netlify**:
   - Ve a Site settings > Environment variables
   - Añade: `VITE_API_URL` = `https://tu-backend-url.herokuapp.com`

2. **Redespliega el sitio** para que tome la nueva configuración

## Paso 5: ¡Listo! 🎉

Tu aplicación estará disponible en:
- **Frontend**: `https://tu-sitio.netlify.app`
- **Backend**: `https://tu-backend.herokuapp.com` (si lo desplegaste)

## Características de la Aplicación

✅ **Sin atribución del autor** (eliminada como solicitaste)
✅ **Modo oscuro/claro**
✅ **Persistencia de sesión** con refresh tokens
✅ **Subida de archivos hasta 1GB**
✅ **Interfaz responsiva**
✅ **Autenticación segura**

## Solución de Problemas

### Si el frontend no se conecta al backend:
1. Verifica que `VITE_API_URL` esté configurado correctamente
2. Asegúrate de que el backend permita CORS desde tu dominio de Netlify
3. Revisa los logs de Netlify en el dashboard

### Si hay errores de construcción:
1. Verifica que todas las dependencias estén en `package.json`
2. Revisa los logs de construcción en Netlify
3. Asegúrate de que Node.js versión 20 esté configurado

## Contacto

Si necesitas ayuda adicional, revisa la documentación de:
- [Netlify Docs](https://docs.netlify.com/)
- [GitHub Docs](https://docs.github.com/)
- [React Docs](https://react.dev/)
- [Flask Docs](https://flask.palletsprojects.com/)

