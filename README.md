# CS361-Microservice - Spotify Playlist File Transformer

This microservice will process song entries in a spotify playlist provided by the user as a *.csv file. Song entries are appended to an existing library (*.csv) where the concatenated file is then randomized and returned to the user (containing no duplicate entries).

Request Data

A client running on the same local machine communicates with the microservice using a Remote Procedure Call (RPC) that will request data from the microservice using RabbitMQ as a message broker. A remote procedure call is an interprocess communication technique that is used for client-server based applications (ref: https://www.rabbitmq.com/tutorials/tutorial-six-python.html). 

The client initiates a request by:
1. Establishing a connection to the RabbitMQ message broker located on the same network as the microservice (amqp://127.0.0.1) (note: third-party libraries will need to be imported on the client application. eg. if using Python, 'pika' and 'requests' will need to be manually imported).
2. Connect to the same message queue as the microservice to publish and consume messages (documentation: https://www.rabbitmq.com/tutorials/tutorial-six-python.html)
3. Make an HTTP request to the microservice located at http://localhost:5672/add-songs to initiate a request and send the Spotify input .csv file to the message queue to be retrieved by the microservice. (note: requests can be made from the client application without needing to use a web browser - https://requests.readthedocs.io/en/latest/).

Receive Data

After processing a client request, the microservice will send the pathname of the 'library.csv' file to the user and generate/update the file in the same directory as the microservice.