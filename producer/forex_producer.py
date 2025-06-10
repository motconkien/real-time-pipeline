import json 
import time 
import random
from kafka import KafkaProducer
from datetime import datetime

def create_forex_data():
    # Simulate forex data and return time, currency pair, and bid/ask price, volumn
    currency_pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD']
    return {
        'timestamp': datetime.now().isoformat(),
        'currency_pair': random.choice(currency_pairs),
        'bid_price': round(random.uniform(1.0, 2.0), 4),
        'ask_price': round(random.uniform(1.0, 2.0), 4),
        'volume': random.randint(100, 10000)
    }

def main():
    #create producer object
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8') #convert dict to json -> byte. In this case value = forex_data 
    
    )

    print("Forex producer started...")
    try:
        while True:
            #random data generation
            forex_data = create_forex_data()
            print(f"Producing data: {forex_data}")
            try:
                producer.send('forex_topic', value=forex_data) #send to kafka tpice calle forex_topic and call lambda function as well
                producer.flush()  # Ensure the message is sent immediately
            except Exception as e:
                print(f"Failed to send message: {e}")
                # Sleep for a while before sending the next message
                time.sleep(1)  # Sleep for 1 second before sending the next message
            time.sleep(2)
    except Exception as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        producer.flush()
        producer.close()
        print("Producer closed.")

if __name__ == "__main__":
    main()