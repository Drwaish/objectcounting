""" Load model for processingg"""
from ultralytics import YOLO


def load_model():
    '''
    Download model and send for processing.

    Parameters
    ----------
    None

    Return
    ------
    model
    '''
    model = YOLO('yolov8s.pt')
    return model
