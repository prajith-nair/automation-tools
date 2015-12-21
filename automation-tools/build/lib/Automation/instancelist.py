

"""
" Author : Prajith Nair
"""

__version__ = "0.0.2"
import csv
import logging
import argparse
import boto.ec2
import boto.ec2.cloudwatch
import boto
import ConfigParser
import os
import sys,getopt
from os.path import expanduser
from prettytable import PrettyTable as table

# list if default regions selected by default
aws_regs = [ "us-east-1" , "us-west-1", "us-west-2", "eu-west-1", "ap-southeast-1", "ap-northeast-1", "ap-southeast-2", "sa-east-1" ]
tbl = table(["Instance Name", "Instance-id", "DNS","Public IP", "Size", "Region", "Private IP","VPC Id", "Start Time", "Status"])
dependency_dictionary = {}


def setup_config():
    config_home = os.path.sep.join([expanduser('~'),'.cred','config'])
    if (not os.path.exists(config_home)):
        logging.error("Configurations not initialized")
        raise SystemExit
    return config_home

#---------------------------------------------------------------------------
#   A dictionary of colors
#---------------------------------------------------------------------------
colors = {
    'END' : '\033[0m',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m',
    'RED' : '\033[31m',
    'GREEN' : '\033[32m',
    'YELLOW' : '\033[33m',
    'BLUE' : '\033[34m',
    'PURPLE' : '\033[35m',
    'CYAN' : '\033[36m',
    'RED_LIGHT' : '\033[91m',
    'GREEN_LIGHT' : '\033[92m',
    'YELLOW_LIGHT' : '\033[93m',
    'BLUE_LIGHT' : '\033[94m',
    'PURPLE_LIGHT' : '\033[95m',
    'CYAN_LIGHT' : '\033[96m',
    'GREY' : '\033[90m',
    'DEFAULT' : '\033[99m'
}



def main():
    opts = vars(parse_args())
    region = None
    config = ConfigParser.ConfigParser()
    config.read(setup_config())

    profile = opts['profile']
    filters = opts['filter']
    aws_key = config.get( profile, 'key')
    aws_secret = config.get( profile, 'secret')

    regions = [].append( region and boto.ec2.get_region(region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret))
    regions = map( lambda s: boto.ec2.get_region(s, aws_access_key_id=aws_key, aws_secret_access_key = aws_secret), aws_regs) if not regions else regions

    for r in regions:
        try :
            conn = boto.ec2.connection.EC2Connection(aws_key, aws_secret, region=r)
            instances = get_ec2_instances(conn, filters)
        except Exception as e :
            print "Error %s" % e.message
            pass
    print colors["GREEN"], "\n", tbl, colors["END"]



def get_ec2_instances(conn, filter):
    """
    Connects to EC2, returns a connection object
    """
    reservations = conn.get_all_instances()
    for reservation in reservations:
        for i in reservation.instances:
            if filter in ""+optional([i.tags['Name'] if i.tags.has_key('Name') else '',i.id,i.public_dns_name,i.ip_address,i.instance_type,i.placement,i.private_ip_address,i.vpc_id,i.launch_time,i.state]):
                tbl.add_row([i.tags['Name'] if i.tags.has_key('Name') else '',i.id,i.public_dns_name,i.ip_address,i.instance_type,i.placement,i.private_ip_address,i.vpc_id,i.launch_time,i.state])


def optional(a):
    if not a:
        return ''
    return str(a)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', type=str,
                       default='Default', help='Configuration profile')
    parser.add_argument('-f','--filter', type=str, default='',
                        help=('Amazon EC2 API filter to limit the result returned. '
                              '(Example: --filter running)'))
    return parser.parse_args()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        pass

