import packets
import websocket
import threading
import time

ws = None

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._event = threading.Event()

    def stop(self):
        self._event.set()

    def wait(self, timeout=3):
        return self._event.wait(timeout=timeout)

class ClientUpdate(StoppableThread):
    def __init__(self, *args, **kwargs):
        StoppableThread.__init__(self, *args, **kwargs)

    def run(self):
        key_num = 0
        seq = 0
        keys = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        states = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        while not self.wait():
            key = keys[key_num % len(keys)]
            key_num += 1
            for old_key in keys:
                if old_key != key:
                    if states[old_key]:
                        packet = packets.build_player_command('KEY', dict(seq=seq, key=old_key, state=False))
                        ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
                        states[old_key] = False
                        seq += 1

            packet = packets.build_player_command('KEY', dict(seq=seq, key=key, state=True))
            ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            states[key] = True
            seq += 1
            print("Position: {}:{}".format(me.posX, me.posY))

class Player():
    def __init__(self, data={}):
        self.update(data)

    def update(self, data):
        self.id = self._get_default(data, 'id', 0)
        self.status = self._get_default(data, 'status', 0)
        self.level = self._get_default(data, 'level', 0)
        self.name = self._get_default(data, 'name', "")
        self.team = self._get_default(data, 'team', 0)
        self.flag = self._get_default(data, 'flag', 0)
        self.keystate = self._get_default(data, 'keystate', 0)
        self.upgrades = self._get_default(data, 'upgrade', 0)
        self.posX = self._get_default(data, 'posX', 0)
        self.posY = self._get_default(data, 'posY', 0)
        self.rot = self._get_default(data, 'rot', 0)
        self.speedX = self._get_default(data, 'speedX', 0)
        self.speedY = self._get_default(data, 'speedY', 0)

    def _get_default(self, data, name, default):
        return data.get(name, self.__dict__.get(name, default))

players = {}
me = Player()

_t_update = None

def on_message(ws, message):
    command = packets.decode_server_command(message)
    #print(command)
    if command.command == 'PING':
        cmd = packets.build_player_command('PONG', dict(num=command.num))
        ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)
        return

    if command.command == 'PLAYER_UPDATE':
        players[command.id].update(command)
        if command.id == me.id:
            me.update(command)
        return

    if command.command == 'PLAYER_LEAVE':
        del players[command.id]
        return

    if command.command == 'PLAYER_NEW':
        players[command.id] = Player(command)
        return

    if command.command == 'PLAYER_KILL':
        killer = players[command.killer].name
        killed = players[command.id].name
        print("Player {} killed by {}".format(killed, killer))
        return

    if command.command == 'LOGIN':
        me.update(command)
        print("Player ID: {}".format(me.id))
        last_id = ''
        for player in command.players:
            players[player.id] = Player(player)
            last_id = player.id
        cmd = packets.build_player_command('COMMAND', dict(
            com='spectate',
            data=str(last_id)
        ))
        ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)
        return

def on_error(ws, error):
    print(error)

def on_close(ws):
    global _t_update
    print("### closed ###")
    if _t_update is not None:
        _t_update.stop()
        _t_update.join()

def on_open(ws):
    global _t_update
    print("### Opened ###")
    cmd = packets.build_player_command('LOGIN', dict(
        protocol=4,
        name='test',
        session='none',
        horizonX=1024 / 2,
        horizonY=768 / 2,
        flag='en'
    ))
    ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)
    #_t_update = ClientUpdate()
    #_t_update.start()


def run():
    global ws
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(packets.SERVER_ADDR,
        subprotocols=['binary'],
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        on_open = on_open)
    ws.run_forever(origin = 'https://airma.sh')

if __name__ == "__main__":
    run()