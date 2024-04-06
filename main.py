import json
import random
import time
from faker import Faker  # Importing Faker library for generating fake data
from confluent_kafka import SerializingProducer  # Importing the SerializingProducer from confluent_kafka
from datetime import datetime

fake = Faker()  # create Faker object for generating fake data


def generate_sales_transactions():
    # Function to generate fake sales transactions
    user = fake.simple_profile()  # Generating a fake user profile

    # Returning a dictionary representing a sales transaction
    return {
        "transactionId": fake.uuid4(),  # Unique transaction ID
        "productId": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        # Random product ID
        "productName": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        # Random product name
        'productCategory': random.choice(['electronic', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        # Random product category
        'productPrice': round(random.uniform(10, 1000), 2),  # Random product price
        'productQuantity': random.randint(1, 10),  # Random product quantity
        'productBrand': random.choice(['apple', 'samsung', 'oneplus', 'mi', 'boat', 'sony']),  # Random product brand
        'currency': random.choice(['USD', 'GBP']),  # Random currency
        'customerId': user['username'],  # Customer ID from fake user profile
        'transactionDate': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),  # Current UTC datetime
        "paymentMethod": random.choice(['credit_card', 'debit_card', 'online_transfer'])  # Random payment method
    }


def delivery_report(err, msg):
    """ Function to handle delivery report of Kafka messages """
    if err is None:
        # If successful(not error), print the message delivered information
        print(f"Message delivered to {msg.topic} [{msg.partition()}]")
    else:
        # If there's an error, print the message delivery failure
        print(f'Message delivery failed: {err}')


def main():
    # Main function
    topic = 'financial_transactions'  # Kafka topic name
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'  # Kafka broker address
    })  # Creating a Kafka producer object

    # curr_time = datetime.now()  # Getting the current time
    # while (datetime.now() - curr_time).seconds < 120:

    start_time = time.time()  # returns the current time in seconds

    # Looping for 120 seconds
    while time.time() - start_time < 120:

        try:
            transaction = generate_sales_transactions()  # Generating a fake sales transaction
            transaction['totalAmount'] = transaction['productPrice'] * transaction[
                'productQuantity']  # Calculating total amount

            print(f"transaction: {transaction}")  # Printing the transaction

            producer.produce(topic,  # Producing message to Kafka topic
                             key=transaction['transactionId'],  # Transaction ID as key
                             value=json.dumps(transaction),  # Serializing transaction to JSON format
                             on_delivery=delivery_report  # Specifying delivery report function
                             )

            # Polling the producer for delivery reports
            # - handle asynchronous events: allows the producer to handle asynchronous events,
            #   such as message deliveries or errors, without blocking the main execution flow
            # - ensure Responsiveness: ensures the script remains responsive by checking
            #   for pending events and promptly handles them
            producer.poll(0)

            # Waiting for 5 seconds before sending the next transaction
            time.sleep(5)

        # error due to producer
        except BufferError:
            # Handling buffer full exception
            print("Buffer full! Waiting to retry ...")
            # wait 1 sec before retrying to send the next transaction again, allowing some time for the buffer
            # to clear up before retrying to send the message.
            time.sleep(1)
        except Exception as e:
            # Handling other exceptions
            print(e)


if __name__ == "__main__":
    # execut main function if script is ran directly
    main()
