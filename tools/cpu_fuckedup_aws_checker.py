import boto3
import re
import colored

from distutils.version import LooseVersion
from colored import stylize
from sshed import servers


ec2 = boto3.client('ec2')
instances = ec2.describe_instances()

cant_connect = []

def get_name(tags):
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return False

parsed_instances = []

for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        parsed_instances.append(
            {
                'id': instance['InstanceId'],
                'name': get_name(instance['Tags']),
                'ip': instance['PrivateIpAddress']
            }
        )

print "Start checking for fucked ups!"

for instance in parsed_instances:
    print "Connection to {} ({})".format(instance['name'], instance['ip'])
    try:
        conn = servers.Server(instance['ip'], 'ssola', password='a')
    except Exception, e:
        print "Can't connect to this one!!"
        cant_connect.append(instance)
        continue

    distro_data = " ".join(conn.run('lsb_release -a').output)
    distro = re.findall('Distributor ID:	([a-zA-z]+)', distro_data)[0].strip()
    release = re.findall('Release:	([0-9\.]+)', distro_data)[0].strip()

    print "Running: {} Release: {}".format(distro, release)

    safe = False
    if distro == "Ubuntu":
        kernels = conn.run("dpkg -l | grep linux-image | awk  '{print $3}'").output
        for kernel in kernels:
            if LooseVersion(release) < LooseVersion('16.0'):
                if LooseVersion(kernel) >= LooseVersion('3.13.0-139.188'):
                    safe = True
                    break
            else:
                if LooseVersion(kernel) >= LooseVersion('4.4.0-109.132'):
                    safe = True
                    break
    elif distro == "CentOS":
        kernel = conn.run('uname -r').output[0]
        if LooseVersion(kernel) >= LooseVersion('3.10.0-514.26.2.el7.x86_64'):
            safe = True

    if safe:
        print stylize("IS IT SAFE! GO ON HAVE A BEER!", colored.fg("green"))
    else:
        print stylize("NOT PATCHED FOR MELTDOWN&SPECTRE", colored.fg("red"))

print "You cannot connect to {} instances".format(len(cant_connect))
print cant_connect