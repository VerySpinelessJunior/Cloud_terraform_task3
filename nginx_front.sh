#!/bin/bash
echo "Beginning installation of nginx web server"
if ! which nginx > /dev/null 2>&1; then
    echo "Nginx is not installed"
else
    echo "Installing nginx"
    yum install nginx -y
    
    #check if nginx services are up
    service nginx start
fi
