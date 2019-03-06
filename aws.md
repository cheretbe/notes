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

* Images
    * https://aws.amazon.com/marketplace
    * https://stackoverflow.com/questions/40835953/how-to-find-ami-id-of-centos-7-image-in-aws-marketplace
* Networking
    * https://www.blog.labouardy.com/create-a-aws-vpc-with-terraform/
    * https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnets-commands-example.html
    * https://www.assistanz.com/creating-vpc-with-nat-instance/
    * https://medium.com/@brad.simonin/create-an-aws-vpc-and-subnet-using-the-aws-cli-and-bash-a92af4d2e54b
    * https://serverfault.com/questions/406351/how-to-configure-a-custom-nat-for-use-in-amazon-vpc/406508
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
```
