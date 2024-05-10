from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from keras.models import load_model
from PIL import Image
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to limit access to specific origins
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

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
    #image= Image.open('broken-bottle.jpg')
    processed_image = preprocess_image(image)

    # Hacer la predicción utilizando el modelo cargado
    predictions = model.predict(processed_image)

    # Devolver las predicciones en formato JSON
    return JSONResponse(content={"predictions": predictions.tolist()})

@app.get("/")
async def menu(request: Request):
    return templates.TemplateResponse(
    request=request, name="index.html"
)