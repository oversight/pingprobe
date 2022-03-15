import asyncio
import logging

from .utils import check_config

DEFAULT_PING_COUNT = 5  # (1 - 9)
DEFAULT_PING_INTERVAL = 1  # (1s - 9s)
DEFAULT_PING_TIMEOUT = 10


class Base:
    required = False
    type_name = None
    interval = 300  # interval is required, as it is used by agentcoreclient

    @classmethod
    async def run(cls, data, asset_config=None):
        try:
            # If asset_id is needed in future; uncomment next line:
            # asset_id = data['hostUuid']
            config = data['hostConfig']['probeConfig']['pingProbe']
            ping_address = config['ip4']
            ping_count = config.get('count', DEFAULT_PING_COUNT)
            ping_interval = config.get('interval', DEFAULT_PING_INTERVAL)
            ping_timeout = config.get('timeout', DEFAULT_PING_TIMEOUT)

            check_config(ping_count, ping_interval)
        except Exception as e:
            logging.error(f'invalid check configuration: `{e}`')
            return

        try:
            state_data = await cls.get_data(
                ping_address,
                ping_count,
                ping_interval,
                ping_timeout
            )
        except asyncio.TimeoutError:
            raise Exception('Check timed out.')
        except Exception as e:
            raise Exception(f'Check error: {e.__class__.__name__}: {e}')
        else:
            return state_data

    @classmethod
    async def get_data(cls, address, count, interval, timeout):
        data = None
        try:
            data = await cls.run_check(address, count, interval, timeout)
        except Exception as err:
            logging.exception(f'Ping error (address: {address}): `{err}`\n')
            raise

        try:
            state = cls.get_result(data)
        except Exception:
            logging.exception(f'Ping parse error (address: {address})\n')
            raise

        return state

    @staticmethod
    async def run_check(address, count, interval, timeout):
        pass

    @staticmethod
    def on_item(itm):
        return itm

    @classmethod
    def get_result(cls, data):
        itm = cls.on_item(data)
        state = {}
        state[cls.type_name] = {}
        name = itm['name']
        state[cls.type_name][name] = itm
        return state
