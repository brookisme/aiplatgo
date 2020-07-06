import re
from . import utils
from pprint import pprint

NO_DEFALUT_VALUE='_no_default_value'

class Parser(object):


    @staticmethod
    def cli_args(args):
        return {  _key(args[i]): _value(args[i+1]) 
                  for i in range(0,len(args),2) }


    def __init__(self,args_config,config=None,config_list=None):
        if isinstance(args_config,str):
            args_config=utils.read_yaml(args_config)
        self.args_config=args_config
        self.defaults=args_config.get('defaults',{})
        if config_list:
            config=Parser.cli_args(config_list)
        self.config=config



    def args(self,args_key,config=None,defaults={}):
        config=config or self.config
        defaults=defaults or self.defaults
        _args={}
        for k in self.args_config.get(args_key,{}):
            k,v=self._get_key_value(k,config,defaults)
            _args[k]=v
        return _args


    #
    # INTERNAL
    #
    def _get_key_value(self,key,config,defaults):
        if isinstance(key,str):
            default=defaults.get(key,NO_DEFALUT_VALUE)
            if default==NO_DEFALUT_VALUE:
                value=config[key]
            else: 
                value=config.get(key,default)
        else:
            default=list(key.values())[0]
            key=list(key.keys())[0]
            value=config.get(key,default)
        return key, value






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