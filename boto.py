import boto3
import botocore

s3 = boto3.resource('s3')
object = s3.Object('arm-odoo-hd-storage-preprod', 'test.txt')
object.put(Body=b'test')