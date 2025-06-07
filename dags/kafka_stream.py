from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import logging

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 10, 1, 10, 00)
}

def get_data():
    import requests
    
    try:
        res = requests.get('https://randomuser.me/api/')
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API request failed: {e}")
        return {"error": str(e)}

def format_data(res):
    if "error" in res:
        return res
    
    try:
        user = res['results'][0]
        formatted_data = {
            'first_name': user['name']['first'],
            'last_name': user['name']['last'],
            'gender': user['gender'],
            'address': f"{user['location']['street']['number']} {user['location']['street']['name']}, {user['location']['city']}, {user['location']['state']}, {user['location']['country']}",
            'postcode': user['location']['postcode'],
            'email': user['email'],
            'username': user['login']['username'],
            'dob': user['dob']['date'],
            'registered_date': user['registered']['date'],
            'phone': user['phone'],
            'picture': user['picture']['large'],
        }
        return formatted_data
    except KeyError as e:
        return {"error": f"Missing field in API response: {e}"}

def stream_data():
    import json
    from kafka import KafkaProducer
    import logging

    # Get and format data first
    res = get_data()
    res = format_data(res)
    
    # Check if there's an error in the data
    if "error" in res:
        logging.error(f"Data error: {res['error']}")
        return res
    
    print(json.dumps(res, indent=2))
    
    producer = None
    try:
        # Create Kafka producer with proper configuration
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            max_block_ms=5000,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),  # Handle serialization automatically
            retries=3,
            acks='all'
        )
        
        print(f"Producer created successfully. Sending to topic: users_created")
        
        # Send message to Kafka
        future = producer.send('users_created', res)  # Send dict directly, serializer handles JSON
        print(f"Message queued for sending...")
        
        # Wait for message to be sent and get confirmation
        record_metadata = future.get(timeout=10)
        
        print(f"✅ Message sent successfully!")
        print(f"Topic: {record_metadata.topic}")
        print(f"Partition: {record_metadata.partition}")
        print(f"Offset: {record_metadata.offset}")
        
        # Ensure all messages are sent before closing
        producer.flush()
        print("Producer flushed successfully")
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        logging.error(f"Failed to send message to Kafka: {e}")
        return {"error": f"Kafka send failed: {e}"}
    
    finally:
        # Always close the producer
        if producer is not None:
            producer.close()
            print("Producer closed")
    
    return res


with DAG('user_automation',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:
    
    stream_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data,
    )

# Add this for direct testing
if __name__ == "__main__":
    print("Testing stream_data function directly...")
    result = stream_data()
    print("Direct test complete.")
