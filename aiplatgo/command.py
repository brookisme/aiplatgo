import os
import re
from . import utils


_package_dir=os.path.dirname(os.path.realpath(__file__))


#
# CONSTANTS
#
FLAGS_PATH=f'{_package_dir}/config/flags.yaml'
FLAGS=utils.read_yaml(FLAGS_PATH)
AI_PLAT_ROOT='gcloud ai-platform'
FLAG_PREFIX='--'
SPACE=' '
LOCAL='local'
LOCAL_VERBS=['train','predict']
TRAIN='jobs submit training'
PREDICT='jobs submit prediction'
CFIG_ALIASES={
    'staging': 'staging-bucket',
    'output': 'output-bucket',
    'output_folder': 'output-folder'
}
ALIASES={
    'staging': 'staging-bucket',
    'package': 'package-path',
    'module': 'module-name'
}
GS='gs:/'
OUTPUT_DIR='output'
KEY_DOES_NOT_EXIST='_aipgo_missing_key'
#
# PUBLIC
#
def local(verb,*args,**kwargs):
    if verb not in LOCAL_VERBS:
        raise NotImplementedError(f'<{verb}> not in {LOCAL_VERBS}')
    kwargs, flags, user_kwargs=_process_kwargs(
                                    kwargs,
                                    _excluded_flags(f'local_{verb}'),
                                    gs_prefix=False,
                                    is_local=True)
    return _build(f'{LOCAL} {verb}',args,kwargs,flags,user_kwargs)


def train(job,*args,**kwargs):
    kwargs, flags, user_kwargs=_process_kwargs(kwargs,_excluded_flags('train'))
    return _build(f'{TRAIN} {job}',args,kwargs,flags,user_kwargs)


def predict(job,*args,**kwargs):
    kwargs, flags, user_kwargs=_process_kwargs(kwargs,_excluded_flags('predict'))
    return _build(f'{PREDICT} {job}',args,kwargs,flags,user_kwargs)


#
# INTERNAL
#
def _excluded_flags(key):
    flags=FLAGS.copy()
    valid=flags.pop(key,{})
    other=[f for v in flags.values() for f in v]
    return [ f for f in other if f not in valid ]


def _build(verb,args,kwargs,flags,user_kwargs):
    cmd=f'{AI_PLAT_ROOT} {verb}'
    for arg in args:
        cmd=_cat(cmd,key=arg) 
    for k,v in kwargs.items():
        cmd=_cat(cmd,value=v,key=k)
    for flag in flags:
        cmd=_cat(cmd,key=flag) 
    if user_kwargs:
        cmd+=' -- '
        for k,v in user_kwargs.items():
            cmd=_cat(cmd,value=v,key=k)
    return cmd


def _cat(cmd,value=None,key=None,prefix=FLAG_PREFIX):
    if key:
        cmd+=SPACE
        if prefix: 
            cmd+=prefix
        cmd+=key
    if value:
        if isinstance(value,list):
            value=','.join([str(v) for v in value])
        cmd+=SPACE+str(value)
    return cmd


def _process_kwargs(kwargs,exclude=None,gs_prefix=True,is_local=False):
    flags=kwargs.get('flags',[])
    flags=[ utils.to_dash(k) for k in kwargs.get('flags',[]) if k not in exclude ]
    config=kwargs.get('config',{})
    config={ utils.to_dash(CFIG_ALIASES.get(k,k)): v for k,v in config.items() }
    version=config.get('version')
    if version: 
        version=f'v{version}'
    _kwargs=kwargs.get('args',{})
    _kwargs={ utils.to_dash(ALIASES.get(k,k)): v for k,v in _kwargs.items() }
    if exclude: 
        [ _kwargs.pop(k,None) for k in exclude ]
    if not _kwargs.get('job-dir'):
        _kwargs['job-dir']=_path(config.get('name'),version,OUTPUT_DIR)
    if gs_prefix:
        _kwargs=_gs_prefix(config,_kwargs,version)
    pass_args=kwargs.get('pass_args',[])
    for arg in pass_args:
        value=_kwargs.get(arg,KEY_DOES_NOT_EXIST)
        if value != KEY_DOES_NOT_EXIST:
            kwargs['user'][arg]=value
    kwargs['user']=kwargs.get('user',{})
    if is_local:
        kwargs['user'].update(kwargs.get('local',{}))
    else:
        kwargs['user'].update(kwargs.get('job',{}))
    return _kwargs, flags, kwargs['user']


def _gs_prefix(config,kwargs,version):
    bucket=config.get('bucket')
    staging_bucket=config.get('staging-bucket',bucket)
    output_bucket=config.get('output-bucket',bucket)
    output_folder=config.get(
        'output-folder',
        _path(config.get('name'),OUTPUT_DIR))
    kwargs['job-dir']=_gs_prefix_build(output_bucket,output_folder)
    kwargs['staging-bucket']=_gs_prefix_build(staging_bucket)
    return kwargs


def _gs_prefix_build(bucket,*parts):
    if not re.search(f'^{GS}',bucket):
        bucket=f'{GS}/{bucket}'
    return _path(*([bucket]+list(parts)))


def _path(*parts):
    parts=[ str(p) for p in parts if p ]
    return "/".join(parts)




