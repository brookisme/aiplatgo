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
GS='gs://'
GS_PREFIX_KEYS=[
    'staging-bucket',
    'job-dir' ]



#
# PUBLIC
#
def local(verb,*args,**kwargs):
    if verb not in LOCAL_VERBS:
        raise NotImplementedError(f'<{verb}> not in {LOCAL_VERBS}')
    verb=f'{LOCAL} {verb}'
    kwargs=_process_kwargs(kwargs,_excluded_flags(f'local_{verb}'))
    return _build(verb,*args,**kwargs)


def train(job,*args,**kwargs):
    kwargs=_process_kwargs(kwargs,_excluded_flags('train'))
    return _build(TRAIN,*args,**kwargs)



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
    args=kwargs.get('args',{})
    args.update(kwargs.get('user',{}))
    args={ ALIASES.get(k,k): v for k,v in args.items() }
    if exclude: 
        [ args.pop(k,None) for k in exclude ]
    if gs_prefix:
        for k in GS_PREFIX_KEYS:
            args=_gs_prefix(args,k)
    return args


def _gs_prefix(args,key):
    v=args.get(key)
    if v and (not re.search(f'^{GS}',v)):
        args[key]=f"{GS}{re.sub('^/','',v)}"
    return args


