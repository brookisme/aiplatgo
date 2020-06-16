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
    'staging_bucket': 'staging-bucket',
    'staging_folder': 'staging-folder',
    'staging': 'staging-bucket',
    'output_bucket': 'output-bucket',
    'output_folder': 'output-folder',
    'output': 'output-bucket'
}
ALIASES={
    'scale_tier': 'scale-tier',
    'package_path': 'package-path',
    'module_name': 'module-name',
    'job_dir': 'job-dir',
    'staging_bucket': 'staging-bucket',
    'staging': 'staging-bucket',
    'package': 'package-path',
    'module': 'module-name'
}
GS='gs:/'
OUTPUT_DIR='output'
STAGING_DIR='staging'

#
# PUBLIC
#
def local(verb,*args,**kwargs):
    if verb not in LOCAL_VERBS:
        raise NotImplementedError(f'<{verb}> not in {LOCAL_VERBS}')
    kwargs=_process_kwargs(kwargs,_excluded_flags(f'local_{verb}'),gs_prefix=False)
    return _build(f'{LOCAL} {verb}',*args,**kwargs)


def train(job,*args,**kwargs):
    kwargs=_process_kwargs(kwargs,_excluded_flags('train'))
    return _build(f'{TRAIN} {job}',*args,**kwargs)


def predict(job,*args,**kwargs):
    kwargs=_process_kwargs(kwargs,_excluded_flags('predict'))
    return _build(f'{PREDICT} {job}',*args,**kwargs)


#
# INTERNAL
#
def _excluded_flags(key):
    flags=FLAGS.copy()
    valid=flags.pop(key,{})
    other=[f for v in flags.values() for f in v]
    return [ f for f in other if f not in valid ]


def _build(verb,*args,**kwargs):
    cmd=f'{AI_PLAT_ROOT} {verb}'
    for arg in args:
        cmd=_cat(cmd,key=arg) 
    for k,v in kwargs.items():
        cmd=_cat(cmd,value=v,key=k)
    return  cmd


def _cat(cmd,value=None,key=None,prefix=FLAG_PREFIX):
    if key:
        cmd+=SPACE
        if prefix: 
            cmd+=prefix
        cmd+=key
    if value:
        cmd+=SPACE+str(value)
    return cmd


def _process_kwargs(kwargs,exclude=None,gs_prefix=True):
    config=kwargs.get('config',{})
    config={ CFIG_ALIASES.get(k,k): v for k,v in config.items() }
    _kwargs=kwargs.get('args',{})
    _kwargs.update(kwargs.get('user',{}))
    _kwargs={ ALIASES.get(k,k): v for k,v in _kwargs.items() }
    version=config.get('version')
    if version: 
        version=f'v{version}'
    if not _kwargs.get('job-dir'):
        _kwargs['job-dir']=_path(OUTPUT_DIR,config.get('name'),version)
    if exclude: 
        [ _kwargs.pop(k,None) for k in exclude ]
    if gs_prefix:
        _kwargs=_gs_prefix(config,_kwargs,version)
    return _kwargs


def _gs_prefix(config,kwargs,version):
    folder=config.get('folder')
    bucket=config.get('bucket')
    output_bucket=config.get('output-bucket',bucket)
    staging_bucket=config.get('staging-bucket',bucket)
    output_folder=config.get('output-folder')
    staging_folder=config.get(
        'staging-folder',
        _path(STAGING_DIR,config.get('name'),version))
    kwargs['job-dir']=_gs_prefix_build(
        kwargs,
        'job-dir',
        output_bucket,
        folder,
        output_folder )
    kwargs['staging-bucket']=_gs_prefix_build( 
        kwargs,
        'staging-bucket',
        staging_bucket,
        folder,
        staging_folder )
    return kwargs


def _gs_prefix_build(kwargs,key,*parts):
    value=kwargs.get(key)
    if not re.search(f'^{GS}',str(value)):
        value=_path(value,*([GS]+list(parts)))
    return value


def _path(value,*parts):
    parts=[p for p in parts if p]
    if value: parts.append(value)
    return "/".join(parts)




