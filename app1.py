import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

import os
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import time
import glob

from textblob import TextBlob
import pandas as pd

from gtts import gTTS
from googletrans import Translator

import tempfile
import subprocess

st.title("Reconocimiento óptico de Caracteres")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
      filtro = st.radio("Aplicar Filtro",('Con Filtro', 'Sin Filtro'))


if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Con Filtro':
         cv2_img=cv2.bitwise_not(cv2_img)
    else:
         cv2_img= cv2_img
    
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text=pytesseract.image_to_string(img_rgb)
    st.write(text) 


#aqui empieza la otra interfaz

# Título de la aplicación
st.title("Traductor de Texto")

# Entrada de texto
texto_a_traducir = st.text_area("Escribe el texto que deseas traducir:")

# Selección del idioma de destino
idioma_destino = st.selectbox("Selecciona el idioma de destino:", ["Español", "Inglés", "Francés", "Alemán"])

# Traducción del texto
translator = Translator()
if texto_a_traducir:
    try:
        if idioma_destino == "Español":
            traduccion = translator.translate(texto_a_traducir, dest="es").text
        elif idioma_destino == "Inglés":
            traduccion = translator.translate(texto_a_traducir, dest="en").text
        elif idioma_destino == "Francés":
            traduccion = translator.translate(texto_a_traducir, dest="fr").text
        elif idioma_destino == "Alemán":
            traduccion = translator.translate(texto_a_traducir, dest="de").text
        else:
            traduccion = "Seleccione un idioma de destino válido"
        
        st.write("Texto traducido:")
        st.write(traduccion)

      
        # Reproducir audio de la traducción
        audio = gTTS(text=traduccion, lang=idioma_destino.lower())
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            audio.save(temp_audio_file.name)
            audio_path = temp_audio_file.name

        # Crear un botón para reproducir el audio
        if st.button("Reproducir Audio"):
            os.system(f"afplay {audio_path}")  # Esto funciona en macOS
            # Puedes ajustar el comando según tu sistema operativo si no estás en macOS

      
    except Exception as e:
        st.write("Ocurrió un error al traducir el texto.")
