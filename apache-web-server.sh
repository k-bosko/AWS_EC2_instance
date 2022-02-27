#!/bin/bash
# Install Apache Web Server and PHP
yum install -y httpd mysql php

# Download Lab files from AWS or replace the url with a link to the source code of your preferred website
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-100-ACCLFO-2/2-lab2-vpc/s3/lab-app.zip
unzip lab-app.zip -d /var/www/html/

# Turn on web server
chkconfig httpd on
service httpd start
