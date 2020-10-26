import os
import re
from pathlib import Path
import pandas as pd
import mproc
import gcs_helpers.fetch as gfetch
#
# CONSTANTS
#
FETCH_CMD="gsutil -m cp -r {} {}"
LS_CMD="gsutil ls {}"
GS='gs://'
MAX_PROCESSES=64


#
# PUBLIC
#
def download_from_storage(
        dest=None,
        srcs=None,
        uri=None,
        bucket=None,
        folder=None,
        dry_run=False ):
    if dest:
        dest=_prepare_destination(dest)
    else:
        raise ValueError('aiplatgo.gcs: `dest` kwarg must be provided')
    if not uri:
        uri="/".join([p for p in ['gs:/',bucket,folder] if p])
    if isinstance(srcs,str):
        srcs=[srcs]
    dests=[]
    if srcs:
        for s in srcs:
            _dest=_prepare_destination(dest)
            _uri=f'{uri}/{s}'
            cmd=FETCH_CMD.format(_uri,_dest)
            print(cmd)
            if dry_run:
                print('--dry_run:')
                cmd=LS_CMD.format(_uri)
            os.system(cmd)
            dests.append(_dest)
    else:
        cmd=FETCH_CMD.format(uri,dest)
        print(cmd)
        if dry_run:
            print('--dry_run:')
            cmd=LS_CMD.format(uri)
        os.system(cmd)
    return dest, dests


def download_from_dataset(
        dataset,
        dest_root,
        bucket=None,
        keys=['path'],
        max_processes=MAX_PROCESSES,
        safe=True,
        dry_run=False):
    if isinstance(dataset,str):
        dataset=[dataset]
    if isinstance(dataset,list):
        if isinstance(dataset[0],str):
            dataset=[pd.read_csv(d) for d in dataset]
        df=pd.concat(dataset)
    else:
        df=dataset
    uris=df[keys].drop_duplicates().values.tolist()
    def _down(uris):
        return download_uris(
            uris,
            dest_root=dest_root,
            bucket=bucket,
            safe=safe,
            dry_run=dry_run)
    return mproc.map_with_threadpool(_down,uris,max_processes=max_processes)


def download_uris(uris,dest_root='.',bucket=None,safe=True,dry_run=False):
    if isinstance(uris,str):
        uris=[uris]
    return [download_uri(u,dest_root,bucket=bucket,safe=safe,dry_run=dry_run) for u in uris]


def download_uri(uri,dest_root='.',bucket=None,safe=True,dry_run=False):
    path=re.sub(f'^{GS}','',uri)
    if bucket:
        path=re.sub(f'{bucket}/','',path)
        uri=f'{GS}{bucket}/{path}'
    else:
        path="/".join(path.split('/')[1:])
    dest=Path(f'{dest_root}/{path}')
    if dry_run or (safe and dest.is_file()):
        return dest
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        return gfetch.blob(path=uri,dest=str(dest))



#
# INTERNAL
#
def _prepare_destination(*args):
    dest='/'.join([a for a in args if a])
    path=Path(dest)
    if '.' in path.name:
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        path.mkdir(parents=True, exist_ok=True)
    return dest

