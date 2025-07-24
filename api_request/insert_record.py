from api_request import mock_fetch_data,fetch_data
import logging
import psycopg2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("weather_api.log"),  # Ghi log ra file
        logging.StreamHandler()  # Ghi log ra console
    ]
)

logger = logging.getLogger(__name__)

def connect_to_db():
    logging.info("Connecting to ProgresSQL!")
    
    try:
        conn = psycopg2.connect(
            host="database",
            port="5432",
            dbname="weather",
            user="quang",
            password="q"
        )
        return conn
    except psycopg2.Error as e:
        logger.error("Database connected failded: %s",e)
        raise
    
def create_table(conn):
    logger.info("Creating table if not exist..")
    try:    
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS wt;
            CREATE TABLE IF NOT EXISTS wt.raw_weather_data(
                id serial primary key,
                city text,
                temperature float,
                weather_description text,
                wind_speed float,
                time timestamp,
                inserted_at timestamp default now(),
                utc_offset text
            );         
        """)
        conn.commit()
        logger.info("Table was created")
    except psycopg2.Error as e:
        logger.info("Failed to create table %s",e)
        raise

def insert_record(conn , data):
    logger.info("Inserting weather data into the database...")
    try:
        weather = data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
            Insert into wt.raw_weather_data (
                city ,
                temperature ,
                weather_description ,
                wind_speed ,
                time ,
                inserted_at ,
                utc_offset 
            ) values (%s, %s , %s , %s , %s, NOW(), %s)             
        """,(
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        logger.info("Data successfully inserted")
    except psycopg2.Error as e:
        logger.info("Failed to insert table %s",e)
        raise

def main():
    try:
        # data = mock_fetch_data()
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_record(conn,data)
    except Exception as e:
        logger.info("Error occurred during excecuton %s",e)
    finally:
        if 'conn' in locals():
            conn.close()
            logger.info("Database connectuon closed") 
