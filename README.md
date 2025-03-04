# Video Downloader con Selenium

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen)
![Moodle](https://img.shields.io/badge/Moodle-Supported-orange)


## 📌 Descripción
Este script automatiza la descarga de videos desde la plataforma Moodle utilizando Selenium. Realiza el inicio de sesión, extrae dinámicamente el título del video y lo descarga automáticamente en la carpeta especificada.

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/agosalvez/moodle-video-downloader.git
   cd moodle-video-downloader
   ```

2. **Instalar dependencias**
   ```bash
   pip install selenium webdriver-manager requests
   ```

3. **Configurar credenciales y ruta de descarga**
   Edita el archivo `index.py` y reemplaza:
   ```python
   config = Config(
       url="https://campus.uax.es/moodle/course/view.php?id=16854",
       email="YOUR_EMAIL",
       password="YOUR_PASSWORD",
       download_path="YOUR_PATH_TO_DOWNLOAD",
   )
   ```

## 📋 Uso

Ejecuta el script con:
```bash
python index.py
```

💡 **Nota:** Se requiere autenticación en Moodle. El script detendrá la ejecución y te pedirá que completes la autenticación 2FA manualmente.

## ⚙️ Personalización
Este script está diseñado para ser adaptable según las necesidades del usuario. Los parámetros como la **URL del curso**, las **credenciales de acceso**, el **directorio de descarga**, e incluso la **lógica de selección de grabaciones** pueden modificarse dentro del código fuente.

Por defecto, el script está configurado con valores de ejemplo, pero cada usuario puede ajustarlo según los videos o el contenido que desee descargar. 

💡 **Si tienes mejoras o sugerencias, considera contribuir al proyecto!** 🙌

## 🔍 Funcionamiento

1. **Accede a Moodle** e inicia sesión automáticamente.
2. **Obtiene el título del video** desde el encabezado `<h1>` y lo usa como nombre del archivo.
3. **Busca y abre enlaces de grabaciones**, evitando duplicados.
4. **Descarga el video** en la carpeta configurada.
5. **Guarda el video con un nombre estructurado**, evitando caracteres especiales.

## 🛠️ Requisitos
- Python 3.x
- Google Chrome instalado
- ChromeDriver (se instala automáticamente con `webdriver-manager`)

## ⚠️ Advertencias
- **Credenciales en código:** Se recomienda utilizar variables de entorno para manejar credenciales de manera segura.
- **Políticas de la plataforma:** Antes de descargar videos, asegúrate de cumplir con las políticas de uso del sitio web.
- **Uso del script:** El autor de este script **no se hace responsable** del uso indebido que pueda darse al código. Cada usuario es responsable de asegurarse de que su uso cumple con las normativas y términos de servicio de la plataforma en la que se utilice.

## 🤝 Contribuir
¡Gracias por tu interés en contribuir a este proyecto! Sigue estos pasos para hacer una contribución:

1. **Haz un fork del repositorio**
   ```bash
   git clone https://github.com/agosalvez/moodle-video-downloader.git
   cd moodle-video-downloader
   ```
2. **Crea una nueva rama para tu cambio**
   ```bash
   git checkout -b feature-nueva-funcionalidad
   ```
3. **Realiza tus cambios y haz un commit**
   ```bash
   git add .
   git commit -m "Añadida nueva funcionalidad XYZ"
   ```
4. **Sube los cambios a tu repositorio**
   ```bash
   git push origin feature-nueva-funcionalidad
   ```
5. **Abre un Pull Request (PR)** en GitHub con una descripción clara de tu cambio.

💡 **Nota:** Asegúrate de que tu código sigue las mejores prácticas y pasa todas las pruebas antes de enviar un PR.

## 📄 Licencia
Este proyecto está bajo la licencia **MIT**. ¡Siéntete libre de usarlo y mejorarlo! 🎯

