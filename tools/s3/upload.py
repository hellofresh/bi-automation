import boto
import os
from argparse import ArgumentParser


def parse_input_arguments():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        '--from', dest='from_', required=True,
        help='From where to pull data'
    )

    arg_parser.add_argument(
        '--to', dest='to', required=False,
        help='Where yo upload it', default=""
    )

    arg_parser.add_argument(
        '--bucket', dest='bucket', required=True,
        help='To which bucket'
    )

    arg_parser.add_argument(
        '--aws-key', dest='aws_key', required=True,
        help='Amazon key'
    )

    arg_parser.add_argument(
        '--aws-secret', dest='aws_secret', required=False,
        help='Define amazon secret', default=None
    )

    return arg_parser.parse_args()

if __name__ == '__main__':
    args = parse_input_arguments()
    AWS_ACCESS_KEY_ID = args.aws_key
    AWS_ACCESS_KEY_SECRET = args.aws_secret

    BUCKET_NAME =  args.bucket
    SOURCE_DIR = args.from_
    DEST_DIR = args.to

    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET)
    bucket = conn.get_bucket(BUCKET_NAME)

    upload_files = []

    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            fullpath = os.path.join(root, f)
            upload_files.append(fullpath)


    for filename in upload_files:
        dest_path = filename.replace(SOURCE_DIR, "")

        k = boto.s3.key.Key(bucket)
        k.key = dest_path.replace(SOURCE_DIR, "")

        k.set_contents_from_filename(filename)
