from construct import *

DEBUG_INFO = 0
DEBUG_ACTION = 1
DEBUG_WARNING = 2
DEBUG_ERROR = 3

DEBUG_TEXT = ["Info", "Action", "Warning", "Error"]

# JSON API for data about existing games
GAMES_ADDR = "https://airma.sh/games"

SERVER_ADDR = "wss://game-eu-s1.airma.sh/ffa1"

GAME_ADDR = "wss://game-{host}.airma.sh/{room}"

emotes = [
    'tf',
    'pepe',
    'clap',
    'lol',
    'bro',
    'kappa',
    'cry',
    'rage'
]

error_types = {
    1: ('DISCONNECTED', 'Packet flooding detected'),
    2: ('BANNED', 'Packet flooding detected'),
    3: ('BANNED', 'You have been globally banned'),
    4: ('UNKNOWN', 'UNKNOWN'), # Disconnect?
    5: ('RESPAWN', 'Full health and 2 seconds of inactivity required'),
    6: ('DISCONNECTED', 'AFK for more than 10 minutes'),
    7: ('DISCONNECTED', 'You have been kicked out'),
    8: ('DISCONNECTED', 'Invalid login data'),
    9: ('DISCONNECTED', 'Incorrect protocol level'),
    10:('BANNED', 'Account banned'),
    11:('DISCONNECTED', 'Account already logged in'),
    12:('RESPAWN', 'Cannot respawn or change aircraft in a Battle Royale game'),
    13:('ALERT', 'Full health and 2 seconds of inactivity required'),
    20:('INFORMATION', 'Not enough upgrade points'),
    30:('ALERT', 'Chat throttled to prevent spamming'),
    31:('ALERT', 'Flag change too fast'),
    100:('ERROR', 'Unknown command')
}

player_status = {
    'alive': 0,
    'dead': 1
}

PlayerStatus = Enum(Int8ul, **player_status)

# Type 1: Predator single missile
# Type 2: Goliath single big missile
# Type 3: Mohawk rocket
# Type 5: Tornado single-shot
# Type 6: Tornado triple-shot
# Type 7: Prowler single-shot
mob_types = {
    'None': 0,
    'Predator Missile': 1,
    'Goliath Missile': 2,
    'Mohawk Rocket': 3,
    'Upgrade?': 4,
    'Tornado Single Missile': 5,
    'Tornado Triple Missile': 6,
    'Prowler Missile': 7,
    'Shield?': 8,
    'Rampage?': 9
}

MobTypes = Enum(Int8ul, **mob_types)
MissileTypes = MobTypes

ship_types = {
    'Predator': 1,
    'Goliath': 2,
    'Mohawk': 3,
    'Tornado': 4,
    'Prowler': 5
}

ShipTypes = Enum(Int8ul, **ship_types)

message_types = {
    'ALERT': 1,
    'INFO': 2
}

MessageTypes = Enum(Int8ul, **message_types)

player_keys = {
    'UP': 1,
    'DOWN': 2,
    'LEFT': 3,
    'RIGHT': 4,
    'FIRE': 5,
    'SPECIAL': 6
}

PlayerKeys = Enum(Int8ul, **player_keys)

state = {
    'LOGIN': 1,
    'CONNECTING': 2,
    'PLAYING': 3
}

player_commands = {
    'LOGIN': 0,
    'BACKUP': 1,
    'HORIZON': 2,
    'ACK': 5,
    'PONG': 6,
    'KEY': 10,
    'COMMAND': 11,
    'SCOREDETAILED': 12,
    'CHAT': 20,
    'WHISPER': 21,
    'SAY': 22,
    'TEAMCHAT': 23,
    'VOTEMUTE': 24,
    'LOCALPING': 255
}

PlayerCommands = Enum(Int8ul, **player_commands)

