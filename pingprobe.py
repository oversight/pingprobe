import asyncio
from libprobe.probe import Probe
from lib.check.ping import check_ping
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'ping': check_ping
    }

    probe = Probe("ping", version, checks)

    asyncio.run(probe.start())
