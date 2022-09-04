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
![image](https://user-images.githubusercontent.com/36897394/188297295-8dae60ce-3b99-4ce3-a447-0c6c32e73c17.png)

### Graph view
![image](https://user-images.githubusercontent.com/36897394/188297221-00f9abac-0954-464a-9833-80074b2671e5.png)
