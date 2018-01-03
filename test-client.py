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
                client.key('UP', True)
                print("Me: {}, {}".format(client.player.posX, client.player.posY))


client = Client()

@client.on('LOGIN')
def on_login(client, message):
    print("Client has logged in!")

_t_update = ClientUpdate()
_t_update.start()

client.connect(
    name='TestBot',
    flag='GB',
    region='eu',
    room='ffa1',
    enable_trace=True
)

_t_update.stop()
_t_update.join()