from commands import *

class AdapterCoordX(Adapter):
    def _encode(self, obj, ctx):
        return int(obj * 2) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 2.0

class AdapterCoordY(Adapter):
    def _encode(self, obj, ctx):
        return (obj * 2) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 2.0

class AdapterRotation(Adapter):
    def _encode(self, obj, ctx):
        return int(obj * 6553.6)
    def _decode(self, obj, ctx):
        return obj / 6553.6

class AdapterSpeed(Adapter):
    def _encode(self, obj, ctx):
        return int(obj * 1638.4) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 1638.4

class AdapterAccel(Adapter):
    def _encode(self, obj, ctx):
        return int(obj * 32768) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 32768.0

class AdapterRegen(Adapter):
    def _encode(self, obj, ctx):
        return int(obj * 1e6) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 1e6

class AdapterHealthEnergy(Adapter):
    def _encode(self, obj, ctx):
        return int(obj * 255)
    def _decode(self, obj, ctx):
        return obj / 255

class AdapterCoord24(Adapter):
    def _encode(self, obj, ctx):
        return (obj * 512) + 8388608
    def _decode(self, obj, ctx):
        return (obj - 8388608) / 512.0

CoordX = AdapterCoordX(Int16ul)
CoordY = AdapterCoordY(Int16ul)
Coord24 = AdapterCoord24(Int24ub)
Rotation = AdapterRotation(Int16ul)

Speed = AdapterSpeed(Int16ul)
Accel = AdapterAccel(Int16ul)
Regen = AdapterRegen(Int16ul)
HealthEnergy = AdapterHealthEnergy(Int8ub)
Text = PascalString(Int8ub, encoding='UTF-8')
TextBig = PascalString(Int16ul, encoding='UTF-8')

player = {
    player_commands['LOGIN']: Struct(
        'command' / Default(PlayerCommands, 'LOGIN'),
        'protocol' / Int8ub,
        'name' / Text,
        'session' / Text,
        'horizonX' / Int16ul,
        'horizonY' / Int16ul,
        'flag' / Text
    ),
    player_commands['BACKUP']: Struct(
        'command' / Default(PlayerCommands, 'BACKUP'),
        'token' / Text
    ),
    player_commands['HORIZON']: Struct(
        'command' / Default(PlayerCommands, 'HORIZON'),
        'horizonX' / Int16ul,
        'horizonY' / Int16ul,
    ),
    player_commands['ACK']: Struct(
        'command' / Default(PlayerCommands, 'ACK')
    ),
    player_commands['PONG']: Struct(
        'command' / Default(PlayerCommands, 'PONG'),
        'num' / Int32ul
    ),
    player_commands['KEY']: Struct(
        'command' / Default(PlayerCommands, 'KEY'),
        'seq' / Int32ul,
        'key' / PlayerKeys,
        'state' / Flag
    ),
    player_commands['COMMAND']: Struct(
        'command' / Default(PlayerCommands, 'COMMAND'),
        'com' / Text,
        'data' / Text
    ),
    player_commands['SCOREDETAILED']: Struct(
        'command' / Default(PlayerCommands, 'SCOREDETAILED'),
        'text' / Text
    ),
    player_commands['WHISPER']: Struct(
        'command' / Default(PlayerCommands, 'WHISPER'),
        'id' / Int16ul,
        'text' / Text
    ),
    player_commands['SAY']: Struct(
        'command' / Default(PlayerCommands, 'SAY'),
        'text' / Text
    ),
    player_commands['TEAMCHAT']: Struct(
        'command' / Default(PlayerCommands, 'TEAMCHAT'),
        'text' / Text
    ),
    player_commands['VOTEMUTE']: Struct(
        'command' / Default(PlayerCommands, 'VOTEMUTE'),
        'id' / Int16ul
    ),
    player_commands['LOCALPING']: Struct(
        'command' / Default(PlayerCommands, 'LOCALPING'),
        'auth' / Int32ul
    )
}

