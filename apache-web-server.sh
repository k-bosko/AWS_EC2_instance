#!/bin/bash
# Install Apache Web Server and PHP
yum install -y httpd mysql php

# Download Lab files from AWS or replace the url with a link to the source code of your preferred website
# PASTE YOUR OWN RESOURCES instead of {name-of-your-public-bucket} and {name-of-your-zipped-website}
wget https://{name-of-your-public-bucket}.s3.amazonaws.com/{name-of-your-zipped-website}.zip
unzip {name-of-your-zipped-website}.zip -d /var/www/html/

# Turn on web server
chkconfig httpd on
service httpd start
