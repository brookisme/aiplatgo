import re
from . import utils
from pprint import pprint

NO_DEFALUT_VALUE='_no_default_value'
MISSING_KEY_ERROR=(
    '{} is not in parser.config. '
    'provide a default value other than None or '
    'use required=True to allow' )


class Parser(object):
    """ Parser for user args passed through `ai-platform (local) job`

    Args:

        - args_config<str|dict>: config or path to yaml config file with defaults and per method args
        - config_list<list>: 
            * a flat list of key/value pairs. note: this is how ai-platform passes user args
            * keys: config_list[2n]
            * values: config_list[2n+1]
        - config<dict|None>: dictionary containing arg key-values to parse (if config_list not provided)
        - boolify<bool>: if true turn true/false strings into bool True/False


    Usage:

    (using click)

    @click.pass_context
    def run(ctx):
        parser=Parser('args_config.yaml',config_list=ctx.args)
        
        train_model=parser.get('train_model',True)
        score_model=parser.get('score_model',False)
        
        ... 

        model=build_model(
            optimizer,
            loss,
            metrics,
            model_dir,
            **parser.args('build_model'))

    """
    @staticmethod
    def cli_args(args):
        return {  _key(args[i]): _value(args[i+1]) 
                  for i in range(0,len(args),2) }


    def __init__(self,args_config,config_list=None,config=None,boolify=True):
        if isinstance(args_config,str):
            args_config=utils.read_yaml(args_config)
        self.args_config=args_config
        self.defaults=args_config.get('defaults',{})
        if config_list:
            config=Parser.cli_args(config_list)
        self.config=config
        self.boolify=boolify


    def args(self,args_key,config=None,defaults={}):
        config=config or self.config
        defaults=defaults or self.defaults
        _args={}
        for k in self.args_config.get(args_key,{}):
            k,v=self._get_key_value(k,config,defaults)
            _args[k]=v
        return _args


    def get(self,key,default=None,required=False):
        value=self.config.get(key,default)
        if required and (value is None):
            raise KeyError(MISSING_KEY_ERROR.format(key))
        else:
            return self._process_value(value)


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
        return key, self._process_value(value)


    def _process_value(self,value):
        if self.boolify and isinstance(value,str):
            if value.lower()=='false':
                value=False
            elif value.lower()=='true':
                value=True
        return value





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
            value=value.split(':')
            value=[_relist(v) for v in value]
            if len(value)==1:
                value=value[0]
        else:
            value=float(value)
            if (value==value//1): 
                value=int(value)
    except:
        pass
    return value


def _relist(value):
    value=value.split(',')
    if value[-1] is '':
        value=value[:-1]
    return value


def _is_list_str(value):
    if (',' in value) and (' ' not in value):
        return True
    else:
        return False