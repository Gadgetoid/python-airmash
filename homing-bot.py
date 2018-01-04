#! /usr/bin/python3
import sys
sys.path.append("..")

import random
from airmash.client import Client
from airmash.player import Player
from airmash import packets
import threading
import time
import names
import math

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
FIRE = 'FIRE'
SPECIAL = 'SPECIAL'

ANGLE_FUZZ = math.pi / 11.
SHOOT_CUTOFF = 600.
MAX_TRIES=50

# This is a null player who can be used for debugging.
ZERO_PLAYER = Player(99999999)
ZERO_PLAYER.posX=0
ZERO_PLAYER.posX=0

me = None

def rare():
  return random.randrange(0, 10) == 0

def get_nearest_player():
  #return ZERO_PLAYER
  minDist = float("inf")
  nearestPlayer = None
  for uid in client.players:
    p = client.players[uid]
    if p == client.player:
      continue
    dist = p.dist_from(client.player)
    if (dist < minDist):
      minDist = dist
      nearestPlayer = p
  return nearestPlayer 

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
    
    def target_player(self, player):
      wrongness = client.player.angle_to(player) - client.player.rotation;
      print("Aiming at {0} who is {1} away and {2} off".format(player.name,
                                                               player.dist_from(client.player),
                                                               client.player.angle_to(player)))
      print ("Target location: {0}, {1}".format(player.posX, player.posY))
      print ("My location: {0}, {1}".format(client.player.posX, client.player.posY))
      tries = 0
      direction = UP
      self.send_keydown(direction)
      while (tries < MAX_TRIES) and (abs(wrongness) > ANGLE_FUZZ) :
        if rare() and rare():
          self.send_keyup(direction)
          direction = (DOWN if direction == UP else UP)
          self.send_keydown(direction)
        print(wrongness)
        keypress = None
        if (wrongness < -ANGLE_FUZZ):
          keypress = LEFT
        if wrongness > ANGLE_FUZZ:
          keypress = RIGHT
        if keypress is not None:
          print(keypress)
          self.send_keydown(keypress)
          self.wait(.1)
          self.send_keyup(keypress)
        wrongness = client.player.angle_to(player) - client.player.rotation;
        tries+=1
      self.send_keydown(direction)
      print("Aimed at {0}".format(player.name))

    def charge_or_shoot(self, player):
      orig_health = client.player.health;
      dist = client.player.dist_from(player)
      cooldown = 0; 
      while client.player.dist_from(player) <= dist:
        print ("My location: {0}, {1}".format(client.player.posX, client.player.posY))
        dist = client.player.dist_from(player) 
        if (dist > SHOOT_CUTOFF) or cooldown > 0 or rare():
          print("Charging")
          keypress = (DOWN if rare() and rare() else UP)
          self.send_keydown(keypress)
          self.wait(random.randrange(1, 5)/4.)
          self.send_keyup(keypress)
        else:
          keypress = FIRE
          # If neither prowler nor mohawk
          if not client.player.type in [3, 5]:
            if not (random.randrange(0, 3) == 0):
              keypress = SPECIAL 
          print("Firing")
          self.send_keydown(keypress)
          self.wait(.15)
          self.send_keyup(keypress)
          cooldown = 3
        if (client.player.type == 5):
          if (client.player.health < orig_health) or (cooldown == 1) or rare():
            self.key_up(SPECIAL)
            self.key_down(SPECIAL)
            self.wait(.15)
        if (client.player.type == 3):
          cooldown = 0
        cooldown-=1
        if (client.player.dist_from(get_nearest_player()) < SHOOT_CUTOFF) and (client.player.dist_from(get_nearest_player()) < dist/2.):
          # Someone is much closer. Abort, deal with the immediate threat.
          print("Punting to deal with near threat")
          return;
          # Recloak. 
        self.target_player(player)
     
    def react_to_nearest(self):
      nearestPlayer = get_nearest_player()
      if (nearestPlayer is None):
        print("Nobody detected")
        return
      print("Targetting {0}".format(nearestPlayer.name))
      # Attack them until someone dies or we're too badly shot at.
      # Are we pointed vaguely near them?
      self.target_player(nearestPlayer)
      # Attack.
      self.charge_or_shoot(nearestPlayer)
 
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
        while True:
            self.react_to_nearest()
            #my_status = client.players[me].status


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

