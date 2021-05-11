from __future__ import print_function
import os
from datetime import datetime
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
    'submit training job to platform:  ' )+SHARED_HELP
PRED_HELP=(
    'submit prediction job to platform:  ' )+SHARED_HELP
NAME_HELP='by default uses `config.name` for the job name. pass --name to override'
ECHO_HELP='if true print command without executing'
ECHO=False
TS_HELP='append timestamp (YYYYMMDD_HMS) to job name'
TS=True
ARG_KWARGS_SETTINGS={
    'ignore_unknown_options': True,
    'allow_extra_args': True
}
TS_FMT='%Y%m%d_%H%M%S'
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
@click.option('--echo','-e',help=ECHO_HELP,default=ECHO,is_flag=True,type=bool)
@click.pass_context
def local(ctx,verb,config='.',echo=ECHO):
    args, kwargs = _process_args(ctx,config)
    kwargs['user']['job_name']=kwargs['user'].get(
        'job_name',
        f'local_{datetime.now().strftime(TS_FMT)}')
    cmd=command.local(verb,*args,**kwargs)
    _execute(cmd,echo,verb=verb,config=config)



@click.command( help=TRAIN_HELP,context_settings=ARG_KWARGS_SETTINGS ) 
@click.argument('config',type=str,required=False)
@click.option('--name','-n',help=NAME_HELP,default='.',is_flag=False,type=str)
@click.option('--echo','-e',help=ECHO_HELP,default=ECHO,is_flag=True,type=bool)
@click.option('--timestamp','-t',help=TS_HELP,default=TS,is_flag=True,type=bool)
@click.pass_context
def train(ctx,config='.',name='.',echo=ECHO,timestamp=TS):
    args, kwargs = _process_args(ctx,config)
    name, kwargs = _process_name(name,kwargs,timestamp)
    cmd=command.train(name,*args,**kwargs)
    _execute(cmd,echo,verb=verb,config=config)



@click.command( help=PRED_HELP,context_settings=ARG_KWARGS_SETTINGS ) 
@click.argument('config',type=str,required=False)
@click.option('--name','-n',help=NAME_HELP,default='.',is_flag=False,type=str)
@click.option('--echo','-e',help=ECHO_HELP,default=ECHO,is_flag=True,type=bool)
@click.option('--timestamp','-t',help=TS_HELP,default=TS,is_flag=True,type=bool)
@click.pass_context
def predict(ctx,config='.',name='.',echo=ECHO,timestamp=TS):
    args, kwargs = _process_args(ctx,config)
    name, kwargs = _process_name(name,kwargs,timestamp)
    cmd=command.predict(name,*args,**kwargs)
    _execute(cmd,echo,verb=verb,config=config)



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
    _kwargs['config']=_kwargs.get('config',{})
    _kwargs['args']=_kwargs.get('args',{})
    _kwargs['user']=_kwargs.get('user',{})
    if kwargs:
        for k,v in kwargs.items():
            d,k=_key_path(k)
            _kwargs[d][k]=v
    return args, _kwargs


def _process_name(name,kwargs,timestamp):
    kwargs['user']=kwargs.get('user',{})
    if name in SKIPS:
        name=kwargs['config']['name']
    kwargs['config']['name']=name
    kwargs['user']['name']=name
    if timestamp:
        timestamp=datetime.now().strftime(TS_FMT)
        name=f'{name}_{timestamp}'
    kwargs['user']['job_name']=name
    return name, kwargs


def _key_path(key):
    if '.' in key:
        d,k=key.split('.')
    else:
        d,k='args',key
    return d, k


def _execute(cmd,echo,verb=None,config=None):
    if verb:
        cmd+=f" --aip_cmd {re.sub(' ','__',verb)}"
        if config:
            cmd+=f"__{re.sub(' ','__',config)}"
    print()
    print(re.sub('--','\n\t--',cmd))
    if not echo:
        os.system(cmd)


#
# MAIN
#
cli.add_command(local)
cli.add_command(train)
cli.add_command(predict)
if __name__ == "__main__":
    cli()


