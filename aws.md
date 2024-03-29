* Regions
    * `eu-north-1` - Europe (Stockholm)
    * `eu-central-1` - Europe (Frankfurt)
* TODO
    * Try running PowerShell in Lambda
    * https://aws.amazon.com/solutions/implementations/distributed-load-testing-on-aws/
* Types of EC2 storage
    * EC2 Instance Store - not detachable, ephemeral (destroyed on shudown). Survives reboots though. High IOPS, no additional cost (included in in the price of the instance)
    * EBS (Elastic Block Store) - detachable, persistent, suports different types of snaphots. Single AZ. Block level.
    * EFS (Elastic File System)  - network storage (NFS 4.0/4.1, therefore no Windows support), can be mounted on multiple ec2 instances and this storage can be available in multiple AZ. File tree level.
* **AWS Storage Gateway** is a set of hybrid cloud storage services that provide on-premises access to virtually unlimited cloud storage.
    * File gateway - NFS 3/4 to S3
    * Stored volume gateway - backup to S3 of local iSCSI storage (max 32 volumes of 1GiB to 16TiB)
    * Cached volume gateway - iSCSI to S3 (max 32 volumes of up to 32TiB)
    * Virtual tape library gateway - virtual tape library to S3 or Glacier
* **AWS Snowball** - physical devices, that shipped from/to Amazon to transfer data to/from S3
* A **security group** is an AWS firewall solution that performs one primary function: to filter incoming and outgoing traffic from an EC2 instance. It accomplishes this filtering function at the TCP and IP layers, via their respective ports, and source/destination IP addresses.
* **AWS Fargate** is a serverless, pay-as-you-go compute engine that lets you focus on building applications without managing servers. AWS Fargate is compatible with both **ECS** (Amazon Elastic Container Service) and **EKS** (Amazon Elastic Kubernetes Service)
* **ECR** (Elastic Container Registry) is a managed container image registry service: https://aws.amazon.com/ecr/ 
* **CloudFormation** is a method of provisioning AWS infrastructure as code. CloudFormation works by defining your AWS resources in a structured text file in either JSON or YAML formats. This is known as a CloudFormation template. Using the template, you then create a CloudFormation stack in AWS which contains all the resources you defined.
* **AWS Elastic Beanstalk** is a service for deploying and scaling web applications and services. You can simply upload your code and Elastic Beanstalk automatically handles the deployment, from capacity provisioning, load balancing, auto-scaling to application health monitoring. At the same time, you retain full control over the AWS resources powering your application and can access the underlying resources at any time.
* **AWS Lambda** is a serverless compute service which has been designed to allow you to run your application code without having to manage and provision your own EC2 instances.
* **SQS** (Amazon Simple Queue Service) is a fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications.
* **CloudFront** - Low-latency CDN
* **RDS** (Relational Database Service) is a collection of managed database services (Amazon Aurora with MySQL compatibility, Amazon Aurora with PostgreSQL compatibility, MySQL, MariaDB, PostgreSQL, Oracle, SQL Server)
* **DynamoDB** is a fully managed NoSQL database service
* **ElastiCache** is a fully managed, in-memory caching service (compatible with Redis and Memcached)
* **Neptune** is a fully managed graph database
* **Redshift** is a data warehouse (based on PostgreSQL with custom modifications). ETL (extract, transform, load) and analytics on a very large scale.
* **DocumentDB** is a scalable, highly durable, and fully managed database service for operating mission-critical MongoDB workloads
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

### AWS CLI

#### Installation

* https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
    * :warning: `pip install awscli` installs version 1
    * [awscliv2](https://pypi.org/project/awscliv2/) is unofficial and there are no plans to publish it on PyPi (https://github.com/aws/aws-cli/issues/4947#issuecomment-793192340)
```shell
# Install as local user (default locations are /usr/local/aws-cli and /usr/local/bin
./aws/install -i ~/.local/share/aws-cli -b /usr/local/bin
```
    
```bash
# Configure (this creates/updates .aws/config and .aws/credentials)
aws configure
```

#### Useful Commands

```shell
# List all resources in all regions
for region in `aws ec2 describe-regions --output text | cut -f4`
do
     echo -e "\nListing resources in region: $region..."
     aws resourcegroupstaggingapi get-resources --region $region --query "ResourceTagMappingList[][ResourceARN]" --output table
done
```

#### EC2 Instances

```shell
# List all EC2 instances across all regions
for region in `aws ec2 describe-regions --output text | cut -f4`
do
     echo -e "\nListing Instances in region: $region..."
     # aws ec2 describe-instances --region $region
     aws ec2 describe-instances --region $region --query "Reservations[].Instances[][InstanceId,InstanceType,LaunchTime,State.Name]" --output table
done
```

#### EC2 AMI
```shell
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
