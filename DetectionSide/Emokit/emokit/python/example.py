import time

from emokit.emotiv import Emotiv
from emokit.packet import EmotivNewPacket

if __name__ == "__main__":
    with Emotiv(display_output=True, verbose=False) as emotiv:
        while True:
            PACK = emotiv.dequeue()

            while PACK is not None:
                print('HAY \n')
                print([PACK.sensors['O1']['value']])
                PACK = emotiv.dequeue()
  #          time.sleep(0.1)
