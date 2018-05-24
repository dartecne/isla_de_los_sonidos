import threading
import time
import random
import logging
import queue

import MIDI_interface

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


class Father( threading.Thread ):
#    data = -1
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID
        self.q = queue.Queue()
        self.MIDI = MIDI_interface.MIDI_interface()
        self.MIDI.connect()
        self.MIDI.test_note_on()

    def get_queue(self):
        return self.q

    def get_MIDI(self):
        return self.MIDI

    def run(self):
        while(1) :
         self.data = random.randint(0, 6)
         self.q.put(self.data)
         note = "C-" + str(self.data)
         logging.debug( note )
         self.MIDI.note_on(note)
         time.sleep(self.data)

class Mother(threading.Thread ):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID

    def set_queue(self,q):
        self.q = q

    def set_MIDI(self,MIDI):
        self.MIDI = MIDI

    def run(self):
        while(1):
            logging.debug(str(self.q.get()))
            self.MIDI.note_on("C-6")
            time.sleep(1)

class Son(Father):
    def run(self):
        while(1):
            logging.debug(str(self.data))
            time.sleep(1)

if __name__ == '__main__':
    father = Father(69, "father_69")
    mother = Mother(1, "mother_1")
    mother.set_queue(father.get_queue())
    mother.set_MIDI(father.get_MIDI())
    father.start()
    mother.start()

