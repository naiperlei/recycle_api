from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from keras.models import load_model
from PIL import Image
import numpy as np

app = FastAPI()

#Cargar el modelo de la red neuronal
model=load_model('best_model.h5')

# Función para preprocesar la imagen antes de hacer la predicción
def preprocess_image(image):
    img = image.convert('RGB') #convertimos imagen a rgb en caso de que sea rgba
    img = img.resize((64,64))  #ponemos el tamaño que necesita la red
    img_array = np.array(img) / 255  #normalizamos los valores
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión extra para el lote

    return img_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Abrir la imagen y preprocesarla
    image = Image.open(file.file)
    processed_image = preprocess_image(image)

    # Hacer la predicción utilizando el modelo cargado
    predictions = model.predict(processed_image)

    # Devolver las predicciones en formato JSON
    return JSONResponse(content={"predictions": predictions.tolist()})




