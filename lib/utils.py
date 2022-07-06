from libprobe.exceptions import CheckException


def check_config(count, interval):
    if count not in range(1, 10):
        raise CheckException('count expects an integer value between 1 and 9')
    if not 1 <= interval <= 9:
        raise CheckException('interval expects a float value between 1 and 9')
