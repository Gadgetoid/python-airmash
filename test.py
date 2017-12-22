from airmash import packets
from airmash.player import Player
from airmash.mob import Mob
from airmash.country import COUNTRY_CODES
import websocket
import threading
import time

ws = None

def track_rotation(player, key, old, new):
    print("Rotation: {}".format(new))

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
        #key_num = 0
        seq = 0
        state = True
        #keys = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'FIRE', 'SPECIAL']
        #states = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False, 'FIRE': False, 'SPECIAL': False}
        while not self.wait():
            packet = packets.build_player_command('KEY', seq=seq, key='LEFT', state=True)
            ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            seq += 1
            packet = packets.build_player_command('KEY', seq=seq, key='UP', state=True)
            ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            seq += 1
            #my_status = players[me].status
            #print("Status: {}".format(my_status))
            packet = packets.build_player_command('KEY', seq=seq, key='FIRE', state=state)
            ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            seq += 1
            state = not state
            #packet = packets.build_player_command('COMMAND', dict(com='respawn', data='2'))
            #ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            #code = seq % len(COUNTRY_CODES.keys())
            #packet = packets.build_player_command('COMMAND', dict(com='flag', data=COUNTRY_CODES.keys()[code]))
            #ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            #key = keys[key_num % len(keys)]
            #key_num += 1
            #for old_key in keys:
            #    if old_key != key:
            #        if states[old_key]:
            #            packet = packets.build_player_command('KEY', dict(seq=seq, key=old_key, state=False))
            #            ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            #            states[old_key] = False
            #            seq += 1

            #packet = packets.build_player_command('KEY', dict(seq=seq, key=key, state=True))
            #ws.send(packet, opcode=websocket.ABNF.OPCODE_BINARY)
            #states[key] = True
            #print("Position: {}:{}".format(me.posX, me.posY))

players = {}
projectiles = {}
me = None

_t_update = None


def on_open(ws):
    global _t_update
    print("### Opened ###")
    cmd = packets.build_player_command('LOGIN',
        protocol=4,
        name='test',
        session='none',
        horizonX=1920 / 2,
        horizonY=1920 / 2,
        flag='GB'
    )
    ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)
    #_t_update = ClientUpdate()
    #_t_update.start()

def on_close(ws):
    global _t_update
    print("### closed ###")
    if _t_update is not None:
        _t_update.stop()
        _t_update.join()

