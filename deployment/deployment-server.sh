#!/bin/bash

echo "Starting deployment server on port 3005"
while true; do
  netcat -l -p 3005 >> nodes.txt
  echo "New client request"
done
