import boto3


region = "eu-west-1"
ec2 = boto3.resource("ec2", region_name=region)

available_volumes = ec2.volumes.filter(
    Filters=[{'Name': 'status', 'Values': ['available']}]
)

for volume in available_volumes:
    if not volume.attachments:
        print "Volume {} ({} GB) isn't attached to anything".format(volume.id, volume.size)
        volume.delete()
        print "Volume {} deleted".format(volume.id)
