#! /usr/bin/python3

from airmash import packets
from airmash.player import Player
from airmash.mob import Mob
from airmash.country import COUNTRY_CODES
from airmash import games
import random
import websocket
import threading
import time
import names

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
FIRE = 'FIRE'
SPECIAL = 'SPECIAL'

def rare():
  return random.randrange(0, 10) == 0

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._event = threading.Event()

    def stop(self):
        self._event.set()

    def wait(self, timeout=1):
        return self._event.wait(timeout=timeout)

class ClientUpdate(StoppableThread):
    def __init__(self, *args, **kwargs):
        StoppableThread.__init__(self, *args, **kwargs)
        self.keyProbs = {};
        keys = [None, None, UP, UP, UP, UP, DOWN, LEFT, RIGHT, FIRE, FIRE, FIRE, SPECIAL]
        for i in set(keys):
          self.keyProbs[i] = []
          for j in keys:
            for k in range(random.randrange(0, 3)):
              self.keyProbs[i].append(j)
        print(self.keyProbs) 
            
    def send_keydown(self, key):
      client.key(key=key, state=True)

    def send_keyup(self, key):
      client.key(key=key, state=False)

    def run(self):
        while not self.wait():
          if client.connected:
            break
        packet = packets.build_player_command('COMMAND', com='respawn', data=str(random.randrange(1,6)))
        client.send(packet)
        if False: #rare(): 
          packet = packets.build_player_command('CHAT', text = "All hail the robot overlords!")
          client.send(packet)
        self.wait(2)

        lastKey = None
        pressedKeys = []
        while not self.wait(random.randrange(1, 8)/4.):
            key = random.choice(self.keyProbs[lastKey])
            #print("sending ", key)
            lastKey = key
            if key is None:
              continue
            if key in pressedKeys:
              self.send_keyup(key);
              pressedKeys.remove(key)
            else:
              self.send_keydown(key)
              pressedKeys.append(key)
            my_status = players[me].status
            #print("Status: {}".format(my_status))
            #print("Position: {}:{}".format(me.posX, me.posY))

client = Client()

@client.on('LOGIN')
def on_login(client, message):
    print("Client has logged in!")

_t_update = ClientUpdate()
_t_update.start()

name = names.get_full_name()
if rare():
  name = "Robot " + name
name = name[:20]
print("Name is ", name)

client.connect(
    name=name,
    flag='US',
    region='us',
    room='ffa1',
    enable_trace=True
)

_t_update.stop()
_t_update.join()

