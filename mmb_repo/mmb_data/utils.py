__author__ = 'delhivery'

import os


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)