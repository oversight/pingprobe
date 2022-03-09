def check_config(count, interval):
    if count not in range(1, 10):
        raise Exception('count expects an integer value between 1 and 9')
    if not 1 <= interval <= 9:
        raise Exception('interval expects a float value between 1 and 9')