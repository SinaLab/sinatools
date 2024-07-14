import os
import sys
import logging
import importlib
import shutil
import torch
import random
import numpy as np


def logging_config(log_file=None):
    """
    Initialize custom logger
    :param log_file: str - path to log file, full path
    :return: None
    """
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        handlers.append(logging.FileHandler(log_file, "w", "utf-8"))
        print("Logging to {}".format(log_file))

    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers,
        format="%(levelname)s\t%(name)s\t%(asctime)s\t%(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S",
        force=True
    )


def load_object(name, kwargs):

    try:
        object_module, object_name = name.rsplit(".", 1)
        object_module = importlib.import_module(object_module)
        obj = getattr(object_module, object_name)
        if callable(obj): 
            fn = obj(**kwargs)
            return fn
        else:
            raise TypeError(f"{name} is not a callable object.")
    except (ImportError, ModuleNotFoundError) as e:
        print(f"Error importing module: {e}")
    except AttributeError as e:
        print(f"Attribute error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None 

def make_output_dirs(path, subdirs=[], overwrite=True):
    """
    Create root directory and any other sub-directories
    :param path: str - root directory
    :param subdirs: List[str] - list of sub-directories
    :param overwrite: boolean - to overwrite the directory or not
    :return: None
    """
    if overwrite:
        shutil.rmtree(path, ignore_errors=True)

    os.makedirs(path)

    for subdir in subdirs:
        os.makedirs(os.path.join(path, subdir))



def set_seed(seed):
    """
    Set the seed for random intialization and set
    CUDANN parameters to ensure determmihstic results across
    multiple runs with the same seed

    :param seed: int
    """
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.enabled = False
