""" your_model_project.interface

DESCRIPTION: 

    * define methods here to pass your models/loss-functions/etc to `trainer.task`


EXAMPLE_IMPORTS/CONSTANTS:

import os
from pathlib import Path
import tensorflow as tf
from tfbox.loaders import ...
from tfbox.nn.MODEL_MODULE import ...
import tfbox.losses
import tfbox.callbacks
_module_dir=os.path.dirname(os.path.realpath(__file__))



#
# CONSTANTS
#
MODEL_CONFIG_DIR=f'{_module_dir}/nn/configs'
DEFAULT_OPTIMIZER='adam'
OPTIMIZERS={
    'adam': tf.keras.optimizers.Adam
}
"""



#
# LOSS
#
def loss(*args,*kwargs):
    """ example:
    if weights:
        weights=[float(w) for w in weights]
    out=tfbox.losses.get(
        loss_func,
        weights,
        **kwargs)
    """
    _loss='todo:get_loss'
    return out



#
# OPTIMIZER
#
def optimizer(*args,*kwargs):
    """ example:
    if not optimizer:
        optimizer=DEFAULT_OPTIMIZER
    if isinstance(optimizer,str):
        optimizer=OPTIMIZERS.get(optimizer,optimizer)
    if not isinstance(optimizer,str):
        print('OPTIMIZER:',optimizer,kwargs)
        optimizer=optimizer(**kwargs)
    """
    _optimizer='todo:get_model'
    return _optimizer



#
# DATALOADER
#
def loader(*args,*kwargs):
    _loader='todo:_loader'
    return _loader



#
# METRICS
#
def metrics(*args,*kwargs):
    metrics_list='todo:get_metrics'
    return metrics_list



#
#  CALLBACKS
#
def callbacks(*args,*kwargs):
    _callbacks='todo:get_callbacks'
    return _callbacks



#
# MODEL
#
def model(*args,*kwargs):
    _model='todo:get_model'
    return _model