def on_message(ws, message):
    message = packets.decode_server_command(message)

    if message.command == 'PING':
        cmd = packets.build_player_command('PONG', num=message.num)
        ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)
        return

    if message.command == 'ERROR':
        error_type, error_text = packets.error_types[message.error]
        print("Server: [{} ({})] {}".format(message.error, error_type, error_text))
        return

    if message.command == 'GAME_SPECTATE':
        return

    if message.command == 'LOGIN':
        global me
        me = message.id
        print("Your ID: {}".format(me))
        last_id = ''
        for player in message.players:
            players[player.id] = Player(player.id, player)
            last_id = player.id
        players[me].update(message)

        #players[me].on_change('rotation', track_rotation)

        #players[me].on_change('upgrades', ks)
        #players[me].on_change('keystate', ks)

        cmd = packets.build_player_command('SCOREDETAILED')
        ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)

        #cmd = packets.build_player_command('COMMAND', dict(
        #    com='spectate',
        #    data=str(last_id)
        #))
        #ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)
        return

    if message.command == 'SERVER_MESSAGE':
        print(u"Server: [{}] {}".format(message.type, message.message))
        return

    if message.command == 'CHAT_PUBLIC':
        player = players[message.id]
        print(u"Public Chat: [{}] {}".format(player.name, message.text))
        return

    if message.command == 'CHAT_TEAM':
        player = players[message.id]
        print(u"Team Chat: [{}] {}".format(player.name, message.text))
        return

    if message.command == 'CHAT_WHISPER':
        w_from = players[message.id]
        w_to = players[message.to]
        print(u"Whisper: [{}] {}".format(w_from.name, message.text))
        return

    if message.command == 'SCORE_BOARD':
        for player in message.data:
            players[player.id].update(player)
        for player in message.rankings:
            players[player.id].update(player)
        return

    if message.command in ['SCORE_DETAILED', 'SCORE_DETAILED_CTF', 'SCORE_DETAILED_BTR']:
        for score in message.scores:
            if score.id in players:
                players[score.id].update(score)
        return

    if message.command == 'PLAYER_HIT':
        # Update the health and healthRegen of hit player(s)
        projectile = None
        if message.id in projectiles:
            projectile = projectiles[message.id]
            for player in message.players:
                players[player.id].update(player)
                print(u"Action: {} hit by {}'s {}".format(players[player.id].name, projectile.owner.name, projectile.type))
        return

    if message.command in ['EVENT_STEALTH', 'EVENT_REPEL', 'EVENT_BOOST', 'EVENT_BOUNCE', 'SCORE_UPDATE', 'PLAYER_LEVEL', 'PLAYER_TYPE', 'PLAYER_FIRE', 'PLAYER_RESPAWN', 'PLAYER_UPDATE']:

        # All of these commands trigger some change to the player state, so handle them together for now
        if message.id in players:
            players[message.id].update(message)
        else:
            print(u"WARNING: Players missing ID: {} for command: {}".format(message.id, message.command))
        player = players[message.id]

        if message.command == 'PLAYER_FIRE':
            for projectile in message.projectiles:
                print(u"Action: New projectile of type {}".format(projectile.type))
                projectiles[projectile.id] = Mob(projectile.id, players[message.id], projectile)
            return

        if message.command == 'EVENT_STEALTH':
            #print("Player {} has gone into stealth!".format(player.name))
            return

        # These commands trigger an update to multiple other players and have a `.players` array
        if message.command in ['EVENT_REPEL', 'PLAYER_HIT']:
            for player in message.players:
                players[player.id].update(player)
            
            # Handle projectiles hijacked by repel
            if message.command == 'EVENT_REPEL':
                print(u"Action: {} uses repel. {} players and {} projectiles repelled.".format(players[message.id].name, len(message.players), len(message.mobs)))
                for projectile in message.mobs:
                    if projectile.id in projectiles:
                        projectiles[projectile.id].update(projectile, new_owner=players[message.id])
                    else:
                        projectiles[projectile.id] = Mob(projectile.id, players[message.id], projectile)
            return

        return

    if message.command == 'PLAYER_KILL':
        killer = players[message.killer].name
        killed = players[message.id].name
        print(u"Action: {} killed by {} at ({}, {})".format(killed, killer, message.posX, message.posY))
        return

    if message.command == 'PLAYER_LEAVE':
        print(u"Action: {} left".format(players[message.id].name))
        players[message.id].online = False
        return

    if message.command == 'PLAYER_NEW':
        players[message.id] = Player(message.id, message)
        print(u"Action: {} joined".format(players[message.id].name))
        return

    if message.command == 'PLAYER_POWERUP':
        # Just has type and duration!? But no player id.
        # Does this mean we've picked up a powerup?
        return

    if message.command == 'PLAYER_UPGRADE':
        # Again, no player id.
        # Does this relate to the current player?
        return

    if message.command == 'EVENT_LEAVEHORIZON':
        # Not sure how to interpret this yet
        return

    if message.command == 'PING_RESULT':
        # This returns total players, and players playing I think,
        # plus a uint16 "ping" value
        return

    # Mobs are missiles. But are they also upgrade crates and powerups?
    if message.command in ['MOB_UPDATE', 'MOB_UPDATE_STATIONARY']:
        print(u"Action: Mob update of type {}".format(message.type))
        if message.id in projectiles:
            projectiles[message.id].update(message)
        else:
            print("WARNING: Mob type of {} does not exist? {}".format(message.type, message.id))
            projectiles[message.id] = Mob(message.id, None, message)
        return

    if message.command in ['MOB_DESPAWN', 'MOB_DESPAWN_COORDS']:
        if message.id in projectiles:
            projectiles[message.id].update(message)
            projectiles[message.id].despawn()
        return

    print(u"WARNING: Unhandled command: {}".format(message.command))

def on_error(ws, error):
    print(error)

def run():
    global ws
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(packets.SERVER_ADDR,
        subprotocols=['binary'],
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        on_open = on_open)

    ws.run_forever(origin = 'https://airma.sh')

if __name__ == "__main__":
    run()
