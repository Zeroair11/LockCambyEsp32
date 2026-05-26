import time

from config import *

fail_count = 0

locked_until = 0

def is_locked():

    global locked_until

    return time.time() < locked_until

def access_failed():

    global fail_count
    global locked_until

    fail_count += 1

    print("FAIL:", fail_count)

    if fail_count >= MAX_FAIL_ATTEMPTS:

        locked_until = (
            time.time()
            + LOCKOUT_TIME
        )

        fail_count = 0

        return True

    return False

def access_success():

    global fail_count

    fail_count = 0