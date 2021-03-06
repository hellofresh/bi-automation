"""
    Moves data from one server to another.
"""
import uuid
import os
import shutil

from argparse import ArgumentParser

from sshed import servers


def parse_input_arguments():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        '--origin-server', dest='origin_server', required=True,
        help='Define from which server we need to take the data'
    )

    arg_parser.add_argument(
        '--origin-path', dest='origin_path', required=True,
        help='Define from where we need to take the data'
    )

    arg_parser.add_argument(
        '--target-path', dest='target_path', required=False,
        help='Define where to transfer that data'
    )

    arg_parser.add_argument(
        '--target-server', dest='target_server', required=False,
        help='Define from which server we need to put the data'
    )

    arg_parser.add_argument(
        '--username', dest='username', required=False,
        help='Define a different username', default=None
    )

    arg_parser.add_argument(
        '--only-local', dest='only_local', required=False,
        default=False, help='True if it should only download to your local'
    )

    return arg_parser.parse_args()


def create_server(host, username=None):
    if not username:
        return servers.from_conf(host)

    return servers.Server(host, username)


if __name__ == '__main__':
    args = parse_input_arguments()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    task_id = uuid.uuid1()

    print "Task ID: {}".format(str(task_id))
    if args.username:
        print "Username: {}".format(args.username)
    print "From: {}".format(args.origin_server)
    print "Copy: {}".format(args.origin_path)

    if args.only_local:
        print "Stored in local only"
    else:
        print "To: {}".format(args.target_server)
        print "Path: {}".format(args.target_path)

    print '\nRead the above input and confirm typing "yes"'
    choice = raw_input().lower()

    if choice not in ['yes']:
        raise Exception("STOOOOOP IT!!!")

    origin_server = create_server(args.origin_server, args.username)
    transfer_path = "~/.transfer/{}".format(task_id)

    create_data_dir = 'mkdir -p {}'.format(transfer_path)

    origin_server.run(create_data_dir)

    copy_data = 'cd {} && cp -r {} .'.format(transfer_path, args.origin_path)

    origin_server.run(copy_data)

    # create local dir
    local_dir = os.path.join(
        dir_path, 'transfered_data', str(task_id)
    )

    os.makedirs(local_dir)

    with_username = ""
    if args.username:
        with_username = "{}@".format(args.username)

    print "Pulling data"
    os.system(
        "scp -rp {}{}:{}/. {}".format(
            with_username, args.origin_server, transfer_path, local_dir)
    )

    if args.only_local:
        print "Done! data located {}".format(local_dir)
        exit()

    # I have the data in my local
    # create target local user dir
    target_server = create_server(args.target_server, args.username)
    create_data_dir = 'mkdir -p {}'.format(transfer_path)
    target_server.run(create_data_dir)

    print "Pushing data"
    os.system(
        "scp -r {}/. {}{}:{}".format(
            local_dir, with_username, args.target_server, transfer_path
        )
    )

    # we have the content, yay, now move it to final dir.
    copy_content_final_dest = "cd {} && sudo cp -rp . {}".format(
        transfer_path, args.target_path
    )

    target_server.run(copy_content_final_dest)

    # Remove data from everywhere
    print 'Remove all generated data? type "yes"'
    choice = raw_input().lower()

    if choice in ['yes']:
        remove_transfer_path = 'rm -fr {}'.format(transfer_path)
        shutil.rmtree(local_dir)
        origin_server.run(remove_transfer_path)
        target_server.run(remove_transfer_path)

