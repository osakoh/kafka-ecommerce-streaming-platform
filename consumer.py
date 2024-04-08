# docker exec -it broker kafka-console-consumer --bootstrap-server broker:9092 --topic financial_transactions
# docker exec -it broker kafka-console-consumer --bootstrap-server broker:9092 --topic financial_transactions --from-beginning


from confluent_kafka import Consumer, KafkaError


def consume_messages(topic, start_from_latest=True):
    """
        Consume messages from a Kafka topic.

        Parameters:
            topic (str): The name of the Kafka topic from which to consume messages.
            start_from_latest (bool, optional): Specifies whether to start consuming messages
                from the latest available message in the topic. If True, consumption starts
                from the latest message. If False, consumption starts from the earliest
                available message in the topic. Default is True.

        Returns:
            None

        Raises:
            KeyboardInterrupt: Raised when the user interrupts the program execution
                with Ctrl+C.

        Notes:
            This function continuously polls for messages from the specified Kafka topic.
            It prints the received messages to the console. The function runs indefinitely
            until interrupted by the user.

            Example usage:
            ```
            consume_messages('my_topic', start_from_latest=True)
            ```
        """
    conf = {
        'bootstrap.servers': 'localhost:9092',  # Kafka broker address
        'group.id': 'sales-events-consumer',  # Consumer group ID
        'auto.offset.reset': 'latest' if start_from_latest else 'earliest'  # Offset reset policy
    }

    consumer = Consumer(conf)

    consumer.subscribe([topic])  # Subscribe to the specified topic

    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for messages with a timeout of 1 second
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError.PARTITION_EOF:
                    # End of partition, no more messages to consume
                    continue
                else:
                    # Error occurred, handle it
                    print(f"Error: {msg.error()}")
                    break
            else:
                # Message successfully consumed
                print(f"Received message: {msg.value().decode('utf-8')}")

    except AttributeError as e:
        print(f"Error: {e}")

    except KeyboardInterrupt as e:
        print(f"\nUser pressed [Ctrl + C]: {e}")
        pass

    finally:
        # Close the consumer
        consumer.close()


if __name__ == "__main__":
    topic = 'financial_transactions'  # Kafka topic to consume from
    consume_messages(topic, start_from_latest=True)  # Consume from the latest message by default
