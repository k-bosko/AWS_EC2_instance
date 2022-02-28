# AWS EC2 instance
In this lab, I launched my website www.cross-validated.com on AWS EC2 instance using Python SDK. 

## Steps:
1. Created a custom VPC
2. Created a subnet in this VPC
3. Created an internet gateway 
4. Attached internet gateway to my VPC
5. Retrieved the main route table id that was created together with VPC and added quad-zero route to this route table
6. Associated the route table with my subnet
7. Created a security group 
8. Authorized SSH and HTTP access through two inbound rules
9. Launched EC2 instance - Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type - with 10 GB storage. 
10. Added a shell script to UserData when launching the EC2 instance. 
    The script installs and launches Apache web server. It also copies over the website that is stored on Amazon S3 bucket to the launched EC2 instance.
    
    
