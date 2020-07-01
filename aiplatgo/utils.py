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
def to_dash(value):
    return re.sub('_','-',value)


def to_underscore(value):
    return re.sub('-','_',value)    






