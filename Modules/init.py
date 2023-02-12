#    _____  _   _  _____  _______ 
#   |_   _|| \ | ||_   _||__   __|
#     | |  |  \| |  | |     | |   
#     | |  | . ` |  | |     | |   
#    _| |_ | |\  | _| |_    | |   
#   |_____||_| \_||_____|   |_|   
# 
#   ---------------------------------------
#   Fonctions d'initialisation des notebooks
#

import datetime
import glob
import platform
import shutil
import Modules.config as config
import os
import sys
from IPython.display import display, Markdown


def init(name=None, run_directory='./run'):
    global notebook_id
    global datasets_dir
    global run_dir

    notebook_id = config.DEFAULT_NAME if name is None else name

    run_dir = run_directory

    datasets_dir = config.DATA_PATH

    if datasets_dir is False:
        print("Impossible de trouver les datasets !\nVeuillez vérifier le chemin.")

    datasets_dir = os.path.expanduser(datasets_dir)

    if not os.path.exists(run_dir):
        os.mkdir(run_dir)

    updated = update_keras_cache()

    log_level = int(os.getenv('TF_CPP_MIN_LOG_LEVEL', 0))
    str_level = ['Info + Warning + Error',
                 'Warning + Error', 'Error only'][log_level]

    _start_time = datetime.datetime.now()
    h = platform.uname()

    title = '<br>**Projet M1 - Détection d\'anomalies sur imagerie médicale - ' + name + '**'
    display(Markdown(title))
    print('Version              :', config.VERSION)
    print('Notebook id          :', notebook_id)
    print('Run time             :', _start_time.strftime("%A %d %B %Y, %H:%M:%S"))
    print('Hostname             :', f'{h[1]} ({h[0]})')
    print('Tensorflow log level :', str_level, f' (={log_level})')
    print('Datasets dir         :', datasets_dir)
    print('Run dir              :', run_dir)
    print('Update keras cache   :', updated)

    for m in config.MODULES:
        if m in sys.modules:
            print(f'{m:21s}:', sys.modules[m].__version__)

    return datasets_dir


def update_keras_cache():
    updated = False
    if os.path.isdir(f'{datasets_dir}/keras_cache'):
        from_dir = f'{datasets_dir}/keras_cache/*.*'
        to_dir = os.path.expanduser('~/.keras/datasets')
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)
        for pathname in glob.glob(from_dir):
            filename = os.path.basename(pathname)
            destname = f'{to_dir}/{filename}'
            if not os.path.isfile(destname):
                shutil.copy(pathname, destname)
                updated = True
    return updated
