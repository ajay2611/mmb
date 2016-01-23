__author__ = 'naveen'
import os

from config.settings.common import MEDIA_ROOT


def handle_uploaded_file(f, pk):
    """
    uploading file to a specific folder based on user
    :param f: mp3 file
    :param pk: user primary key
    :return:
    """
    pk = unicode(pk)
    folder = pk
    audio = "audio"
    try:
        os.mkdir(os.path.join(MEDIA_ROOT, audio))
        os.mkdir(os.path.join(MEDIA_ROOT, audio, folder))
    except:
        pass

    name_list = os.path.splitext(f.name)
    ext = name_list[-1]
    name = name_list[0]
    full_path = os.path.join(MEDIA_ROOT, audio, folder)

    destination = open('{0}/{1}{2}'.format(full_path, name, ext), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
