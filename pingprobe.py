import asyncio
from libprobe.probe import Probe
from lib.check.ping import check_ping
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'checkPing': check_ping
    }

    probe = Probe("pingProbe", version, checks)

    asyncio.run(probe.start())
