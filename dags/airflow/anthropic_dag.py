from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import anthropic
import json
from pathlib import Path

# Define el cliente de la API
client = anthropic.Anthropic(
    api_key="szwQq0wdagYsCgDJw-xBdA8AAA",
)

# Carpeta raíz donde están los adjuntos
adjuntos_dir = Path("/home/ubuntu/adjuntos")

def cargar_pregunta():
    with open("/home/ubuntu/pregunta.txt", "r", encoding="utf-8") as file:
        pregunta = file.read().strip()
    return pregunta

# Función para procesar cada archivo ocr.txt
def procesar_ocr_txt(ocr_txt_path):
    pregunta = cargar_pregunta()

    with open(ocr_txt_path, "r", encoding="utf-8") as file:
        ocr_text = file.read()

    # Formatea el texto con el formato adecuado para la API
    consulta = f'"{pregunta}\\n\\n{ocr_text}\\n\\f"'

    # Realiza la consulta a la API de Anthropic
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": consulta
                    }
                ]
            }
        ]
    )

    # Convertimos los bloques de texto en un formato serializable (cadena de texto)
    respuesta_texto = "".join([block.text for block in message.content])
    
    return respuesta_texto

# Función principal para buscar archivos OCR y procesarlos
def procesar_todos_los_ocr(**kwargs):
    # Buscar todos los archivos ocr.txt en la carpeta adjuntos
    for ocr_txt_path in adjuntos_dir.rglob("ocr.txt"):
        print(f"Procesando archivo: {ocr_txt_path}")
        respuesta = procesar_ocr_txt(ocr_txt_path)

        # Definir la ruta donde se guardará el archivo JSON
        # Usamos el nombre de la carpeta donde está el ocr.txt para nombrar el archivo JSON
        nombre_carpeta = ocr_txt_path.parent.name
        json_output_path = ocr_txt_path.parent / f"{nombre_carpeta}_resultados.json"

        # Guardar la respuesta en un archivo JSON en la misma carpeta del ocr.txt
        with open(json_output_path, "w", encoding="utf-8") as json_file:
            json.dump({
                "archivo": str(ocr_txt_path),
                "respuesta": respuesta
            }, json_file, ensure_ascii=False, indent=4)
        
        print(f"Respuesta guardada en: {json_output_path}")

# Configuración del DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 10, 15),
}

with DAG(
    'procesar_ocr_anthropic',
    default_args=default_args,
    description='DAG para procesar archivos OCR con la API de Anthropic',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    procesar_ocr_task = PythonOperator(
        task_id='procesar_ocr',
        python_callable=procesar_todos_los_ocr,
        provide_context=True
    )

    procesar_ocr_task
