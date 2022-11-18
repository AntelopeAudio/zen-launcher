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
            try:
                chunk = resp.read(size)
            except (ConnectionAbortedError, ConnectionResetError):
                f.close()
                return None
            else:
                if not chunk:
                    break
                f.write(chunk)
                progress = int(min(100, max(0, 100 * i * size / length)))
                on_progress and on_progress(progress)

        f.seek(0)
        return f


def extract(f, where, archive_type):
    """ARCHIVE_TYPE can either be 'tar.bz', 'tar.gz' or 'zip'.

    """
    if not os.path.exists(where):
        os.makedirs(where)

    # print('Extracting {} to {}'.format(fn, where))
    if archive_type == 'zip':
        with zipfile.ZipFile(f) as zf:
            zf.extractall(where)

    elif archive_type in ('tar.bz', 'tar.gz'):
        with tarfile.open(f.name) as tf:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tf, where)

    else:
        raise ValueError
