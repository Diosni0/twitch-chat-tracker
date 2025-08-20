# 🎮 Twitch Chat Tracker

API REST para capturar y descargar chats de Twitch, YouTube y otras plataformas en tiempo real.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Diosni0/twitch-chat-tracker)

## 🚀 Características

- ✅ **Captura en tiempo real** de chats de Twitch, YouTube, Facebook
- ✅ **API REST** fácil de usar
- ✅ **Múltiples formatos** de salida (JSON, JSONL, CSV, TXT)
- ✅ **Descargas en background** sin bloquear la API
- ✅ **Monitoreo en tiempo real** del progreso
- ✅ **Deploy automático** en Render
- ✅ **Sin autenticación** requerida

## 🌐 Demo en vivo

**API Base URL:** `https://tu-app.onrender.com`

## 📡 Endpoints

### `POST /download`
Inicia la captura de un chat.

```bash
curl -X POST https://tu-app.onrender.com/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.twitch.tv/alimentacionchino",
    "format": "jsonl",
    "max_messages": 1000
  }'
```

### `GET /status/<download_id>`
Consulta el progreso de una descarga.

```bash
curl https://tu-app.onrender.com/status/download_1692567890
```

### `GET /download/<download_id>`
Descarga el archivo generado.

```bash
curl -O https://tu-app.onrender.com/download/download_1692567890
```

## 🛠️ Instalación local

```bash
# Clonar repositorio
git clone https://github.com/Diosni0/twitch-chat-tracker.git
cd twitch-chat-tracker

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
python app.py

# Probar API
python test_api.py
```

## 🚀 Deploy en Render

1. **Fork este repositorio**
2. **Conecta GitHub a Render**
3. **Crea nuevo Web Service**
4. **Selecciona tu fork**
5. **Deploy automático** ✨

Render detectará automáticamente:
- `requirements.txt` - Dependencias Python
- `Procfile` - Comando de inicio
- `runtime.txt` - Versión de Python
- `render.yaml` - Configuración del servicio

## 📊 Formatos soportados

| Formato | Descripción | Uso recomendado |
|---------|-------------|-----------------|
| `jsonl` | Una línea por mensaje | **Streams largos** |
| `json` | Array JSON completo | Análisis completo |
| `csv` | Formato tabular | Excel/Pandas |
| `txt` | Texto plano | Lectura simple |

## 🎯 Plataformas soportadas

- 🟣 **Twitch** - Livestreams, VODs, Clips
- 🔴 **YouTube** - Livestreams, Premieres
- 🔵 **Facebook** - Livestreams
- 🟡 **Zoom** - Past broadcasts

## 📝 Ejemplos de uso

### Capturar stream completo
```json
{
  "url": "https://www.twitch.tv/shroud",
  "format": "jsonl"
}
```

### Capturar con límites
```json
{
  "url": "https://www.twitch.tv/ninja",
  "format": "json",
  "max_messages": 500,
  "timeout": 3600
}
```

### Capturar VOD específico
```json
{
  "url": "https://www.twitch.tv/videos/1234567890",
  "format": "csv"
}
```

## 🔧 Configuración avanzada

### Variables de entorno
- `PORT` - Puerto del servidor (automático en Render)
- `PYTHON_VERSION` - Versión de Python (3.9.16)

### Límites por defecto
- **Descargas simultáneas:** 10
- **Timeout máximo:** 2 horas
- **Archivos temporales:** 24 horas

## 📈 Estructura de datos

### Mensaje de chat típico
```json
{
  "message_id": "abc123",
  "message": "Hola mundo!",
  "timestamp": 1692567890000,
  "author": {
    "name": "usuario123",
    "display_name": "Usuario123",
    "badges": ["subscriber", "moderator"],
    "color": "#FF0000"
  },
  "emotes": [...],
  "message_type": "text_message"
}
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Créditos

Basado en [chat-downloader](https://github.com/xenova/chat-downloader) por xenova.

---

⭐ **¡Dale una estrella si te resulta útil!**