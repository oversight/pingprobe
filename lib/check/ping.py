from icmplib import async_ping
from libprobe.asset import Asset
from ..utils import check_config


DEFAULT_PING_COUNT = 5  # (1 - 9)
DEFAULT_PING_INTERVAL = 1  # (1s - 9s)
DEFAULT_PING_TIMEOUT = 10
TYPE_NAME = 'icmp'
ITEM_NAME = 'ping'


def get_item(itm):
    max_time = None
    min_time = None

    if itm.is_alive:
        max_time = itm.max_rtt / 1000  # float (s)
        min_time = itm.min_rtt / 1000  # float (s)

    return {
        'droppedCount': itm.packets_sent - itm.packets_received,  # int
        'successCount': itm.packets_received,  # int
        'maxTime': max_time,  # float (s) or None
        'minTime': min_time,  # float(s) or None
    }


def get_state(data):
    state = {
        TYPE_NAME: {
            ITEM_NAME: get_item(data)
        }
    }
    return state


async def check_ping(asset: Asset, asset_config: dict, check_config: dict):
    address = check_config.get('address')
    if not address:
        address = asset.name
    count = check_config.get('count', DEFAULT_PING_COUNT)
    interval = check_config.get('interval', DEFAULT_PING_INTERVAL)
    timeout = check_config.get('timeout', DEFAULT_PING_TIMEOUT)
    check_config(ping_count, ping_interval)

    logging.debug(
        f"ping {address}; "
        f"count: {count} interval: {interval} timeout: {timeout}; {asset}")

    try:
        data = await async_ping(
            address,
            count=count,
            interval=interval,
            timeout=timeout,
        )
    except Exception as e:
        error_msg = str(e) or type(e).__name__
        raise CheckError(f"ping failed: {error_msg}")

    return get_state(data)
