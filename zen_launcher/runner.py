import os
import re
import sys


BASE_DIR = os.path.expanduser('~/.antelope/zen/panel')
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)


def get_panel_dir(ver, create=True):
    stripped = ver.strip()
    if re.match(r'\d+(\.\d+)*', stripped) is not None:
        d = os.path.join(BASE_DIR, stripped)
        if create and not os.path.exists(d):
            os.makedirs(d)
        return d


def sort_vers(vers):
    """Return versions sorted in descending order.  Format is expected to be
    consistent.  For example passing ['1.10.1', '1.11'] (Note that
    '1.10.1' has a micro version number and '1.11' doesn't.) will yield
    incorrect results.

    """
    key = lambda v: int(v.replace('.', ''))
    return list(sorted(vers, key=key, reverse=True))


def get_latest_panel_version():
    """Returns None in case of no panels installed.

    """
    vers = os.listdir(BASE_DIR)
    srt = sort_vers(vers)
    if srt:
        return srt[0]


def get_latest_panel_dir():
    """Returns None in case of no panels installed.

    """
    latest = get_latest_panel_version()
    if latest is not None:
        return os.path.join(BASE_DIR, latest)
    return None


def run_version(ver):
    d = get_panel_dir(ver, create=False)
    if not os.path.exists(d):
        raise ValueError
    if sys.platform.startswith('win'):
        # START FOR WINDOWS
        print('Starting {} for Windows'.format(d))
    elif sys.platform.startswith('darwin'):
        print('Starting {} for Darwin'.format(d))
    else:
        print('Starting {} for GNU'.format(d))
