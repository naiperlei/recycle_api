from fastapi import FastAPI, BackgroundTasks
import requests
import os
import time

app = FastAPI()

# Definir las URL de las páginas web de donde se descargarán los archivos JSON
urls = [
    "https://valencia.opendatasoft.com/api/v2/catalog/datasets/contenidors-residus-solids-contenidores-residuos-solidos/exports/json",
    "https://valencia.opendatasoft.com/api/v2/catalog/datasets/contenidors-vidre-contenedores-vidrio/exports/json"
]

# Directorio donde se guardarán los archivos descargados
download_dir = "json"

# Función para descargar los archivos JSON y reemplazar los existentes
def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(download_dir, f"{url.split("/")[-3]}.json")
        # Eliminar el archivo existente si hay uno
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Archivo {filename} descargado y reemplazado correctamente.")
    else:
        print(f"No se pudo descargar el archivo desde {url}.")

# Tarea de fondo para descargar los archivos JSON
def download_json_periodically():
    while True:
        print("Descargando archivos JSON...")
        for url in urls:
            download_json(url)
        time.sleep(24 * 60 * 60)  # Esperar 24 horas

# Ruta para iniciar la tarea de descarga de archivos
@app.get("/")
async def start_download(background_tasks: BackgroundTasks):
    background_tasks.add_task(download_json_periodically)
    return {"message": "Tarea de descarga iniciada."}



