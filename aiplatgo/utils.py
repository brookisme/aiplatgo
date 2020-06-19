import os
import re
from pathlib import Path
import yaml
#
# CONSTANTS
#
FETCH_CMD="gsutil -m cp -r gs://{}/{} {}"
LS_CMD="gsutil ls gs://{}/{} "


#
# I/O
#
def read_yaml(path,*key_path):
    """ read yaml file
    path<str>: path to yaml file
    *key_path: keys to go to in object
    """    
    with open(path,'rb') as file:
        obj=yaml.safe_load(file)
    for k in key_path:
        obj=obj[k]
    return obj


def gs_fetch(
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


#
# HELPERS
#
def to_dash(value):
    return re.sub('_','-',value)


def to_underscore(value):
    return re.sub('-','_',value)    


#
# UTILS
#
def _prepare_destination(dest,path):
    if re.search('/',path):
        p=Path(f'{dest}/{path}')
        dest=p.parent
        Path(dest).mkdir(parents=True, exist_ok=True)
    return dest



