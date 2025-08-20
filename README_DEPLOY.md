# Chat Downloader API - Render Deployment

API REST para descargar chats de Twitch, YouTube y otras plataformas usando Chat Downloader.

## 🚀 Despliegue en Render

### Opción 1: Deploy automático
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Opción 2: Deploy manual
1. Fork este repositorio
2. Conecta tu cuenta de GitHub a Render
3. Crea un nuevo Web Service
4. Selecciona este repositorio
5. Render detectará automáticamente la configuración

## 📡 API Endpoints

### `POST /download`
Inicia la descarga de un chat.

**Body:**
```json
{
  "url": "https://www.twitch.tv/canal",
  "format": "jsonl",
  "max_messages": 1000,
  "timeout": 3600
}
```

**Response:**
```json
{
  "download_id": "download_1692567890",
  "status": "started",
  "message": "Download started successfully"
}
```

### `GET /status/<download_id>`
Consulta el estado de una descarga.

**Response:**
```json
{
  "status": "downloading",
  "messages_count": 150,
  "start_time": "2023-08-20T22:30:00",
  "url": "https://www.twitch.tv/canal"
}
```

### `GET /download/<download_id>`
Descarga el archivo generado.

### `GET /active`
Lista todas las descargas activas.

### `GET /health`
Health check del servicio.

## 🔧 Formatos soportados

- **jsonl**: Una línea por mensaje (recomendado)
- **json**: Array JSON completo
- **csv**: Formato tabular
- **txt**: Texto plano

## 🌐 Plataformas soportadas

- ✅ Twitch (livestreams, VODs, clips)
- ✅ YouTube (livestreams, premieres)
- ✅ Facebook (livestreams)
- ✅ Zoom (past broadcasts)

## 📝 Ejemplos de uso

### Capturar chat de Twitch
```bash
curl -X POST https://tu-app.onrender.com/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.twitch.tv/alimentacionchino",
    "format": "jsonl",
    "max_messages": 500
  }'
```

### Verificar estado
```bash
curl https://tu-app.onrender.com/status/download_1692567890
```

### Descargar archivo
```bash
curl -O https://tu-app.onrender.com/download/download_1692567890
```

## ⚙️ Variables de entorno

- `PORT`: Puerto del servidor (automático en Render)
- `PYTHON_VERSION`: Versión de Python (3.9.16)

## 🔒 Limitaciones

- Archivos temporales se eliminan después de 24h
- Máximo 10 descargas simultáneas
- Timeout máximo: 2 horas por descarga

## 🐛 Troubleshooting

### Error de dependencias
Si hay problemas con las dependencias, verifica que `requirements.txt` esté actualizado.

### Timeout en descargas largas
Para streams muy largos, usa `timeout` o `max_messages` para limitar la captura.

### Memoria insuficiente
Usa formato `jsonl` en lugar de `json` para streams largos.