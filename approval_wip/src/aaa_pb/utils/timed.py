import time


def timed(f):
    def g(*args, **kwargs):
        start_time = time.time()
        f(*args, **kwargs)
        elapsed_time = time.time() - start_time
        elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print("================")
        print("Elapsed time: {0}".format(elapsed_time_formatted))

    return g
