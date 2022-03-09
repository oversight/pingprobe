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
        maxTime = None
        minTime = None

        if itm.is_alive:
            maxTime = itm.max_rtt * 1000  # float (s)
            minTime = itm.min_rtt * 1000  # float (s)

        return {
            'droppedCount': itm.packet_loss,  # int
            'successCount': itm.packets_received,  # int
            'name': 'ping',  # unicode
            'maxTime': maxTime,
            'minTime': minTime
        }
