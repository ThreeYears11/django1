import time

dt = time.time()
time_local = time.localtime(dt)
dt = time.strftime("%Y%m%d%H%M%S", time_local)
