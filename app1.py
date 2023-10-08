import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from textblob import TextBlob
import pandas as pd
import streamlit as st

from gtts import gTTS
from googletrans import Translator

from pydub import AudioSegment
import tempfile


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
    
st.title("Interfaces Multimodales")
st.subheader("TRADUCTOR")


image = Image.open('traductor.JPG')

st.image(image)

st.write("Toca el Botón y habla lo que quieres traducir")

stt_button = Button(label=" Inicio ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
    try:
        os.mkdir("temp")
    except:
        pass
    st.title("Texto a Audio")
    translator = Translator()
    
    text = str(result.get("GET_TEXT"))
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Francés", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Francés":
        input_language = "fr"    
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Francés", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Francés":
        output_language = "fr"  
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )
    
    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"
    
    
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    
    display_output_text = st.checkbox("Mostrar el texto")
    
    if st.button("convertir"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown(f"## Texto de salida:")
            st.write(f" {output_text}")
    
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)


#aqui empieza la otra interfaz
import streamlit as st
from googletrans import Translator

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
    except Exception as e:
        st.write("Ocurrió un error al traducir el texto.")

# Nota
st.sidebar.write("Nota: Este es un ejemplo simple de traducción. La precisión de la traducción puede variar.")


