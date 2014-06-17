#!/usr/bin/env python

import threading
import time

from zen_launcher import app
from zen_launcher import update
from zen_launcher import download
from zen_launcher import runner


# XXX y: Translate?
TEXT_CHECKING = 'Checking for new updates'
TEXT_NO_CONNECTION = 'Please check your Internet connection and try again'
TEXT_DOWNLOADING_FMT = 'Downloading control panel v{}'
TEXT_INSTALLING = 'Installing update'
TEXT_LAUNCHING_FMT = 'Launching control panel v{}'

window = None


def animate_progress(duration):
    window.set_progress(0)
    for i in range(11):
        window.set_progress(10 * i)
        time.sleep(duration / 10)


def get_archive_type(url):
    if url.endswith('.tar.bz'):
        return 'tar.bz'
    elif url.endswith('.tar.gz'):
        return 'tar.gz'
    elif url.endswith('.zip'):
        return 'zip'
    raise ValueError


def run_latest():
    ver = runner.get_latest_panel_version()
    if not ver:
        window.set_text(TEXT_NO_CONNECTION, color='red')
    else:
        window.set_text(TEXT_LAUNCHING_FMT.format(ver))
        # animate_progress(0.5)
        time.sleep(0.5)

        app.destroy()
        runner.run_version(ver)


def install(updates):
    # 1. Download
    latest = updates[0]
    url = latest['url']
    window.set_text(TEXT_DOWNLOADING_FMT.format(latest['version']))
    window.set_progress(0)
    f = download.tempdownload(latest['url'], window.set_progress)

    # 2. Extract
    window.set_text(TEXT_INSTALLING)
    window.set_progress(100)
    archive_type = get_archive_type(url)
    newdir = runner.get_panel_dir(latest['version'])

    # Fucking Windows doesn't allow by default multiple processes to
    # work with one and the same file, so we need to f.seek to 0 and
    # work with this object as readable file to extract contents from.
    f.seek(0)
    download.extract(f, newdir, archive_type)

    # 3. Clean up and run
    latest = runner.get_latest_panel_dir()
    assert newdir == latest, 'newdir={}, latest={}'.format(newdir, latest)
    f.close()
    run_latest()


def background():
    window.set_text(TEXT_CHECKING)
    # We're nice, so we give the user some time to read the message ;)
    animate_progress(0.5)

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
