Inventory Tool
============

Automation tool : 

Using inventory listing tool, you can list all or specific instances running/stopped/terminated in AWS account:

Please check if python is installed. If you are running RHEL, run below:

yum groupinstall -y development
or;

yum groupinstall -y 'development tools’

If Ubuntu :

Install Easy Install

$ sudo apt-get install python-setuptools python-dev build-essential 

Install pip

$ sudo easy_install pip 

Install virtualenv

$ sudo pip install --upgrade virtualenv 

Later run : pip install --upgrade pip

Now, download the setup files for pip and have Python (2.7) install it:

This will install it for version 2.7.6


curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python2.7 -



Steps 1) sudo python setup.py install

Step 2) execute : instancelist-cli --help 

Step 3) Uninstalling instancelist-cli (sudo pip uninstall instancelist-cli) 


usage: instancelist-cli [-h] [-p PROFILE] [--filter FILTER]

optional arguments:
  -h, --help            show this help message and exit
    -p PROFILE, --profile PROFILE
                            Configuration profile
                              --filter FILTER       Amazon EC2 API filter to limit the result returned.
                                                      (Example: --filter running)
Please make sure that you create ~/.cred/config file and add aws key and secret in config file, it would like below:

Here [Default]  is default profile selected.

Below is content of ~/.cred/config 

[Default] 
key=xxxxxxxx
secret= xxxxxxxx
                                                             
[QA]
key= xxxxxxxx
secret= xxxxxxxx
                                                                    
[Dev]
key= xxxxxxxx
secret= xxxxxxxx
