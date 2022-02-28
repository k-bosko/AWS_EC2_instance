#!/bin/bash
# Install Apache Web Server and PHP
yum install -y httpd mysql php

# Download Lab files from AWS or replace the url with a link to the source code of your preferred website
wget https://lab2-kbosko-website.s3.amazonaws.com/kbosko-website.zip
unzip kbosko-website.zip -d /var/www/html/

# Turn on web server
chkconfig httpd on
service httpd start
