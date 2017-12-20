from construct import *

SERVER_ADDR = "wss://game-eu-s1.airma.sh/ffa1"

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