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
LOCAL_HELP='local run'
TRAIN_HELP='train on platform'
DEV_HELP='dev run'
IS_DEV=False
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


@click.command(
    help=LOCAL_HELP,
    context_settings=ARG_KWARGS_SETTINGS ) 
@click.argument('verb',type=str)
@click.argument('config',type=str,required=False)
@click.option(
    '--dev',
    help=DEV_HELP,
    default=IS_DEV,
    type=bool)
@click.pass_context
def local(ctx,verb,config='.',dev=IS_DEV):
    print('config file:',config)
    args, config = _process_args(ctx,config)
    print('args:',args)
    pprint(config)
    cmd=command.local(
            verb,
            *args,
            **config)
    print('-'*50)
    print(cmd)



@click.command(
    help=TRAIN_HELP,
    context_settings=ARG_KWARGS_SETTINGS ) 
@click.argument('name',type=str)
@click.argument('config',type=str,required=False)
@click.option(
    '--dev',
    help=DEV_HELP,
    default=IS_DEV,
    type=bool)
@click.pass_context
def train(ctx,name='.',config='.',dev=IS_DEV):
    print('config file:',config)
    args, config = _process_args(ctx,config)
    print('args:',args)
    pprint(config)
    if name in SKIPS:
        name=config['config']['name']
    cmd=command.train(
            name,
            *args,
            **config)
    print('-'*50)
    print(cmd)


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
    config=_get_config(config)
    if kwargs:
        config['config']=config.get('config',{})
        config['args']=config.get('args',{})
        config['user']=config.get('user',{})
        for k,v in kwargs.items():
            d,k=_key_path(k)
            config[d][k]=v
    return args, config


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