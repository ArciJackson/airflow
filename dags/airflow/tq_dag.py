from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime

# Función para conectarse a la base de datos y ejecutar una consulta
def ejecutar_consulta():
    # Crear una conexión utilizando el Hook de MySQL
    mysql_hook = MySqlHook(mysql_conn_id='helpdesk')  # ID de conexión en Airflow o variable de entorno
    conn = mysql_hook.get_conn()  # Obtener la conexión
    cursor = conn.cursor()  # Crear un cursor para ejecutar la consulta

    # Ejecutar la consulta para mostrar las bases de datos
    cursor.execute("SHOW DATABASES;")
    result = cursor.fetchall()  # Obtener los resultados

    # Imprimir los resultados en los logs de Airflow
    for row in result:
        print(row)

    cursor.close()
    conn.close()

# Definir el DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 23),
}

with DAG('consulta_mariadb', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    
    # Tarea para ejecutar la consulta
    consulta_db = PythonOperator(
        task_id='ejecutar_consulta_db',
        python_callable=ejecutar_consulta
    )

    consulta_db