server_commands = {
    'LOGIN': 0,
    'BACKUP': 1,
    'PING': 5,
    'PING_RESULT': 6,
    'ACK': 7,
    'ERROR': 8,
    'COMMAND_REPLY': 9,
    'PLAYER_NEW': 10,
    'PLAYER_LEAVE': 11,
    'PLAYER_UPDATE': 12,
    'PLAYER_FIRE': 13,
    'PLAYER_HIT': 14,
    'PLAYER_RESPAWN': 15,
    'PLAYER_FLAG': 16,
    'PLAYER_KILL': 17,
    'PLAYER_UPGRADE': 18,
    'PLAYER_TYPE': 19,
    'PLAYER_POWERUP': 20,
    'PLAYER_LEVEL': 21,
    'GAME_FLAG': 30,
    'GAME_SPECTATE': 31,
    'GAME_PLAYERSALIVE': 32,
    'GAME_FIREWALL': 33,
    'EVENT_REPEL': 40,
    'EVENT_BOOST': 41,
    'EVENT_BOUNCE': 42,
    'EVENT_STEALTH': 43,
    'EVENT_LEAVEHORIZON': 44,
    'MOB_UPDATE': 60,
    'MOB_UPDATE_STATIONARY': 61,
    'MOB_DESPAWN': 62,
    'MOB_DESPAWN_COORDS': 63,
    'CHAT_PUBLIC': 70,
    'CHAT_TEAM': 71,
    'CHAT_SAY': 72,
    'CHAT_WHISPER': 73,
    'CHAT_VOTEMUTEPASSED': 78,
    'CHAT_VOTEMUTED': 79,
    'SCORE_UPDATE': 80,
    'SCORE_BOARD': 81,
    'SCORE_DETAILED': 82,
    'SCORE_DETAILED_CTF': 83,
    'SCORE_DETAILED_BTR': 84,
    'SERVER_MESSAGE': 90,
    'SERVER_CUSTOM': 91
}

ServerCommands = Enum(Int8ul, **server_commands)

class AdapterCoordX(Adapter):
    """Converts X coordinate from a uint16 to the range +-16384"""
    def _encode(self, obj, ctx):
        return int(obj * 2) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 2.0

class AdapterCoordY(Adapter):
    """Converts Y coordinate from a uint16 to the range +-8192"""
    def _encode(self, obj, ctx):
        return (obj * 4) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 4.0

class AdapterRotation(Adapter):
    """Converts rotation from a uint16 to the range 0-10
    In reality only the range 0-2*PI is used AFAIK since this
    value describes the ships rotation in radians"""
    def _encode(self, obj, ctx):
        return int(obj * 6553.6)
    def _decode(self, obj, ctx):
        return obj / 6553.6

class AdapterSpeed(Adapter):
    """Converts speed from a uint16 to the range +-10"""
    def _encode(self, obj, ctx):
        return int(obj * 1638.4) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 1638.4

class AdapterAccel(Adapter):
    """Converts acceleration from a uint16 to the range +-1"""
    def _encode(self, obj, ctx):
        return int(obj * 32768) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 32768.0

class AdapterRegen(Adapter):
    """Converts regen from a uint16 to +-0.032768"""
    def _encode(self, obj, ctx):
        return int(obj * 1e6) + 32768
    def _decode(self, obj, ctx):
        return (obj - 32768) / 1e6

class AdapterHealthEnergy(Adapter):
    """Converts health/energy from a uint8 to 0-1"""
    def _encode(self, obj, ctx):
        return int(obj * 255)
    def _decode(self, obj, ctx):
        return obj / 255

class AdapterCoord24(Adapter):
    """Converts a uint24 to 0-16384
    producing a high-precision X or Y coordinate"""
    def _encode(self, obj, ctx):
        obj = int((obj * 512) + 8388608)
        return ((obj << 16) & 0xff0000) | (obj >> 8)
    def _decode(self, obj, ctx):
        # The 24bit high-precision Coord24 has a really weird byte order
        unpacked = ((obj << 8) & 0xffff00) | (obj >> 16)
        return (unpacked - 8388608) / 512.0

# Define types for various ship telemetry
CoordX = AdapterCoordX(Int16ul)
CoordY = AdapterCoordY(Int16ul)
Coord24 = AdapterCoord24(Int24ul)
Rotation = AdapterRotation(Int16ul)
Speed = AdapterSpeed(Int16ul)
Accel = AdapterAccel(Int16ul)
Regen = AdapterRegen(Int16ul)
HealthEnergy = AdapterHealthEnergy(Int8ub)

# Shorthand for Text and TextBig types used by Airmash
Text = PascalString(Int8ub, encoding='UTF-8')
TextBig = PascalString(Int16ul, encoding='UTF-8')

# Bitfield type for player key state
KeyState = BitStruct(
    None / Padding(2),
    "SPECIAL" / Flag,
    "FIRE" / Flag,
    "RIGHT" / Flag,
    "LEFT" / Flag,
    "DOWN" / Flag,
    "UP" / Flag
)
