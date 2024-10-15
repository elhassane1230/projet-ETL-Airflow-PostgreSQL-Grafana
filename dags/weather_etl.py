from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
import requests
from datetime import datetime

API_KEY = 'Your_API_Key'
CITY = 'Paris'
BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Fonction de validation des données
def validate_data(data):
    if data['main']['temp_min'] < -100 or data['main']['temp_max'] > 60:
        raise ValueError("Invalid temperature range")
    if not (0 <= data['main']['humidity'] <= 100):
        raise ValueError("Invalid humidity value")
    if data['wind']['speed'] < 0:
        raise ValueError("Invalid wind speed")

# Fonction d'extraction
def extract_weather_data(**kwargs):
    response = requests.get(BASE_URL)
    data = response.json()
    
    if response.status_code == 200:
        validate_data(data)
        kwargs['ti'].xcom_push(key='raw_weather_data', value=data)
    else:
        raise Exception("Error fetching data from OpenWeatherMap")

# Fonction de transformation et calcul de nouvelles métriques
def transform_weather_data(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(key='raw_weather_data', task_ids='extract_weather_data')
    
    if raw_data:
        transformed_data = {
            'city': raw_data['name'],
            'date': datetime.fromtimestamp(raw_data['dt']).date(),
            'temperature_min': raw_data['main']['temp_min'],
            'temperature_max': raw_data['main']['temp_max'],
            'humidity': raw_data['main']['humidity'],
            'wind_speed': raw_data['wind']['speed'],
            'weather_condition': raw_data['weather'][0]['description'],
            'comfort_index': (raw_data['main']['temp_min'] + raw_data['main']['temp_max']) / 2 - (0.55 * (1 - raw_data['main']['humidity'] / 100) * (raw_data['main']['temp_max'] - 14))
        }
        kwargs['ti'].xcom_push(key='transformed_weather_data', value=transformed_data)
    else:
        raise Exception("No raw data to transform")

# Fonction de chargement dans PostgreSQL
def load_to_postgresql(**kwargs):
    weather_data = kwargs['ti'].xcom_pull(key='transformed_weather_data', task_ids='transform_weather_data')

    if weather_data:
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        sql = """
            INSERT INTO weather (city, date, temperature_min, temperature_max, humidity, wind_speed, weather_condition, comfort_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        pg_hook.run(sql, parameters=(
            weather_data['city'], 
            weather_data['date'], 
            weather_data['temperature_min'], 
            weather_data['temperature_max'], 
            weather_data['humidity'], 
            weather_data['wind_speed'], 
            weather_data['weather_condition'],
            weather_data['comfort_index']
        ))
    else:
        raise Exception("No transformed data to load")

# Définir le DAG
with DAG('weather_etl', start_date=datetime(2024, 10, 10), schedule_interval='@hourly') as dag:
    
    extract_task = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract_weather_data,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform_weather_data,
        provide_context=True
    )
    
    load_task = PythonOperator(
        task_id='load_to_postgresql',
        python_callable=load_to_postgresql,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
