from .types import *

player = {
    player_commands['LOGIN']: Struct(
        # Log in a player
        # Players can log in anonymously by providing a 'session' value of 'none'
        # Protocol: should be 4, TODO: enum is needed to describe the other available protocols
        # Name: is the player name, up to 255 chars
        # HorizonX: is the game screen width / 2
        # HorizonY: is the game screen height / 2
        # Flag: the two-letter country code of desired flag
        'command' / Default(PlayerCommands, 'LOGIN'),
        'protocol' / Int8ub,
        'name' / Text,
        'session' / Default(Text, 'none'),
        'horizonX' / Int16ul,
        'horizonY' / Int16ul,
        'flag' / Text
    ),
    player_commands['BACKUP']: Struct(
        # TODO: Figuere out what this is for
        'command' / Default(PlayerCommands, 'BACKUP'),
        'token' / Text
    ),
    player_commands['HORIZON']: Struct(
        # Update horizon information
        # Presumably called when the player resizes their browser window
        # HorizonX: is the game screen width / 2
        # HorizonY: is the game screen height / 2
        'command' / Default(PlayerCommands, 'HORIZON'),
        'horizonX' / Int16ul,
        'horizonY' / Int16ul,
    ),
    player_commands['ACK']: Struct(
        # TODO: Figure out what this is for
        # Have managed to maintain a connection to the server without ack-ing any packets
        'command' / Default(PlayerCommands, 'ACK')
    ),
    player_commands['PONG']: Struct(
        # Reply to a PING from the server
        # You *MUST* send this response in a timely fashion to avoid a disconnect
        # num: is the num value as supplied by the PING command, although in practise I don't think the server cares
        'command' / Default(PlayerCommands, 'PONG'),
        'num' / Int32ul
    ),
    player_commands['KEY']: Struct(
        # Send a key state for current player
        # seg: a sequential number that increments with every key press, presumably so packets that arrive out of order are interpreted correctly?
        # key: the key to change: UP, DOWN, LEFT, RIGHT, FIRE, SPECIAL
        # state: the state of the key press: True or False
        'command' / Default(PlayerCommands, 'KEY'),
        'seq' / Int32ul,
        'key' / PlayerKeys,
        'state' / Flag
    ),
    player_commands['COMMAND']: Struct(
        # Send a command to the server, eg: to switch to spectate mode: com = spectate, data = player ID
        # com: command to send
        # data: additional data for command
        'command' / Default(PlayerCommands, 'COMMAND'),
        'com' / Text,
        'data' / Text
    ),
    player_commands['SCOREDETAILED']: Struct(
        # Request a detailed score table from the server
        'command' / Default(PlayerCommands, 'SCOREDETAILED')
    ),
    player_commands['CHAT']: Struct(
        # Send a public chat message
        # text: text to send - up to 255 chars
        'command' / Default(PlayerCommands, 'CHAT'),
        'text' / Text
    ),
    player_commands['WHISPER']: Struct(
        # Send a whisper to another player
        # id: player ID to whisper
        # text: text to send - up to 255 chars
        'command' / Default(PlayerCommands, 'WHISPER'),
        'id' / Int16ul,
        'text' / Text
    ),
    player_commands['SAY']: Struct(
        # Send a local say message
        # text: text to send - up to 255 chars
        # Text can also be an emote in the format :emote:, eg: :pepe:
        'command' / Default(PlayerCommands, 'SAY'),
        'text' / Text
    ),
    player_commands['TEAMCHAT']: Struct(
        # Send a team chat message
        # text: text to send - up to 255 chars
        # Since your team = your player ID in FFA and BR this would have no effect in those modes
        'command' / Default(PlayerCommands, 'TEAMCHAT'),
        'text' / Text
    ),
    player_commands['VOTEMUTE']: Struct(
        # Vote to mute a player
        # id: player ID you're voting to mute
        'command' / Default(PlayerCommands, 'VOTEMUTE'),
        'id' / Int16ul
    ),
    player_commands['LOCALPING']: Struct(
        # TODO: figure out what this is for
        'command' / Default(PlayerCommands, 'LOCALPING'),
        'auth' / Int32ul
    )
}

