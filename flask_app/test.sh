#!/bin/bash

# Start the first process
# python3 server.py &
  
uwsgi app.ini &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
