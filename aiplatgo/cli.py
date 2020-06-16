from __future__ import print_function
import os,sys
sys.path.append('..')
import re
from pprint import pprint
import click
from . import command
from . import utils


#
# CONSTANTS
#
SKIPS=['.','-','_']
YAML_EXT_RGX='.(yaml|yml)$'
SHARED_HELP=(
    '* config<optional>: yaml config. default or "." uses kwargs only  '    
    '* additional args become flags <ie> "arg_name" => "--arg_name"  ' 
    '* additional kwargs become kw-flags <ie> "arg_name=123" => "--arg_name 123"  '
)
LOCAL_HELP=(
    'run local training or prediction:  '
    '* verb: "train" or "predict"  ' )+SHARED_HELP
TRAIN_HELP=(
    'submit training job to platform:  '
    '* name<optional>: job name. '
    'default or "." to use name from yaml([config][name])  ' )+SHARED_HELP
ECHO_HELP='if true print command without executing'
ECHO=False
ARG_KWARGS_SETTINGS={
    'ignore_unknown_options': True,
    'allow_extra_args': True
}


#
# CLI INTERFACE
#
@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj={}


@click.command( help=LOCAL_HELP,context_settings=ARG_KWARGS_SETTINGS ) 
@click.argument('verb',type=str)
@click.argument('config',type=str,required=False)
@click.option('--echo',help=ECHO_HELP,default=ECHO,type=bool)
@click.pass_context
def local(ctx,verb,config='.',echo=ECHO):
    args, kwargs = _process_args(ctx,config)
    cmd=command.local(verb,*args,**kwargs)




@click.command( help=TRAIN_HELP,context_settings=ARG_KWARGS_SETTINGS ) 
@click.argument('name',type=str)
@click.argument('config',type=str,required=False)
@click.option('--echo',help=ECHO_HELP,default=ECHO,type=bool)
@click.pass_context
def train(ctx,name='.',config='.',echo=ECHO):
    args, kwargs = _process_args(ctx,config)
    if name in SKIPS:
        name=kwargs['config']['name']
    cmd=command.train(name,*args,**kwargs)


#
# HELPERS
#
def _args_kwargs(ctx_args):
    args=[]
    kwargs={}
    for a in ctx_args:
        if re.search('=',a):
            k,v=a.split('=')
            kwargs[k]=v
        else:
            args.append(a)
    return args,kwargs


def _get_config(config):
    if config in SKIPS:
        config={}
    else:
        if not re.search(YAML_EXT_RGX,config):
            config=f'{config}.yaml'
        config=utils.read_yaml(config)
    return config


def _process_args(ctx,config):
    args, kwargs=_args_kwargs(ctx.args)
    _kwargs=_get_config(config)
    if kwargs:
        _kwargs['config']=_kwargs.get('config',{})
        _kwargs['args']=_kwargs.get('args',{})
        _kwargs['user']=_kwargs.get('user',{})
        for k,v in kwargs.items():
            d,k=_key_path(k)
            _kwargs[d][k]=v
    return args, _kwargs


def _key_path(key):
    if '.' in key:
        d,k=key.split('.')
    else:
        d,k='args',key
    return d, k



#
# MAIN
#
cli.add_command(local)
cli.add_command(train)
if __name__ == "__main__":
    cli()