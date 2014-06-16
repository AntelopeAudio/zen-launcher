import json
import sys
from urllib import request
from zen_launcher import utils


def get_updates(ver):
    platform = 'windows' if sys.platform.startswith('win') else \
               'mac' if sys.platform.startswith('darwin') else\
               'gnu'
    platform = 'mac'
    url = 'http://my.antelopeaudio.com/api/downloads/zenstudio/control_panel/'\
          '{}/{}/'.format(platform, ver)
    try:
        resp = request.urlopen(url)
    except request.URLError as e:
        print('[Warning] {}'.format(e), file=sys.stderr)
        return []
    else:
        if resp.code == 200:
            updates = json.loads(resp.readall().decode('utf-8'))
            return [u for u in updates if utils.vercmp(u['version'], ver) > 0]
        return []


def check_for_updates(ver, yes, no):
    updates = get_updates(ver)
    if updates:
        yes(updates)
    else:
        no()
