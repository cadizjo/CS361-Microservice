// import dependencies (express server framework and advanced message queuing protocol library)
const express = require('express');
const amqp = require('amqplib/callback_api'); 
var fs = require("fs") // file manipulation

const app = express(); // create instance of server
const PORT = 5672; // establish port # to run process

// RabbitMQ connection details
// note: connection URL specifies the IPv4 loopback addr
const rabbitMQUrl = 'amqp://127.0.0.1';

// route to respond to client requests specified by pathname: '/add-songs'
app.get('/add-songs', (req, res) => {

  // after receiving client request...establish connection to RabbitMQ server using amqp instance
  amqp.connect(rabbitMQUrl, (error0, connection) => { 
    if (error0) {
      throw error0;
    }
    // create a channel for declaring message queue
    connection.createChannel((error1, channel) => { 
      if (error1) {
        throw error1;
      }

      const queue = 'csv_queue'; // name of queue

      // declare queue (note: obj of properties passed as arg where durable defines where metadata is stored (disk/ram))
      // Important: Because we might start the consumer before the publisher, we want to make sure the queue exists before we try to consume messages from it.
      channel.assertQueue(queue, {
        durable: false,
      });

      // to run more than one server process and spread the load equally over multiple servers we need to set the prefetch setting on channel
      channel.prefetch(1); 
      console.log(' [x] Awaiting RPC requests');

      // consume messages from the queue (requests from client) then call the reply callback function to perform operations and send a response to client
      channel.consume(queue, function reply(msg) {
        var input_file_path = msg.content.toString();
        var output_file_path = "./library.csv";

        console.log(" [.] ", input_file_path);

        // perform microservice operations using client request data/input file
        appendToLibrary(input_file_path, output_file_path)
        randomizeLibrary(output_file_path)

        // send response message to client process via message queue
        // note: For an RPC request, the Client and Server exchange messages using two properties: replyTo, which is set to the callback queue and correlationId, which is set to a unique value for every request and is useful for correlating RPC responses with requests.
        channel.sendToQueue(msg.properties.replyTo, Buffer.from(output_file_path.toString()), {
          correlationId: msg.properties.correlationId
        });

        channel.ack(msg); // acknowledge message and remove it from queue
      });
    });
  });
  // send server response to client
  res.send('CSV data request sent to server. Check the server console for details.');
});

// listens for any client connections on specified port
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});


// note: AMQP is language agnostic meaning that as long as you have clients that can connect to the same RabbitMQ server as this microservice you should be able to communicate between them


// helper functions

function shuffle(sourceArray) {
  for (var i = 0; i < sourceArray.length - 1; i++) {
      var j = i + Math.floor(Math.random() * (sourceArray.length - i));

      var temp = sourceArray[j];
      sourceArray[j] = sourceArray[i];
      sourceArray[i] = temp;
  }
  return sourceArray;
}

function appendToLibrary(input_file_path, output_file_path) {
  var libraryData, librarySongsList
  var librarySpotifyIdData = []
  var spotifyId
  var outputFileExists = 1

  // do nothing if input file does not exist/invalid
  if (!fs.existsSync(input_file_path)) {
    console.log("Input File not found");
    return
  }
  // o/w read input file contents
  var songsData = (fs.readFileSync(input_file_path)).toString(); // (synchronous/blocking operation)
  if (songsData.length == 0) return // do nothing if input file is empty
  var addSongsList = songsData.split("\n"); // convert to array

  // check if library/output file already exists using specified path
  if (!fs.existsSync(output_file_path)) {
    console.log("Output File not found");
    outputFileExists = 0
  }
  else { 
    // read file contents if it exists
    libraryData = (fs.readFileSync(output_file_path)).toString(); // (synchronous/blocking operation)
    librarySongsList = libraryData.split("\n"); // convert to array

    // get unique spotify ids of each record in output file
    for (var i = 0; i < librarySongsList.length - 1; i++) { // note: do length - 1 to not include whitespace
      spotifyId = (librarySongsList[i].split(","))[0]; // delimit each record to get spotify id at first idx
      librarySpotifyIdData.push(spotifyId); // append id to list
    }
    // console.log(librarySpotifyIdData)
  }

  // append new song entries to output file if it doesn't already exist in library (ie. spotify id doesnt match any existing entry or no entries exist at all)
  for (var i = 0; i < addSongsList.length - 1; i++) { // note: do length - 1 to not include whitespace
    spotifyId = (addSongsList[i].split(","))[0]
    console.log("searching...", spotifyId)

    if (!outputFileExists || !(librarySpotifyIdData.includes(spotifyId))) {  // 'includes' returns true if elem exists in array
      fs.appendFileSync(output_file_path, addSongsList[i] + "\n", {flag: 'a'}); // append song entry to output file (creating file if it doesn't exist)
      console.log("appending...")
    }
  }
}

function randomizeLibrary(output_file_path) {
  // do nothing if library/output file doesnt exist
  if (!fs.existsSync(output_file_path)) {
    console.log("Output File not found");
    return
  }
  // o/w randomize order of entries in output file
  libraryData = (fs.readFileSync(output_file_path)).toString(); // read updated library data file (synchronous/blocking operation)
  if (libraryData.length == 0) return // do nothing if input file is empty
  librarySongsList = libraryData.split("\n"); // convert to array

  var fileHeader = librarySongsList[0]
  var randomizedList = []

  // copy body of output file to new array
  for (var i = 1; i < librarySongsList.length - 1; i++) { // note: do length - 1 to not include whitespace
    randomizedList.push(librarySongsList[i])
  }

  // randomize body of output file (ie. not including header)
  randomizedList = shuffle(randomizedList)
  randomizedList.unshift(fileHeader)
  
  // empty output file
  fs.truncateSync(output_file_path, 0)

  // append each entry in randomizedList to output file
  for (var i = 0; i < randomizedList.length; i++) {
    fs.appendFileSync(output_file_path, randomizedList[i].toString())
    fs.appendFileSync(output_file_path, "\n")
  }
}