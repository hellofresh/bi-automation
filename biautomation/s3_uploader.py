import os
import glob
import boto
import math

from datetime import datetime


class PathNotFound(Exception):
    pass


class S3Connection(object):
    def __init__(self, aws_key_id, aws_secret_key):
        self.__aws_secret_key = aws_secret_key
        self.__aws_key_id = aws_key_id

    def create(self):
        return boto.connect_s3(
            self.__aws_key_id, self.__aws_secret_key
        )


class S3Uploader(object):
    def __init__(self, s3_connexion, bucket):
        self.__bucket = bucket
        self.__s3_connexion = s3_connexion.create()
        self.__aws_bucket = None
        self.__date = datetime.now().strftime('%Y_%m_%d')

    @property
    def bucket(self):
        return self.__bucket

    def upload_by_path(self, path):
        """
        This method will upload to AWS S3 all the files given a path
        :param path:
        :return:
        """
        if not os.path.exists(path):
            raise PathNotFound(
                '{path} has not been found'.format(path=path)
            )

        for file_in_dir in glob.glob('{}/*'.format(path)):
            self.upload_file(file_in_dir)
            exit()

    def upload_file(self, path):
        if not os.path.exists(path):
            raise PathNotFound(
                '{path} has not been found'.format(path=path)
            )

        print path

        bucket = self.__get_bucket()
        file_name = os.path.join(self.__date, os.path.basename(path))

        multi_part = bucket.initiate_multipart_upload(file_name)

        source_size = os.stat(path).st_size
        bytes_per_chunk = 5000 * 1024 * 1024
        chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))

        for i in range(chunks_count):
            offset = i * bytes_per_chunk
            remaining_bytes = source_size - offset
            size_in_bytes = min([bytes_per_chunk, remaining_bytes])
            part_num = i + 1

            print "uploading part {} of {}".format(str(part_num), str(chunks_count))

            with open(path, 'r') as fp:
                fp.seek(offset)
                multi_part.upload_part_from_file(
                    fp=fp, part_num=part_num, size=size_in_bytes
                )

        if len(multi_part.get_all_parts()) == chunks_count:
            multi_part.complete_upload()
            print "Upload done"
        else:
            multi_part.cancel_upload()
            print "Upload file"

    def __get_bucket(self):
        if self.__aws_bucket:
            return self.__aws_bucket

        self.__aws_bucket = self.__s3_connexion.get_bucket(self.__bucket)

        return self.__aws_bucket

