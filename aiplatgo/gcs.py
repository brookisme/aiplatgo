import os
import re
from pathlib import Path
import pandas as pd
import mproc
import gcs_helpers.fetch as gfetch
#
# CONSTANTS
#
FETCH_CMD="gsutil -m cp -r gs://{}/{} {}"
LS_CMD="gsutil ls gs://{}/{} "
GS_RGX='^gs://'
MAX_PROCESSES=64


#
# PUBLIC
#
def download_from_storage(
        bucket,
        folders,
        dest,
        folder_path=None,
        dry_run=False ):
    path=bucket
    if isinstance(folders,str):
        folders=[folders]
    if folder_path: 
        path=f'{path}/{folder_path}'
    for f in folders:
        dest=_prepare_destination(dest,f)
        cmd=FETCH_CMD.format(path,f,dest)
        print(cmd)
        if dry_run:
            print('--dry_run:')
            cmd=LS_CMD.format(path,f)
        os.system(cmd)


def download_from_dataset(
        dataset,
        dest_root,
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
    uris=df[keys].values.tolist()
    def _down(uris):
        return download_uris(
            uris,
            dest_root=dest_root,
            safe=safe,
            dry_run=dry_run)
    return mproc.map_with_threadpool(_down,uris,max_processes=max_processes)


def download_uris(uris,dest_root='.',safe=True,dry_run=False):
    if isinstance(uris,str):
        uris=[uris]
    return [download_uri(u,dest_root,safe=safe,dry_run=dry_run) for u in uris]


def download_uri(uri,dest_root='.',safe=True,dry_run=False):
    path=re.sub(GS_RGX,"",uri)
    path="/".join(path.split('/')[1:])
    dest=f'{dest_root}/{path}'
    if dry_run or (safe and os.path.isfile(dest)):
        return dest
    else:
        Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
        return gfetch.blob(path=uri,dest=dest)



#
# INTERNAL
#
def _prepare_destination(dest,path):
    if re.search('/',path):
        p=Path(f'{dest}/{path}')
        dest=p.parent
        Path(dest).mkdir(parents=True, exist_ok=True)
    return dest