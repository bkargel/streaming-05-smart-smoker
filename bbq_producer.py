"""
    This program sends a message every 30 seconds to a queue on the RabbitMQ server. Data is sent to one,
    two, or three queues depending on the row content of a csv file (smoker-temps.csv).
    
    Author: Brendi Kargel
    Date: September 18, 2023

"""

import pika
import sys
import webbrowser
import csv

# Configure logging
from util_logger import setup_logger

logger, logname = setup_logger(__file__)

# Declare program constants (typically constants are named with ALL_CAPS)

HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "smoker-temps.csv"
queue1 = "01-smoker"
queue2 = "02-food-A"
queue3 = "03-food-B"

# Only opens the Admin website if show_offer = True
show_offer = False

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    global show_offer
    if show_offer:
        webbrowser.open_new("http://localhost:15672/#/queues")

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        logger.info(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        logger.info(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

def read_tasks_from_csv(file_name):
    """Read tasks from a CSV file and return them as a list."""
    tasks = []
    with open(file_name, "r") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            if row:
                tasks.append(row[0])  # Extract the task from the first column
    return tasks

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()
    
    # Read the task from the csv file
    tasks = read_tasks_from_csv(INPUT_FILE_NAME)

    # Loop through the csv file until all tasks have been sent
    for x in tasks:
        send_message("localhost", "task_queue3", x)