server = {
    server_commands['LOGIN']: Struct(
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
            'status' / Int8ub,
            'level' / Int8ub,
            'name' / Text,
            'type' / ShipTypes,
            'team' / Int16ul,
            'posX' / CoordX,
            'posY' / CoordY,
            'rot' / Rotation,
            'flag' / Int16ul,
            'upgrades' / Int8ub
        ))
    ),
    server_commands['BACKUP']: Struct(
        'command' / Default(ServerCommands, 'BACKUP')
    ),
    server_commands['PING']: Struct(
        'command' / Default(ServerCommands, 'PING'),
        'clock' / Int32ul,
        'num' / Int32ul
    ),
    server_commands['PING_RESULT']: Struct(
        'command' / Default(ServerCommands, 'PING_RESULT'),
        'ping' / Int16ul,
        'playerstotal' / Int32ul,
        'playersgame' / Int32ul
    ),
    server_commands['ACK']: Struct(
        'command' / Default(ServerCommands, 'ACK')
    ),
    server_commands['ERROR']: Struct(
        'command' / Default(ServerCommands, 'ERROR'),
        'error' / Int8ub
    ),
    server_commands['COMMAND_REPLY']: Struct(
        'command' / Default(ServerCommands, 'COMMAND_REPLY'),
        'type' / Int8ub,
        'text' / TextBig
    ),
    server_commands['PLAYER_NEW']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_NEW'),
        'id' / Int16ul,
        'status' / Int8ub,
        'name' / Text,
        'type' / ShipTypes,
        'team' / Int16ul,
        'posX' / CoordX,
        'posY' / CoordY,
        'rot' / Rotation,
        'flag' / Int16ul,
        'upgrades' / Int8ub
    ),
    server_commands['PLAYER_LEAVE']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_LEAVE'),
        'id' / Int16ul
    ),
    server_commands['PLAYER_UPDATE']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_UPDATE'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'keystate' / Int8ub,
        'upgrades' / Int8ub,
        'posX' / Coord24,
        'posY' / Coord24,
        'rot' / Rotation,
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
            'type' / Int8ub,
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
        'rot' / Rotation,
        'upgrades' / Int8ub
    ),
    server_commands['PLAYER_FLAG']: Struct(
        'command' / Default(ServerCommands, 'PLAYER_FLAG'),
        'id' / Int16ul,
        'flag' / Int16ul
    ),
    server_commands['PLAYER_HIT']: Struct(
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
        'command' / Default(ServerCommands, 'EVENT_REPEL'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'posX' / CoordX,
        'posY' / CoordY,
        'rot' / Rotation,
        'speedX' / Speed,
        'speedY' / Speed,
        'energy' / HealthEnergy,
        'energyRegen' / Regen,
        'players' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'keystate' / Int8ub,
            'posX' / CoordX,
            'posY' / CoordY,
            'rot' / Rotation,
            'speedX' / Speed,
            'speedY' / Speed,
            'energy' / HealthEnergy,
            'energyRegen' / Regen,
            'playerHealth' / HealthEnergy,
            'playerHealthRegen' / Regen
        )),
        'mobs' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'type' / Int8ub,
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
        'rot' / Rotation,
        'speedX' / Speed,
        'speedY' / Speed,
        'energy' / HealthEnergy,
        'energyRegen' / Regen,
    ),
    server_commands['EVENT_BOUNCE']: Struct(
        'command' / Default(ServerCommands, 'EVENT_BOUNCE'),
        'clock' / Int32ul,
        'id' / Int16ul,
        'keystate' / Int8ub,
        'posX' / CoordX,
        'posY' / CoordY,
        'rot' / Rotation,
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
        'type' / Int8ub,
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
        'type' / Int8ub,
        'posX' / Float32b,
        'posY' / Float32b
    ),
    server_commands['MOB_DESPAWN']: Struct(
        'command' / Default(ServerCommands, 'MOB_DESPAWN'),
        'id' / Int16ul,
        'type' / Int8ub
    ),
    server_commands['MOB_DESPAWN_COORDS']: Struct(
        'command' / Default(ServerCommands, 'MOB_DESPAWN_COORDS'),
        'id' / Int16ul,
        'type' / Int8ub,
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
        'data' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'score' / Int32ul,
            'level' / Int8ub
        )),
        'rankings' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'x' / Int8ub,
            'y' / Int8ub
        ))
    ),
    server_commands['SCORE_DETAILED']: Struct(
        'command' / Default(ServerCommands, 'SCORE_DETAILED'),
        'scores' / PrefixedArray(Int8ub, Struct(
            'id' / Int16ul,
            'level' / Int8ub,
            'score' / Int32ul,
            'kills' / Int16ul,
            'deaths' / Int16ul,
            'damage' / Float32b,
            'ping' / Int16ul
        ))
    ),
    server_commands['SCORE_DETAILED_CTF']: Struct(
        'command' / Default(ServerCommands, 'SCORE_DETAILED_CTF'),
        'scores' / PrefixedArray(Int8ub, Struct(
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

def build_player_command(command, contents):
    id = player_commands[command]
    return player[id].build(contents)

def decode_server_command(command):
    id = ord(command[0])
    #name = server_commands.keys()[server_commands.values().index(id)]
    #print("Parsing Command ID: {}, Name: {}".format(id, name))
    return server[id].parse(command)