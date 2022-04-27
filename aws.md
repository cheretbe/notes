* TODO
    * Try running PowerShell in Lambda
* Types of EC2 storage
    * EC2 Instance Store - not detachable, ephemeral (destroyed on shudown). Survives reboots though. High IOPS, no additional cost (included in in the price of the instance)
    * EBS (Elastic Block Store) - detachable, persistent, suports different types of snaphots. Single AZ. Block level.
    * EFS (Elastic File System)  - network storage (NFS 4.0/4.1, therefore no Windows support), can be mounted on multiple ec2 instances and this storage can be available in multiple AZ. File tree level.
* A **security group** is an AWS firewall solution that performs one primary function: to filter incoming and outgoing traffic from an EC2 instance. It accomplishes this filtering function at the TCP and IP layers, via their respective ports, and source/destination IP addresses.
* **AWS Fargate** is a serverless, pay-as-you-go compute engine that lets you focus on building applications without managing servers. AWS Fargate is compatible with both **ECS** (Amazon Elastic Container Service) and **EKS** (Amazon Elastic Kubernetes Service)
* **ECR** (Elastic Container Registry) is a managed container image registry service: https://aws.amazon.com/ecr/ 
* **CloudFormation** is a method of provisioning AWS infrastructure as code. CloudFormation works by defining your AWS resources in a structured text file in either JSON or YAML formats. This is known as a CloudFormation template. Using the template, you then create a CloudFormation stack in AWS which contains all the resources you defined.
* **AWS Elastic Beanstalk** is a service for deploying and scaling web applications and services. You can simply upload your code and Elastic Beanstalk automatically handles the deployment, from capacity provisioning, load balancing, auto-scaling to application health monitoring. At the same time, you retain full control over the AWS resources powering your application and can access the underlying resources at any time.
* **AWS Lambda** is a serverless compute service which has been designed to allow you to run your application code without having to manage and provision your own EC2 instances.
* **SQS** (Amazon Simple Queue Service) is a fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications.
* **CloudFront** - Low-latency CDN
* SES (Amazon Simple Email Service): https://aws.amazon.com/ses/
* AWS Elastic IP: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html
* IAM (Identity and Access Management): https://console.aws.amazon.com/iam/

* CHR RouterOS 6.34.1: `ami-4e739221`

CNAME for S3 (www.johnsmith.net -> www.johnsmith.net.s3.amazonaws.com): http://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html

* https://docs.aws.amazon.com/vm-import/latest/userguide/what-is-vmimport.html
* https://github.com/defionscode/centos7_builder
* https://rzn.id.au/tech/converting-an-ova-to-an-amazon-ami/
* https://stackoverflow.com/questions/14511202/error-importing-vmdk-files-using-ec2-developer-tools
* https://blog.zhaw.ch/icclab/walk-through-importing-virtual-machine-images-into-ec2/
* https://wiki.mikrotik.com/wiki/Manual:CHR_AWS_installation

Move to TODO/2read: https://www.blog.labouardy.com/

* Billing
    * https://www.reddit.com/r/aws/comments/6bgmul/is_there_a_way_of_seeing_what_resource_is/
* Images
    * https://aws.amazon.com/marketplace
    * https://askubuntu.com/questions/53582/how-do-i-know-what-ubuntu-ami-to-launch-on-ec2/53586#53586
    * https://cloud-images.ubuntu.com/locator/ec2/
    * https://stackoverflow.com/questions/40835953/how-to-find-ami-id-of-centos-7-image-in-aws-marketplace
    * https://access.redhat.com/solutions/15356
* Networking
    * https://www.blog.labouardy.com/create-a-aws-vpc-with-terraform/
    * https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnets-commands-example.html
    * https://www.assistanz.com/creating-vpc-with-nat-instance/
    * https://medium.com/@brad.simonin/create-an-aws-vpc-and-subnet-using-the-aws-cli-and-bash-a92af4d2e54b
    * https://serverfault.com/questions/406351/how-to-configure-a-custom-nat-for-use-in-amazon-vpc/406508
    * https://medium.com/@rakeshkanagaraj1990/aws-nat-instance-port-forwarding-475fbcf2585f
* Terraform
    * https://hackernoon.com/introduction-to-aws-with-terraform-7a8daf261dc0
* AWS CLI
    * The [JMESPath](http://jmespath.org/) language is used for filtering **on client side** (--query)
    * http://blog.xi-group.com/2015/01/small-tip-how-to-use-aws-cli-filter-parameter/
    * https://cloudonaut.io/6-tips-and-tricks-for-aws-command-line-ninjas/
* Metadata
    * https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    * https://stackoverflow.com/questions/42314029/whats-special-about-169-254-169-254-ip-address-for-aws
    
```bash
# Configure (this creates/updates .aws/config and .aws/credentials)
aws configure

# Find latest Ubuntu Xenial AMI
aws ec2 describe-images --region eu-central-1 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-xenial*" --query "sort_by(Images, &CreationDate)[-1].[ImageId,Name]" --output text
# Get ID
imageId=$(aws ec2 describe-images --region eu-central-1 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-xenial*" --query "sort_by(Images, &CreationDate)[-1].ImageId" --output text)
# To find out available filters use help command
aws ec2 describe-images help
# View image info by ID
aws ec2 describe-images --region eu-central-1 --filters "Name=image-id,Values=ami-09de4a4c670389e4b" --query "Images[*].[ImageId,Name,OwnerId]" --output text
# List images by owner ordered by date
aws ec2 describe-images --region eu-central-1 --owners 309956199498 --query "sort_by(Images, &CreationDate)[*].[ImageId,Name,CreationDate]" --output text
```
CloudWatch filter examples
```
[version, accountid, interfaceid, srcaddr, dstaddr, srcport, dstport=22, protocol, packets, bytes, start, end, action, logstatus]
```
