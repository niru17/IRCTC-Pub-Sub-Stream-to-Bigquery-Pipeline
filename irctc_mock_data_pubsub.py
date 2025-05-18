from google.cloud import pubsub_v1
from datetime import datetime,timedelta,timezone
import json
import random
import uuid
import string

topic='irctc-data'
project_id='fit-legacy-454720-g4'

#Initializing Pub/Sub
def initialize_pubsub():
    try:
        publisher=pubsub_v1.PublisherClient()
        topic_path=publisher.topic_path(project_id,topic)
        return publisher,topic_path
    except Exception as e:
        print(f"Error occurred in initialization of pubsub due to: {e}")
        raise

#Generating mock data to Pub/Sub
def mock_data_pubsub(num_rows):
    try:
        data=[]
        for _ in range(num_rows):
            row_key=str(uuid.uuid4())
            row_data={
                "row_key":row_key,
                "name": ''.join(random.choices(string.ascii_letters,k=10)),
                "age":random.randint(18,90),
                "email":''.join(random.choices(string.ascii_letters,k=5)) + "@gmail.com",
                "join_date":(datetime.now()-timedelta(days=random.randint(0,3650))).strftime('%Y-%m-%d'),
                "last_login":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "loyalty_points":int(random.uniform(0,1000)),
                "account_balance":round(random.uniform(100,10000),2),
                "is_active":random.choice([True,False]),
                "inserted_at":datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at":None
            }
            data.append(row_data)
        return data
    except Exception as e:
        print(f"Error occurred at mock data generation: {e}")
        raise

#Publishing the mock_data to Pub/Sub  
def publish_to_pubsub(publisher,topic_path,data):
    try:
        for record in data:
            message_json=json.dumps(record)
            message_bytes=message_json.encode('utf-8')
            future=publisher.publish(topic_path,data=message_bytes)
            print(f"Data -> {message_json}")
            print(f"Published message ID: {future.result()}")
        print(f"Data of length {len(data)} messages published successfully!!")
    except Exception as e:
        print(f"Error occurred during publishing data to pubsub due to: {e}")
        raise

if __name__ == "__main__":
    try:
        publisher, topic_path=initialize_pubsub()

        mock_data=mock_data_pubsub(50)

        publish_to_pubsub(publisher,topic_path,mock_data)
    except Exception as e:
        print(f"Exception occurred due to {e}")

