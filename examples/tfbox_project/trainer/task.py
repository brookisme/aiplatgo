import os
from datetime import datetime
from pprint import pprint
import click
from aiplatgo.parser import Parser
_trainer_dir=os.path.dirname(os.path.realpath(__file__))


#
# CONSTANTS
#
TS_FMT='%H:%M:%S (%Y-%m-%d)'
ARGS_CONFIG_PATH=f'{_trainer_dir}/args_config.yaml'
ARG_KWARGS_SETTINGS={
    'ignore_unknown_options': True,
    'allow_extra_args': True
}


#
# PUBLIC
#
def setup(date_time,setup_arg_1,setup_arg_2,setup_arg_3):
    print('start_time:',date_time.strftime(TS_FMT))
    return 'todo'


def load_datasets(datasets_arg_1,arg_with_default_2):
    return 'todo:train_df', 'todo:valid_df'


def fetch_data(*args,*kwargs):
    return 'todo'


def dataloader(training_arg_1,training_arg_2,validation_arg_1):
    data=interface.loader(training_arg_1,training_arg_2)
    vdata=interface.loader(validation_arg_1)
    return  data, vdata


def training_objects(
        loss_func,
        optimizer,
        learning_rate,
        metrics):
    loss=interface.callbacks(loss_func)
    optimizer=interface.optimizer(optimizer)
    metrics=interface.metrics(metrics)
    return loss, optimizer, metrics


def get_callbacks(
        monitor,
        tensorboard_folder,
        patience)
    return interface.callbacks(monitor,tensorboard_folder,patience)


def build_model(
        optimizer,
        loss,
        metrics,
        model_name,
        model_key_path,
        model_config_dir):
    model=interface.model(
        model_name,
        model_key_path,
        model_config_dir)
    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics)
    return model


def train(
    work_dir,
    data,
    vdata,
    dry_run,
    saved_model_folder
    nb_epochs
    print_model):
    if dry_run:
        model.summary()
    else:
        if print_model:
            model.summary()
        model.fit(
            data,
            validation_data=vdata,
            epochs=nb_epochs,
            callbacks=callbacks)
        if saved_model_folder:
            model_path=f'{work_dir}/{saved_model_folder}'
            model.save(model_path) 
        else:
            model_path=None
        return model_path



def complete(work_dir,**kwargs):
    print('post processing and cleanup:')
    pprint(kwargs)


#
# CLI
#
@click.command(context_settings=ARG_KWARGS_SETTINGS)
@click.pass_context
def run(ctx):
    parser=Parser(ARGS_CONFIG_PATH,config_list=ctx.args)
    # setup
    dtime=datetime.now()
    work_dir=setup(dtime,**parser.args('setup'))
    # data
    train_df, valid_df=load_datasets(**parser.args('load_datasets'))
    fetch_data(train_df, valid_df,**parser.args('fetch_data'))
    data, vdata=dataloader(train_df,valid_df,**parser.args('dataloader'))
    # model/training
    loss, optimizer, metrics=training_objects(
        not_water_water_ratio,
        **parser.args('training_objects'))
    model=build_model(
        optimizer,
        loss,
        metrics,
        **parser.args('build_model'))
    callbacks=get_callbacks(
        work_dir,
        **parser.args('get_callbacks'))
    model_path=train(
        work_dir,
        data,
        vdata,
        model,
        callbacks,
        **parser.args('train'))
    # post process
    complete(
        work_dir=work_dir,
        config=parser.config,
        time_stamp=dtime.strftime(TS_FMT),
        model_path=model_path,
        **parser.args('complete'))


if __name__ == '__main__':
    run()

