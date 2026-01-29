

import threading
import queue
import time
import random
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


class Consumer(threading.Thread) :
    def __init__(self, threadID, name,q) :
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID
        self.q = q

    def run( self ):
        while(True):
            d = self.q.get()
            logging.debug(d)
            time.sleep(1)
            self.q.task_done()

class Producer(threading.Thread ):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID
        self.q = []
        for n_thread in range(3):
            self.q.append(queue.Queue())

    def get_queue(self, i) :    
        return(self.q[i])

    def run( self):
        i = 0
        while(i < 100):
            for n in range(3):
                self.q[n].put(i)
            logging.debug(i)
            i+=1
            time.sleep(0.100)

if __name__ == '__main__':

    main_thread = Producer( 2, "main thread" )
    main_thread.start()

#    consumers = []
    for n in range(3):
        consumer = (Consumer(n,"consumer_" + str(n), main_thread.get_queue(n)))
        consumer.start()

#    main_thread.setDaemon(True)
