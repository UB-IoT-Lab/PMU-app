# PMU-app
The application allows you to view  LTE transmission data ( identified by test identifier ) from Iot Sensors (identified by PMU identifier ). 
To list data in tabular form and download PDF or CSV , navigate to View Data.
To graph data of a particular transmission , navigate to Graph Data.
To start and stop listening server script for capturing live transmission data into SQLite database , navigate to Live Test.

## Deploy 
### clone git repository using
git clone [repo]

### change directory into the repo using
cd PMU-app

### Build docker containers and start application using 
docker-compose up --build

## Application views

### Table view 
The application reads an incoming packet from an IoT sensor from an opened socket, processes the packet to calculate 4G LTe transmission parameters such as delay from the arrival timestamp and GPS sensor timestamps. It then stores the processed data of the packet in a single row of a SQlite database.
![image](https://user-images.githubusercontent.com/36897394/188297295-8dae60ce-3b99-4ce3-a447-0c6c32e73c17.png)

### Graph view
As soon as the client side makes a requests for a particular test's data, the backend collects all the transmission data from the SQlite database and send the data to the browser. The front-end then processes the data to plot the technical graphs using D3 Javascript library. 
![image](https://user-images.githubusercontent.com/36897394/188297221-00f9abac-0954-464a-9833-80074b2671e5.png)
