


import signal


def handler(signum, frame):
    print("yoy yoyoyoy what up in the house???")


signal.signal(signal.SIGUSR1, handler)


print("Going into loop")
while(True):
    continue

print("out of loop??")