


import time


init = time.clock()
print("init = " + str(init))

lapso = 12 # secs

while( (time.clock() - init) < lapso ):
    print(str(time.clock()))

print("LAPSO!!")