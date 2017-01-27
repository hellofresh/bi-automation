"""
    Moves data from one server to another.
"""
import uuid
import os

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
        '--target-path', dest='target_path', required=True,
        help='Define where to transfer that data'
    )

    arg_parser.add_argument(
        '--target-server', dest='target_server', required=True,
        help='Define from which server we need to put the data'
    )

    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_input_arguments()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    task_id = uuid.uuid1()

    print "Task ID: {}".format(str(task_id))
    print "From: {}".format(args.origin_server)
    print "Copy: {}".format(args.origin_path)
    print "To: {}".format(args.target_server)
    print "Path: {}".format(args.target_path)

    print '\nRead the above input and confirm typing "yes"'
    choice = raw_input().lower()

    if choice not in ['yes']:
        raise Exception("STOOOOOP IT!!!")

    origin_server = servers.from_conf(args.origin_server)
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

    os.system(
        "scp -rp {}:{}/. {}/.".format(
            args.origin_server, transfer_path, local_dir)
    )

    # I have the data in my local
    # create target local user dir
    target_server = servers.from_conf(args.target_server)
    create_data_dir = 'mkdir -p {}'.format(transfer_path)
    target_server.run(create_data_dir)

    os.system(
        "scp -r {}/. {}:{}/.".format(
            local_dir, args.target_server, transfer_path
        )
    )

    # we have the content, yay, now move it to final dir.
    copy_content_final_dest = "cd {} && sudo mv -rp . {}".format(
        transfer_path, args.target_path
    )

    target_server.run(copy_content_final_dest)
