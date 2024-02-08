import polars as pl
import boto3
AWS_BUCKET = "dataminded-academy-capstone-resources"
AWS_PREFIX = 'raw/open_aq/'
import os

def download_jsons():
    if os.path.exists('local_jsons/data_part_60.json'):
        return
    s3 = boto3.client('s3')
    list_resp = s3.list_objects(Bucket=AWS_BUCKET, Prefix=AWS_PREFIX)
    for c in list_resp['Contents']:
        filename = c['Key']
        print(f"Downloading {AWS_BUCKET}/{filename}")
        s3.download_file(Bucket=AWS_BUCKET, Key=filename, Filename='local_jsons/'+os.path.basename(filename))

def read_into_polar():
    # Read out all json files in local_jsons and merge them into one polars dataframe
    sep_dfs = [ pl.read_json(f'local_jsons/{f}').fill_null('unknown') for f in os.listdir('local_jsons') if f.endswith('.json')]
    return pl.concat(sep_dfs, how='vertical_relaxed')


download_jsons()
df = read_into_polar()
import pdb; pdb.set_trace()

pass