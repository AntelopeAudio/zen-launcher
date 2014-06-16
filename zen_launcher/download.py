import itertools
import os
import tarfile
import tempfile
import zipfile
from urllib import request


def tempdownload(url, on_progress=None):
    """Return a NamedTemporaryFile.  You need to close() it yourself.

    """
    f = tempfile.NamedTemporaryFile()
    try:
        resp = request.urlopen(url)
    except request.URLError:
        return
    else:
        length = int(resp.headers['Content-Length'])
        size = 128 * 1024
        for i in itertools.count(start=1):
            chunk = resp.read(size)
            if not chunk:
                break
            f.write(chunk)
            on_progress and on_progress(
                int(min(100, max(0, 100 * i * size / length)))
            )
        return f


def extract(fn, where, archive_type):
    """ARCHIVE_TYPE can either be 'zip' or 'targz'.

    """
    if not os.path.exists(where):
        os.makedirs(where)

    # print('Extracting {} to {}'.format(fn, where))
    if archive_type == 'zip':
        with zipfile.ZipFile(fn) as f:
            f.extractall(where)
    elif archive_type in ('tar.bz', 'tar.gz'):
        with tarfile.open(fn) as f:
            f.extractall(where)
    else:
        raise ValueError
