import argparse
import json
import os
import re
from tempfile import TemporaryFile, NamedTemporaryFile
import pandas as pd

import socket
import time
import boto3
from tqdm import tqdm
from warcio import ArchiveIterator

import datetime
from botocore import UNSIGNED
from botocore.config import Config
from utils import parse_record, get_timestamp

# NOTE: You might have to put in your credentials here, like
# s3client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
# s3client = boto3.client('s3', config=Config(signature_version=UNSIGNED))


file_key = '../aws_key.csv'
# Looks for credentials in local file
if os.path.exists(file_key):
    keys = pd.read_csv(file_key)
    AWS_ACCESS_KEY = keys['Access key ID'][0]
    AWS_SECRET_KEY = keys['Secret access key'][0]
# Looks for credentials as environment variables (recommended)
else:
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

s3client = boto3.client('s3', 
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY)
# python real_news.py --path crawl-data/CC-NEWS/2020/10/CC-NEWS-20201015140400-00177.warc.gz

def make_response(outcome, dt0, dt1, job_type, payload):
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name) 
    dt0 = get_timestamp(dt0)
    dt1 = get_timestamp(dt1)
    out = {
        'started': dt0,
        'finished': dt1,
        'outcome': outcome,
        'job_type': job_type,
        'payload': payload,
        'host_name': host_name,
        'host_ip': host_ip
    }
    file_path = f'logs/job_{job_type}_{dt1}.txt'
    with open(file_path, 'w') as f:
        json.dump(out,f)
    return file_path

def parse_news_file(args, output_path):
    archive_date = args.path.split('/')[1]
    rest = '_'.join(args.path.split('/')[2:])
    allow_all = args.allow_all
    if allow_all == False:
        allow_all = None
    print('Allow all',allow_all==True)

    out_prefix = 'propaganda-' if args.propaganda else ''
    out_key = '{}{}/{}.jsonl'.format(out_prefix, archive_date, rest)

    with TemporaryFile(mode='w+b', dir=output_path) as warctemp:
        s3client.download_fileobj('commoncrawl', args.path, warctemp)
        warctemp.seek(0)

        with NamedTemporaryFile(mode='w', dir=output_path) as f:
            for record in tqdm(ArchiveIterator(warctemp, no_record_parse=False)):
                for parsed_record in parse_record(record, propaganda=args.propaganda, allow_all=allow_all):
                    f.write(json.dumps(parsed_record) + '\n')

            s3client.upload_file(f.name, args.bucket_name, out_key)

        print("I guess I'm done now")
    return rest

def main(args): 
    dt0 = datetime.datetime.now() 

    try:    
        if args.job_type == 'TEST':
            time.sleep(2)
            payload = 'TEST'
        elif args.job_type == 'CC_NEWS':
            output_path = './'
            print('started',dt0)
            payload = parse_news_file(args, output_path)

        dt1 = datetime.datetime.now()
        print('done',dt1)
        outcome = 'Success'
    except:
        outcome = 'Failed'
        dt1 = datetime.datetime.now()
    
    file_name = make_response(outcome, dt0, dt1, job_type = args.job_type, payload = payload)
    s3client.upload_file(file_name, args.bucket_name, file_name)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Collects and parses a news file')
    parser.add_argument('--path', 
                        type=str,
                        help='file name, example crawl-data/CC-NEWS/2020/10/CC-NEWS-20201015070535-00171.warc.gz')
    parser.add_argument('--bucket_name', 
                        type=str,
                        default = 'real-news',
                        help='out path')
    parser.add_argument('--propaganda', 
                        action='store_true',
                        help='Download some propaganda instead of real news')
    parser.add_argument('--job_type', 
                        type=str,
                        default = 'CC-NEWS',
                        help='Takes CC-NEWS or TEST, defaults to TEST')
    parser.add_argument('--allow_all', 
                        type=bool,
                        default = True,
                        help='Whether to allow all news sources or limit to the Google top 5000 sources, default True')
    args = parser.parse_args()

    # default='crawl-data/CC-MAIN-2017-13/segments/1490218186353.38/warc/CC-MAIN-20170322212946-00000-ip-10-233-31-227.ec2.internal.warc.gz',
    # 
    # aws s3 ls s3://commoncrawl/crawl-data/CC-MAIN-2020-05/segments/1579250589560.16/ --no-sign-request
    # aws s3 ls s3://commoncrawl/crawl-data/CC-NEWS/2020/10/CC-NEWS-20201015* --no-sign-request
    main(args)
