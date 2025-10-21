import socket

maya_host = "127.0.0.1"
maya_port = 7001  # same as in Maya

code = "import maya.cmds as cmds; cmds.polyCube()\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((maya_host, maya_port))
s.send(code.encode("utf-8"))
s.close()


