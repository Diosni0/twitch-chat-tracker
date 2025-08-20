#!/usr/bin/env python3
"""
Script de prueba para la API de Chat Downloader
"""

import requests
import json
import time

# Configuración
API_BASE = "http://localhost:5000"  # Cambiar por tu URL de Render

def test_health():
    """Prueba el endpoint de health"""
    print("🔍 Probando health check...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_download():
    """Prueba iniciar una descarga"""
    print("\n📥 Iniciando descarga de prueba...")
    
    payload = {
        "url": "https://www.twitch.tv/alimentacionchino",
        "format": "jsonl",
        "max_messages": 20,
        "timeout": 60
    }
    
    response = requests.post(
        f"{API_BASE}/download",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json()["download_id"]
    return None

def test_status(download_id):
    """Prueba consultar el estado"""
    print(f"\n📊 Consultando estado de {download_id}...")
    
    response = requests.get(f"{API_BASE}/status/{download_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.json() if response.status_code == 200 else None

def test_active():
    """Prueba listar descargas activas"""
    print("\n📋 Listando descargas activas...")
    
    response = requests.get(f"{API_BASE}/active")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    print("🚀 Probando Chat Downloader API")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("❌ Health check falló")
        return
    
    # Test download
    download_id = test_download()
    if not download_id:
        print("❌ No se pudo iniciar la descarga")
        return
    
    # Test status (esperar un poco)
    print("\n⏳ Esperando 10 segundos...")
    time.sleep(10)
    
    status = test_status(download_id)
    if status:
        print(f"📈 Estado actual: {status.get('status')}")
        print(f"📊 Mensajes capturados: {status.get('messages_count', 0)}")
    
    # Test active downloads
    test_active()
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    main()