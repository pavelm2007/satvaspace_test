from websocket import create_connection

ws = create_connection("ws://localhost:8080/ws")
cid = ws.recv()
print("Connection established with ID {}".format(cid))
while True:
    try:
        msg = input("Message: ")
        b_msg = bytes(msg, 'utf-8')
        ws.send_binary("{}:{}".format(cid, msg))
    except KeyboardInterrupt:
        ws.close()
        print("Connection closed")
        exit(0)