server = {
    server_commands['LOGIN']: Struct(
        # Response from server to a player LOGIN
        'command' / Default(ServerCommands, 'LOGIN'),
        'success' / Flag,
        'id' / Int16ul,
        'team' / Int16ul,
        'clock' / Int32ul,
        'token' / Text,
        'type' / ShipTypes,
        'room' / Text,
        'players' / PrefixedArray(Int16ul, Struct(
            'id' / Int16ul,
            'status' / PlayerStatus,
            'level' / Int8ub,
            'name' / Text,
            'type' / ShipTypes,
            'team' / Int16ul,
            'posX' / CoordX,
            'posY' / CoordY,
            'rotation' / Rotation,
            'flag' / Int16ul,
            'upgrades' / Int8ub
        ))
    ),
    server_commands['BACKUP']: Struct(
        'command' / Default(ServerCommands, 'BACKUP')
    ),
    server_commands['PING']: Struct(
        # Ping request from server,
        # you must reply with PONG
        'command' / Default(ServerCommands, 'PING'),
        'clock' / Int32ul,
        'num' / Int32ul
    ),
    server_commands['PING_RESULT']: Struct(
        # TODO: figure out what this is for
        'command' / Default(ServerCommands, 'PING_RESULT'),
        'ping' / Int16ul,
        'playerstotal' / Int32ul,
        'playersgame' / Int32ul
    ),
    server_commands['ACK']: Struct(
        # TODO: figure out what this is for
        'command' / Default(ServerCommands, 'ACK')
    ),
    server_commands['ERROR']: Struct(
        # Error code sent from server
        # This can include notifications for disconnection/ban/kick and also throttling
        # see `error_types` for a list of valid codes
        'command' / Default(ServerCommands, 'ERROR'),
        'error' / Int8ub
    ),
    server_commands['COMMAND_REPLY']: Struct(
        'command' / Default(ServerCommands, 'COMMAND_REPLY'),
        'type' / Int8ub,
        'text' / TextBig
    ),
    server_commands['PLAYER_NEW']: Struct(
        # Sent from the server to notify a new player has jointed
        'command' / Default(ServerCommands, 'PLAYER_NEW'),
        'id' / Int16ul,
        'status' / PlayerStatus,
        'name' / Text,
        'type' / ShipTypes,
        'team' / Int16ul,
        'posX' / CoordX,
        'posY' / CoordY,
        'rotation' / Rotation,
        'flag' / Int16ul,
        'upgrades' / Int8ub
    ),
    server_commands['PLAYER_LEAVE']: Struct(
        # Sent from the server to notify a player has left
        'command' / Default(ServerCommands, 'PLAYER_LEAVE'),
        'id' / Int16ul
    ),
    server_commands['PLAYER_UPDATE']: Struct(
        # Sent from the server to notify a player has been updated
        'command' / Default(ServerCommands, 'PLAYER_UPDATE'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'keystate' / KeyState, # 1 = UP, 2 = DOWN, 4 = LEFT, 8 = RIGHT
        'upgrades' / Int8ub,
        'posX' / Coord24,
        'posY' / Coord24,
        'rotation' / Rotation,
        'speedX' / Speed,
        'speedY' / Speed
    ),
    server_commands['PLAYER_FIRE']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_FIRE'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'energy' / HealthEnergy,
        'energyRegem' / Regen,
        'projectiles' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'type' / MissileTypes,
            'posX' / CoordX,
            'posY' / CoordY,
            'speedX' / Speed,
            'speedY' / Speed,
            'accelX' / Accel,
            'accelY' / Accel,
            'maxSpeed' / Speed
        ))
    ),
    #server_commands['PLAYER_SAY']: Struct(
    #    'id' / Int16ul,
    #    'text' / Text
    #),
    server_commands['PLAYER_RESPAWN']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_RESPAWN'),
        'id' / Int16ul,
        'posX' / Coord24,
        'posY' / Coord24,
        'rotation' / Rotation,
        'upgrades' / Int8ub
    ),
    server_commands['PLAYER_FLAG']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_FLAG'),
        'id' / Int16ul,
        'flag' / Int16ul
    ),
    server_commands['PLAYER_HIT']: Struct(
        # The id here is the id of the hit, not a player ID,
        # I bet this ID relates to the projectile
        'command' / Default(ServerCommands, 'PLAYER_HIT'),
        'id' / Int16ul,
        'type' / Int8ub,
        'posX' / CoordX,
        'posY' / CoordY,
        'owner' / Int16ul,
        'players' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'health' / HealthEnergy,
            'healthRegen' / Regen
        ))
    ),
    server_commands['PLAYER_KILL']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_KILL'),
        'id' / Int16ul,
        'killer' / Int16ul,
        'posX' / CoordX,
        'posY' / CoordY
    ),
    server_commands['PLAYER_UPGRADE']: Struct(
        # Sent whenever a player applies an upgrade point, or maybe collects one?
        # Haven't seen this appear as anything other than 0 on all fronts,
        # so presumably the individual values apply to the current player?
        'command' / Default(ServerCommands, 'PLAYER_UPGRADE'),
        'upgrades' / Int16ul,
        'type' / Int8ub,
        'speed' / Int8ub,
        'defense' / Int8ub,
        'energy' / Int8ub,
        'missile' / Int8ub
    ),
    server_commands['PLAYER_TYPE']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_TYPE'),
        'id' / Int16ul,
        'type' / ShipTypes
    ),
    server_commands['PLAYER_POWERUP']: Struct(
        # Sent whenever a player gains a powerup
        # Type only ever seems to be 1, does not distinguish between Shield or Rampage
        # As far as I can tell, the JS client ignores this command?
        'command' / Default(ServerCommands, 'PLAYER_POWERUP'),
        'type' / Int8ub,
        'duration' / Int32ul
    ),
    server_commands['PLAYER_LEVEL']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_LEVEL'),
        'id' / Int16ul,
        'type' / Int8ub,
        'level' / Int8ub
    ),
    server_commands['GAME_FLAG']: Struct(
        'command' / Default(ServerCommands, 'GAME_FLAG'),
        'type' / Int8ub,
        'flag' / Int8ub,
        'id' / Int16ul,
        'posX' / CoordX,
        'posY' / CoordY,
        'blueteam' / Int8ub,
        'redteam' / Int8ub
    ),
    server_commands['GAME_SPECTATE']: Struct(
        'command' / Default(ServerCommands, 'GAME_SPECTATE'),
        'id' / Int16ul
    ),
    server_commands['GAME_PLAYERSALIVE']: Struct(
        'command' / Default(ServerCommands, 'GAME_PLAYERSALIVE'),
        'players' / Int16ul
    ),
    server_commands['GAME_FIREWALL']: Struct(
        'command' / Default(ServerCommands, 'GAME_FIREWALL'),
        'type' / Int8ub,
        'status' / Int8ub,
        'posX' / CoordX,
        'posY' / CoordY,
        'radius' / Float32b,
        'speed' / Float32b
    ),
    server_commands['EVENT_REPEL']: Struct(
        # Command to indicate the Goliath's special repel ability
        # players is a list of players repelled by the ability
        # mobs is a list of the projectiles that the Goliath player has taken ownership of by repelling
        'command' / Default(ServerCommands, 'EVENT_REPEL'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'posX' / CoordX,
        'posY' / CoordY,
        'rotation' / Rotation,
        'speedX' / Speed,
        'speedY' / Speed,
        'energy' / HealthEnergy,
        'energyRegen' / Regen,
        'players' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'keystate' / KeyState,
            'posX' / CoordX,
            'posY' / CoordY,
            'rotation' / Rotation,
            'speedX' / Speed,
            'speedY' / Speed,
            'energy' / HealthEnergy,
            'energyRegen' / Regen,
            'playerHealth' / HealthEnergy,
            'playerHealthRegen' / Regen
        )),
        'mobs' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'type' / MobTypes,
            'posX' / CoordX,
            'posY' / CoordY,
            'speedX' / Speed,
            'speedY' / Speed,
            'accelX' / Accel,
            'accelY' / Accel,
            'maxSpeed' / Speed
        ))
    ),
    server_commands['EVENT_BOOST']: Struct(
        'command' / Default(ServerCommands, 'EVENT_BOOST'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'boost' / Flag,
        'posX' / CoordX,
        'posY' / CoordY,
        'rotation' / Rotation,
        'speedX' / Speed,
        'speedY' / Speed,
        'energy' / HealthEnergy,
        'energyRegen' / Regen,
    ),
    server_commands['EVENT_BOUNCE']: Struct(
        'command' / Default(ServerCommands, 'EVENT_BOUNCE'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'keystate' / KeyState,
        'posX' / CoordX,
        'posY' / CoordY,
        'rotation' / Rotation,
        'speedX' / Speed,
        'speedY' / Speed,
    ),
    server_commands['EVENT_STEALTH']: Struct(
        'command' / Default(ServerCommands, 'EVENT_STEALTH'),
        'id' / Int16ul,
        'state' / Flag,
        'energy' / HealthEnergy,
        'energyRegen' / Regen,
    ),
    server_commands['EVENT_LEAVEHORIZON']: Struct(
        'command' / Default(ServerCommands, 'EVENT_LEAVEHORIZON'),
        'type' / Int8ub,
        'id' / Int16ul
    ),
    server_commands['MOB_UPDATE']: Struct(
        'command' / Default(ServerCommands, 'MOB_UPDATE'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'type' / MobTypes,
        'posX' / CoordX,
        'posY' / CoordY,
        'speedX' / Speed,
        'speedY' / Speed,
        'accelX' / Accel,
        'accelY' / Accel,
        'maxSpeed' / Speed
    ),
    server_commands['MOB_UPDATE_STATIONARY']: Struct(
        'command' / Default(ServerCommands, 'MOB_UPDATE_STATIONARY'),
        'id' / Int16ul,
        'type' / MobTypes,
        'posX' / Float32b,
        'posY' / Float32b
    ),
    server_commands['MOB_DESPAWN']: Struct(
        'command' / Default(ServerCommands, 'MOB_DESPAWN'),
        'id' / Int16ul,
        'type' / MobTypes
    ),
    server_commands['MOB_DESPAWN_COORDS']: Struct(
        'command' / Default(ServerCommands, 'MOB_DESPAWN_COORDS'),
        'id' / Int16ul,
        'type' / MobTypes,
        'posX' / CoordX,
        'posY' / CoordY
    ),
    server_commands['SCORE_UPDATE']: Struct(
        'command' / Default(ServerCommands, 'SCORE_UPDATE'),
        'id' / Int16ul,
        'score' / Int32ul,
        'earnings' / Int32ul,
        'upgrades' / Int16ul,
        'totalkills' / Int32ul,
        'totaldeaths' / Int32ul
    ),
    server_commands['SCORE_BOARD']: Struct(
        'command' / Default(ServerCommands, 'SCORE_BOARD'),
        'data' / PrefixedArray(Int16ul, Struct(
            'id' / Int16ul,
            'score' / Int32ul,
            'level' / Int8ul
        )),
        'rankings' / PrefixedArray(Int16ul, Struct(
            'id' / Int16ul,
            'x' / Int8ul,
            'y' / Int8ul
        ))
    ),
    server_commands['SCORE_DETAILED']: Struct(
        # Table of scores for players
        'command' / Default(ServerCommands, 'SCORE_DETAILED'),
        'scores' / PrefixedArray(Int16ul, Struct(
            'id' / Int16ul,
            'level' / Int8ul,
            'score' / Int32ul,
            'kills' / Int16ul,
            'deaths' / Int16ul,
            'damage' / Float32l,
            'ping' / Int16ul
        ))
    ),
    server_commands['SCORE_DETAILED_CTF']: Struct(
        'command' / Default(ServerCommands, 'SCORE_DETAILED_CTF'),
        'scores' / PrefixedArray(Int16ul, Struct(
            'id' / Int16ul,
            'level' / Int8ub,
            'captures' / Int16ul,
            'score' / Int32ul,
            'kills' / Int16ul,
            'deaths' / Int16ul,
            'damage' / Float32b,
            'ping' / Int16ul
        ))
    ),
    server_commands['SCORE_DETAILED_BTR']: Struct(
        'command' / Default(ServerCommands, 'SCORE_DETAILED_BTR'),
        'scores' / PrefixedArray(Int16ul, Struct(
            'id' / Int16ul,
            'level' / Int8ub,
            'alive' / Flag,
            'wins' / Int16ul,
            'score' / Int32ul,
            'kills' / Int16ul,
            'deaths' / Int16ul,
            'damage' / Float32b,
            'ping' / Int16ul
        ))
    ),
    server_commands['CHAT_TEAM']: Struct(
        'command' / Default(ServerCommands, 'CHAT_TEAM'),
        'id' / Int16ul,
        'text' / Text
    ),
    server_commands['CHAT_PUBLIC']: Struct(
        'command' / Default(ServerCommands, 'CHAT_PUBLIC'),
        'id' / Int16ul,
        'text' / Text
    ),
    server_commands['CHAT_SAY']: Struct(
        'command' / Default(ServerCommands, 'CHAT_SAY'),
        'id' / Int16ul,
        'text' / Text
    ),
    server_commands['CHAT_WHISPER']: Struct(
        'command' / Default(ServerCommands, 'CHAT_WHISPER'),
        'id' / Int16ul,
        'to' / Int16ul,
        'text' / Text
    ),
    server_commands['CHAT_VOTEMUTEPASSED']: Struct(
        'command' / Default(ServerCommands, 'CHAT_VOTEMUTEPASSED'),
        'id' / Int16ul
    ),
    server_commands['CHAT_VOTEMUTED']: Struct(
        'command' / Default(ServerCommands, 'CHAT_VOTEMUTED')
    ),
    server_commands['SERVER_MESSAGE']: Struct(
        'command' / Default(ServerCommands, 'SERVER_MESSAGE'),
        'type' / MessageTypes,
        'duration' / Int32ul,
        'message' / TextBig
    ),
    server_commands['SERVER_CUSTOM']: Struct(
        'command' / Default(ServerCommands, 'SERVER_CUSTOM'),
        'type' / Int8ub,
        'message' / TextBig
    )
}

def build_player_command(command,  **kwargs):
    id = player_commands[command]
    return player[id].build(kwargs)

def decode_server_command(command):
    id = command[0]
    if isinstance(id, str):
        id = ord(id)
    #name = server_commands.keys()[server_commands.values().index(id)]
    #print("Parsing Command ID: {}, Name: {}".format(id, name))
    return server[id].parse(command)