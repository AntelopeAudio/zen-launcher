#!/usr/bin/env python

import threading
import time

from zen_launcher import app
from zen_launcher import update
from zen_launcher import download
from zen_launcher import runner


# XXX y: Translate?
TEXT_CHECKING = 'Checking for new updates'
TEXT_DOWNLOADING_FMT = 'Downloading control panel v{}'
TEXT_INSTALLING = 'Installing update'
TEXT_LAUNCHING_FMT = 'Launching control panel v{}'

window = None


def get_archive_type(url):
    if url.endswith('.zip'):
        return 'zip'
    elif url.endswith('.tar.bz'):
        return 'tar.bz'
    raise ValueError


def run_latest():
    ver = runner.get_latest_panel_version()
    if not ver:
        raise ValueError

    window.set_text(TEXT_LAUNCHING_FMT.format(ver))
    time.sleep(0.5)

    app.destroy()
    runner.run_version(ver)


def install(updates):
    # 1. Download
    latest = updates[0]
    url = latest['url']
    window.set_text(TEXT_DOWNLOADING_FMT.format(latest['version']))
    f = download.tempdownload(latest['url'], window.set_progress)

    # 2. Extract
    window.set_text(TEXT_INSTALLING)
    archive_type = get_archive_type(url)
    newdir = runner.get_panel_dir(latest['version'])
    download.extract(f.name, newdir, archive_type)

    # 3. Clean up and run
    latest = runner.get_latest_panel_dir()
    assert newdir == latest, 'newdir={}, latest={}'.format(newdir, latest)
    f.close()
    run_latest()


def background():
    window.set_text(TEXT_CHECKING)

    # We're nice, so we give the user some time to read the message ;)
    time.sleep(0.5)

    ver = runner.get_latest_panel_version() or '1.00'
    # There's a trick: the first official version we're releasing is
    # 1.20, so we know for sure that the server will return a later
    # version, even in case we have nothing downloaded yet.  The update
    # server won't return anything if version string does not start with
    # [1-9].
    update.check_for_updates(ver, yes=install, no=run_latest)


if __name__ == '__main__':
    window = app.create_window()

    t = threading.Thread(target=background)
    t.start()

    app.run()
