"""Run a synthetic-data walkthrough against a running local API."""
import argparse
import json
from pathlib import Path
import httpx

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8103')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
client = httpx.Client(base_url=args.url, timeout=300)

def call(method, path, **kwargs):
    response = client.request(method, path, **kwargs)
    response.raise_for_status()
    return response.json()

brief = call('POST','/research',json={'question':'Retrieval-augmented generation','max_sources':1})
print(json.dumps(brief,indent=2))
print('Markdown export:',args.url+'/research/'+brief['id']+'/export')
