from .base import Base
from icmplib import async_ping


class CheckPing(Base):

    required = True
    type_name = 'icmp'

    @staticmethod
    async def run_check(address, count, interval, timeout):
        return await async_ping(
            address,
            count=count,
            interval=interval,
            timeout=timeout,
        )

    @staticmethod
    def on_item(itm):
        max_time = None
        min_time = None

        if itm.is_alive:
            max_time = itm.max_rtt / 1000  # float (s)
            min_time = itm.min_rtt / 1000  # float (s)

        return {
            'droppedCount': itm.packets_sent - itm.packets_received,  # int
            'successCount': itm.packets_received,  # int
            'name': 'ping',  # unicode
            'maxTime': max_time,
            'minTime': min_time
        }
