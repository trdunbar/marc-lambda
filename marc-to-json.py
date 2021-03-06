from __future__ import print_function
import boto3
from pymarc import MARCReader
from pymarc import JSONWriter
import StringIO


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    filename = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket="marc-to-json", Key=filename)
    marc_file = response['Body']
    reader = MARCReader(marc_file.read())
    string = StringIO.StringIO()
    writer = JSONWriter(string)
    for record in reader:
        writer.write(record)
    writer.close(close_fh=False)
    s3.put_object(Bucket="marc-to-json", Key=filename + '.json', Body=string.getvalue())
