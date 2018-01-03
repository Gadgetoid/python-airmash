from . import packets
from .player import Player
from .mob import Mob
from . import games
import websocket

class Client:
    def __init__(self):
        self._handlers = {}
        self.players = {}
        self.projectiles = {}
        self.player_id = None
        self.websocket = None
        self._login_name = None
        self._login_flag = None
        self.connected = False
        self._key_seq = 0

    def on(self, key, handler=None):
        def decorate(handler):
            self._handlers[key] = handler

        if handler is None:
            return decorate
        else:
            decorate(handler)

    def _on_open(self, ws):
        self._debug_print(packets.DEBUG_INFO, "### Opened ###")
        cmd = packets.build_player_command('LOGIN',
            protocol=games.get_protocol(),
            name=self._login_name,
            session='none',
            horizonX=int(1920 / 2),
            horizonY=int(1920 / 2),
            flag=self._login_flag
        )
        self.send(cmd)

    def _on_close(self, ws):
        self.connected = False
        self._debug_print(packets.DEBUG_INFO, "### closed ###")

    def _on_message(self, ws, message):
        self.process_message(
            packets.decode_server_command(message))

    def _on_error(self, ws, error):
        self._debug_print(packets.DEBUG_ERROR, error)

    @property
    def player(self):
        return self.players[self.player_id]

    def _debug_print(self, level, text):
        print("{}: {}".format(packets.DEBUG_TEXT[level], text))

    def _chat_print(self, text):
        print(text)

    def _call_handler(self, message):
        handler = self._handlers.get(message.command, None)
        if handler is not None and callable(handler):
            handler(self, message)

    def connect(self, name='Test', flag='GB', region='eu', room='ffa1', enable_trace=False):
        self._login_name = name
        self._login_flag = flag

        game_host = games.get_url(region, room)

        websocket.enableTrace(enable_trace)
        self.websocket = websocket.WebSocketApp(game_host,
            subprotocols=['binary'],
            on_message = self._on_message,
            on_error = self._on_error,
            on_close = self._on_close,
            on_open = self._on_open)

        self.websocket.run_forever(origin = 'https://airma.sh')

    def send(self, command):
        self.websocket.send(command, opcode=websocket.ABNF.OPCODE_BINARY)

    def process_message(self, message):
        if message.command == 'PING':
            cmd = packets.build_player_command('PONG', num=message.num)
            self.send(cmd)
            return self._call_handler(message)

        if message.command == 'ERROR':
            error_type, error_text = packets.error_types[message.error]
            self._debug_print(packets.DEBUG_INFO, "Server: [{} ({})] {}".format(message.error, error_type, error_text))
            return self._call_handler(message)

        if message.command == 'GAME_SPECTATE':
            return self._call_handler(message)

        if message.command == 'LOGIN':
            self.player_id = message.id
            self._debug_print(packets.DEBUG_INFO, "Your ID: {}".format(self.player_id))
            last_id = ''
            for player in message.players:
                self.players[player.id] = Player(player.id, player)
                last_id = player.id

            self.players[self.player_id].update(message)

            cmd = packets.build_player_command('SCOREDETAILED')
            self.send(cmd)

            self.connected = True
            return self._call_handler(message)

        if message.command == 'SERVER_MESSAGE':
            self._chat_print(u"Server: [{}] {}".format(message.type, message.message))
            return self._call_handler(message)

        if message.command == 'CHAT_PUBLIC':
            player = self.players[message.id]
            self._chat_print(u"Public Chat: [{}] {}".format(player.name, message.text))
            return self._call_handler(message)

        if message.command == 'CHAT_TEAM':
            player = self.players[message.id]
            self._chat_print(u"Team Chat: [{}] {}".format(player.name, message.text))
            return self._call_handler(message)

        if message.command == 'CHAT_WHISPER':
            w_from = self.players[message.id]
            w_to = self.players[message.to]
            self._chat_print(u"Whisper: [{}] {}".format(w_from.name, message.text))
            return self._call_handler(message)

        if message.command == 'SCORE_BOARD':
            for player in message.data:
                self.players[player.id].update(player)
            for player in message.rankings:
                self.players[player.id].update(player)
            return self._call_handler(message)

        if message.command in ['SCORE_DETAILED', 'SCORE_DETAILED_CTF', 'SCORE_DETAILED_BTR']:
            for score in message.scores:
                if score.id in self.players:
                    self.players[score.id].update(score)
            return self._call_handler(message)

        if message.command == 'PLAYER_HIT':
            # Update the health and healthRegen of hit player(s)
            projectile = None
            if message.id in self.projectiles:
                projectile = self.projectiles[message.id]
                for player in message.players:
                    self.players[player.id].update(player)
                    if projectile.owner is not None:
                        self._debug_print(packets.DEBUG_ACTION, u"{} hit by {}'s {}".format(self.players[player.id].name, projectile.owner.name, projectile.type))
                    else:
                        self._debug_print(packets.DEBUG_ACTION, u"{} hit by {}".format(self.players[player.id].name, projectile.type))
            return self._call_handler(message)

        if message.command in ['EVENT_STEALTH', 'EVENT_REPEL', 'EVENT_BOOST', 'EVENT_BOUNCE', 'SCORE_UPDATE', 'PLAYER_LEVEL', 'PLAYER_TYPE', 'PLAYER_FIRE', 'PLAYER_RESPAWN', 'PLAYER_UPDATE']:

            # All of these commands trigger some change to the player state, so handle them together for now
            if message.id in self.players:
                self.players[message.id].update(message)
            else:
                self._debug_print(packets.DEBUG_WARNING, u"Players missing ID: {} for command: {}".format(message.id, message.command))
            player = self.players[message.id]

            if message.command == 'PLAYER_FIRE':
                for projectile in message.projectiles:
                    self._debug_print(packets.DEBUG_ACTION, u"New projectile of type {}".format(projectile.type))
                    self.projectiles[projectile.id] = Mob(projectile.id, self.players[message.id], projectile)
                return self._call_handler(message)

            if message.command == 'EVENT_STEALTH':
                #self._debug_print("Player {} has gone into stealth!".format(player.name))
                return self._call_handler(message)

            # These commands trigger an update to multiple other self.players and have a `.self.players` array
            if message.command in ['EVENT_REPEL', 'PLAYER_HIT']:
                for player in message.players:
                    self.players[player.id].update(player)
                
                # Handle self.projectiles hijacked by repel
                if message.command == 'EVENT_REPEL':
                    self._debug_print(packets.DEBUG_ACTION, u"{} uses repel. {} self.players and {} self.projectiles repelled.".format(self.players[message.id].name, len(message.players), len(message.mobs)))
                    for projectile in message.mobs:
                        if projectile.id in self.projectiles:
                            self.projectiles[projectile.id].update(projectile, new_owner=self.players[message.id])
                        else:
                            self.projectiles[projectile.id] = Mob(projectile.id, self.players[message.id], projectile)
                return self._call_handler(message)

            return self._call_handler(message)

        if message.command == 'PLAYER_KILL':
            killer = self.players[message.killer].name
            killed = self.players[message.id].name
            self._debug_print(packets.DEBUG_ACTION, u"{} killed by {} at ({}, {})".format(killed, killer, message.posX, message.posY))
            return self._call_handler(message)

        if message.command == 'PLAYER_LEAVE':
            self._debug_print(packets.DEBUG_ACTION, u"{} left".format(self.players[message.id].name))
            self.players[message.id].online = False
            return self._call_handler(message)

        if message.command == 'PLAYER_NEW':
            self.players[message.id] = Player(message.id, message)
            self._debug_print(packets.DEBUG_ACTION, u"{} joined".format(self.players[message.id].name))
            return self._call_handler(message)

        if message.command == 'PLAYER_POWERUP':
            # Just has type and duration!? But no player id.
            # Does this mean we've picked up a powerup?
            return self._call_handler(message)

        if message.command == 'PLAYER_UPGRADE':
            # Again, no player id.
            # Does this relate to the current player?
            return self._call_handler(message)

        if message.command == 'EVENT_LEAVEHORIZON':
            # Not sure how to interpret this yet
            return self._call_handler(message)

        if message.command == 'PING_RESULT':
            # This returns total self.players, and self.players playing I think,
            # plus a uint16 "ping" value
            return self._call_handler(message)

        # Mobs are missiles. But are they also upgrade crates and powerups?
        if message.command in ['MOB_UPDATE', 'MOB_UPDATE_STATIONARY']:
            self._debug_print(packets.DEBUG_ACTION, u"Mob update of type {}".format(message.type))
            if message.id in self.projectiles:
                self.projectiles[message.id].update(message)
            else:
                self._debug_print(packets.DEBUG_INFO, u"Mob type of {} does not exist? {}".format(message.type, message.id))
                self.projectiles[message.id] = Mob(message.id, None, message)
            return self._call_handler(message)

        if message.command in ['MOB_DESPAWN', 'MOB_DESPAWN_COORDS']:
            if message.id in self.projectiles:
                self.projectiles[message.id].update(message)
                self.projectiles[message.id].despawn()
            return self._call_handler(message)

        self._debug_print(packets.DEBUG_WARNING, u"Unhandled command: {}".format(message.command))

    def login(self, name, horizon, protocol=4, session='none', flag='GB'):
        """Login to server
        
        :param name: player name, 0-255 chars utf-8
        :param horizon: player horizon, tuple of (x, y)
        :param protocol: protocol (default 4)
        :param session: session token (default none)
        :param flag: two-letter country code of flag (default GB)
        
        """
        packet = packets.build_player_command('LOGIN',
            protocol=protocol,
            name=name,
            session=session,
            horizonX=horizon[0],
            horizonY=horizon[1],
            flag=flag
        )
        self.send(packet)

    def horizon(self, x, y):
        """Update server with x/y screen resolution
        
        :param x: horizontal screen (viewport) resolution divided by 2
        :param y: vertical screen resolution divided by 2
        
        """
        packet = packets.build_player_command('HORIZON', horizonX=x, horizonY=y)
        self.send(packet)

    def pong(self, num):
        """Response to a server ping
        
        :param num: num value from server ping packet

        """
        packet = packets.build_player_command('PONG', num=num)
        self.send(packet)

    def command(self, command, data):
        """Send a command to the server

        :param command: text denoting command
        :param data: text for additional data

        """
        packet = packets.build_player_command('COMMAND',
            com=command,
            data=data
        )
        self.send(packet)

    def key(self, key, state):
        packet = packets.build_player_command('KEY', seq=self._key_seq, key=key, state=state)
        self.send(packet)
        self._key_seq += 1

    def spectate(self, player):
        """Spectate a player

        :param player: player to spectate

        """
        if not isinstance(player, Player):
            raise ValueError("player must be an instance of Player")

        self.command("spectate", str(player.id))

    def chat(self, text):
        """Send a chat message

        :param text: chat text- 0 to 255 chars

        """
        packet = packets.build_player_command('CHAT', text=text)
        self.send(packet)
    
    def whisper(self, player, text):
        """Send a whisper

        :param player: player to whisper
        :param text: text to send- 0 to 255 chars

        """
        if not isinstance(player, Player):
            raise ValueError("player must be an instance of Player")

        packet = packets.build_player_command('WHISPER',
            id=player.id,
            text=text
        )
        self.send(packet)

    def teamchat(self, text):
        """Send team chat

        :param text: text to send- 0 to 255 chars

        """
        packet = packets.build_player_command('TEAMCHAT', text=text)
        self.send(packet)

    def say(self, text):
        """Send local message

        :param text: text to say- 0 to 255 chars

        """
        if not isinstance(player, Player):
            raise ValueError("player must be an instance of Player")

        packet = packets.build_player_command('SAY', text=text)
        self.send(packet)

    def emote(self, emote):
        if emote not in packets.emotes:
            raise ValueError("invalid emote")

        self.say(':{}:'.format(emote))