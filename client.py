# use command: 'pip install pika requests' in shell to install python dependencies on local OS
# pika is a pure-Python library for interacting with RabbitMQ, which is a message broker software that implements the Advanced Message Queuing Protocol (AMQP). 
# pika serves as a client library for Python applications to communicate with RabbitMQ.

import requests
import pika
import uuid

queue_name = "csv_queue" # name of queue (matches queue that sender process publishes to)

# class to represent a single RPC (remote procedure call) that will request data from a microservice (using RabbitMQ to exchange data)
# note: A remote procedure call is an interprocess communication technique that is used for client-server based applications (ref: https://www.rabbitmq.com/tutorials/tutorial-six-python.html)
class RpcClient(object):

    # constructor
    def __init__(self):

        # establish connection to RabbitMQ at specified host using pika
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        # create a channel for declaring message queue
        self.channel = self.connection.channel()

        # declare an exclusive callback queue for receiving replies 
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # subscribe to the callback_queue, so that we can receive RPC responses.
        # this method is called each time a message is delivered from RabbitMQ
        self.channel.basic_consume(
            queue=self.callback_queue, # specified queue
            on_message_callback=self.on_response, # assigned callback function 
            auto_ack=True) # acknowledge each message after receiving

        # initialize rpc response contents to null
        self.response = None
        self.corr_id = None

    # callback function that gets called after receiving an RPC response
    # for every response message, check if the correlation_id is the one we're looking for. If so, save the response in self.response and breaks the consuming loop
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    # initiates an RPC request
    def call(self, input_file_path):
        self.response = None

        # generate a unique id (correlation id per request). 'on_response()' callback function will use this value to catch the appropriate response.
        self.corr_id = str(uuid.uuid4()) 

        # publish the request message to specified queue (routing key), with two properties: reply_to and correlation_id, and include body of message
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(input_file_path))
        
        # Make a request to the server to initiate request and data retrieval
        server_url = "http://localhost:5672/add-songs"
        response = requests.get(server_url)

        # check response status from server
        if response.status_code == 200:
            print("CSV data request initiated successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        # Receive messages from queue - wait until the proper response arrives and return the response back to the user.
        self.connection.process_data_events(time_limit=None)
        return self.response
    

rpc = RpcClient() # instantiate an RPC object

print(" [x] Requesting rpc()")
response = rpc.call("./add-songs.csv")
print(f" [.] Got {response}")