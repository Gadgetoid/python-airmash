import threading

from airmash.client import Client

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

    def run(self):
        while not self.wait():
            if client.connected:
                client.key('LEFT', True)

def track_position(player, key, old, new):
    new = [int(x) for x in new]
    print("Position: {} {}".format(*new))

def track_rotation(player, key, old, new):
    print("Rotation: {}".format(new))

client = Client(enable_debug=False)

@client.on('LOGIN')
def on_login(client, message):
    print("Client has logged in!")
    print("Player ID: {}".format(client.player.id))
    client.player.on_change('position', track_position)
    client.player.on_change('rotation', track_rotation)

@client.on('PLAYER_HIT')
def on_hit(client, message):
    for player in message.players:
        if player.id == client.player.id:
            print("Uh oh! I've been hit!")

_t_update = ClientUpdate()
_t_update.start()

client.connect(
    name='TestBot',
    flag='GB',
    region='eu',
    room='ffa1',
    enable_trace=False
)

_t_update.stop()
_t_update.join()