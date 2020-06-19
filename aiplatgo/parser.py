import re
from . import utils
from pprint import pprint

class Parser(object):

    @staticmethod
    def cli_args(args):
        return {  _key(args[i]): _value(args[i+1]) 
                  for i in range(0,len(args),2) }


    def __init__(self,args_config,config=None,config_list=None):
        if isinstance(args_config,str):
            args_config=utils.read_yaml(args_config)
        self.args_config=args_config
        if config_list:
            config=Parser.cli_args(config_list)
        self.config=config



    def args(self,args_key,config=None):
        config=config or self.config
        _args={}
        
        for k in self.args_config.get(args_key):
            k,v=self._get_key_value(config,k)
            _args[k]=v
        return _args


    #
    # INTERNAL
    #
    def _get_key_value(self,config,key):
        if isinstance(key,str):
            try:
                return key, config[key]
            except:
                print('key',key)
                pprint(config)
                print('\n'*10)
                raise
        else:
            default=list(key.values())[0]
            key=list(key.keys())[0]
            return key, config.get(key,default)






#
# INTERNAL
#
def _key(key):
    key=re.sub('^--','',key)
    return utils.to_underscore(key)


def _value(value):
    try:
        _v=str(value).lower()
        if _v=='true':
            value=True
        elif _v=='false':
            value=False
        elif _v in ['none','null']:
            value=None
        elif _is_list_str(value):
            value=value.split(',')
        else:
            value=float(value)
            if (value==value//1): 
                value=int(value)
    except:
        pass
    return value


def _is_list_str(value):
    if (',' in value) and (' ' not in value):
        return True
    else:
        return False