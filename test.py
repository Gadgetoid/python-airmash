import packets
import websocket
import thread
import time

def on_message(ws, message):
    command = packets.decode_server_command(message)
    #print(command)
    if command.command == 'PING':
        print(command)
        print("Achknowledging PING")
        cmd = packets.build_player_command('PONG', dict(num=command.num))
        ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### Opened ###")
    cmd = packets.build_player_command('LOGIN', dict(
        protocol=4,
        name='test',
        session='none',
        horizonX=1024 / 2,
        horizonY=768 / 2,
        flag='en'
    ))
    print("Command length: {}".format(len(cmd)))
    ws.send(cmd, opcode=websocket.ABNF.OPCODE_BINARY)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(packets.SERVER_ADDR,
        subprotocols=['binary'],
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        on_open = on_open)
    ws.run_forever(origin = 'https://airma.sh')
