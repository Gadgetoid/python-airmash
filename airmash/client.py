from airmash import packets
from airmash.player import Player

class Client:
    def __init__(self):
        pass

    def login(self, name, horizon, protocol=4, session='none', flag='GB'):
        """Login to server
        
        :param name: player name, 0-255 chars utf-8
        :param horizon: player horizon, tuple of (x, y)
        :param protocol: protocol (default 4)
        :param session: session token (default none)
        :param flag: two-letter country code of flag (default GB)
        
        """
        packet = packets.build_player_command('LOGIN', dict(
            protocol=protocol,
            name=name,
            session=session,
            horizonX=horizon[0],
            horizonY=horizon[1],
            flag=flag
        ))
        self.send(packet)

    def horizon(self, x, y):
        """Update server with x/y screen resolution
        
        :param x: horizontal screen (viewport) resolution divided by 2
        :param y: vertical screen resolution divided by 2
        
        """
        packet = packets.build_player_command('HORIZON', dict(horizonX=x, horizonY=y))
        self.send(packet)

    def pong(self, num):
        """Response to a server ping
        
        :param num: num value from server ping packet

        """
        packet = packets.build_player_command('PONG', dict(num=num))
        self.send(packet)

    def command(self, command, data):
        """Send a command to the server

        :param command: text denoting command
        :param data: text for additional data

        """
        packet = packets.build_player_command('COMMAND', dict(
            com=command,
            data=data
        ))
        self.send(packet)

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
        packet = packets.build_player_command('CHAT', dict(
            text=text
        ))
        self.send(packet)
    
    def whisper(self, player, text):
        """Send a whisper

        :param player: player to whisper
        :param text: text to send- 0 to 255 chars

        """
        if not isinstance(player, Player):
            raise ValueError("player must be an instance of Player")

        packet = packets.build_player_command('WHISPER', dict(
            id=player.id,
            text=text
        ))
        self.send(packet)

    def teamchat(self, text):
        """Send team chat

        :param text: text to send- 0 to 255 chars

        """
        packet = packets.build_player_command('TEAMCHAT', dict(
            text=text
        ))
        self.send(packet)

    def say(self, text):
        """Send local message

        :param text: text to say- 0 to 255 chars

        """
        if not isinstance(player, Player):
            raise ValueError("player must be an instance of Player")

        packet = packets.build_player_command('SAY', dict(
            text=text
        ))
        self.send(packet)

    def emote(self, emote):
        if emote not in packets.emotes:
            raise ValueError("invalid emote")

        self.say(':{}:'.format(emote))

    def send(self, data):
        raise RuntimeError("Must implement a send method!")