# PMU-app
The application allows you to view  LTE transmission data ( identified by test identifier ) from Iot Sensors (identified by PMU identifier ). 
To list data in tabular form and download PDF or CSV , navigate to View Data.
To graph data of a particular transmission , navigate to Graph Data.
To start and stop listening server script for capturing live transmission data into SQLite database , navigate to Live Test.
The application reads an incoming packet from an IoT sensor at an opened socket, processes the packet to calculate 4G LTe transmission parameters such as delay from the arrival timestamp and GPS sensor timestamps. It then stores the processed data of the packet in a single row of a SQlite database.

## Deploy 
### clone git repository using
git clone [repo]

### change directory into the repo using
cd PMU-app

### Build docker containers and start application using 
docker-compose up --build

The docker service boots up two containers, NGinx and Flask in the desired server to serve the application. 
The port required for transmission data collection (7777) in the Flask container are mapped to the server port 7777 for UDP. NGINX runs the web server at port 80 to serve the flask application running at 8080 inside the Flask container.

## Application views

### Table view 

At the request from the client side for a particular transmission data, the backend sends the data of the transmission session and the front end uses datatable Javascript Library to display the data in a tabular form.
![image](https://user-images.githubusercontent.com/36897394/188297295-8dae60ce-3b99-4ce3-a447-0c6c32e73c17.png)

### Graph view
As soon as the client side makes a request for a particular test's data, the backend collects all the transmission data from the SQlite database and sends the data to the browser. The front-end then processes the data to plot the technical graphs using D3 Javascript library. 
![image](https://user-images.githubusercontent.com/36897394/188297221-00f9abac-0954-464a-9833-80074b2671e5.png)
