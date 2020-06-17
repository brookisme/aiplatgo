import re
import yaml


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


#
# HELPERS
#
def parse_args(args):
    return { _key(args,i): args[i+1] for i in range(0,len(args),2) }



#
# INTERNAL
#
def _key(args,i):
    key=re.sub('^--','',args[i])
    return re.sub('-','_',key)