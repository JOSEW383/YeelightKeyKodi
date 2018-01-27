import re
import socket
from time import sleep
from time import strftime
from ast import literal_eval
import xbmc
import sys
#-------------------------------------------------------------------------
#List of light bulbs
bulb1 = "192.168.5.110"
bulb2 = "192.168.5.111"
bulb3 = "192.168.5.112"
bulb4 = "192.168.5.113"
bulbs=[bulb1,bulb2,bulb3,bulb4]

port=55443

#List of colors
white=16777215
blue=255
green=65280
red=16711680
pink=16711935
yellow=16776960
turquoise=65535
film=9599999

colors=[blue,green,red,pink,yellow,turquoise]

#-------------------------------------------------------------------------
#Methods of yeelight

def get_param_value(data, info):
    dictionary = literal_eval(data[0])
    value = dictionary["result"]
    if info == "power":
        return value[0]
    elif info == "bright":
        return value[1]
    elif info == "rgb":
        return value[2]
    else:
        return "error"

#info= power / bright / rgb
def get_info(ip,info):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(2)
        tcp_socket.connect((ip, int(port)))
        tcp_socket.send("{\"id\":" + ip + ", \"method\":\"get_prop\", \"params\":[\"power\", \"bright\", \"rgb\"]}\r\n")
        data = tcp_socket.recvfrom(2048)
        tcp_socket.close()
        return get_param_value(data,info)
    except Exception as e:
        return "empty"

def operate_on_bulb(ip, method, params):
	try:
		tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_socket.settimeout(2)
		print "Send to ",ip, port ,"..."
		tcp_socket.connect((ip, int(port)))

		#msg2="{\"id\": 192.168.4.234, \"method\": \"set_rgb\", \"params\":[\"65280\", \"sudden\", 500]}\r\n"

		msg="{\"id\":" + str(ip) + ",\"method\":\""
		msg += method + "\",\"params\":[" + params + "]}\r\n"

		tcp_socket.send(msg)
		tcp_socket.close()
	except Exception as e:
		print "An error has ocurred:", e

def set_rgb(ip, color):
    #white 16777215 blue 255 green 65280 red 16711680 pink 16711935 yellow 16776960 turquoise 65535
    params=",\"smooth\",500"
    operate_on_bulb(ip, "set_rgb", str(color)+params)

def set_bright(ip, bright):
    params=",\"smooth\",500"
    operate_on_bulb(ip, "set_bright", str(bright)+params)
    #effect (str)  The type of effect. Can be "smooth" or "sudden".
    #Minimun of bright is 1!!

def set_color_temp(ip):
    operate_on_bulb(ip,"set_color_temp","")
    #Parameters:	degrees (int)  The degrees to set the color temperature to (1700 _ 6500).

def toggle(ip):
    operate_on_bulb(ip,"toggle","")

def turn_on(ip):
    params="\"on\",\"smooth\",500"
    operate_on_bulb(ip,"set_power",params)

def turn_off(ip):
    params="\"off\",\"smooth\",500"
    operate_on_bulb(ip,"set_power",params)

#-------------------------------------------------------------------------
#Other Methods

def change_state(mode):
    state = []
    try:
        data  = open("/storage/.kodi/addons/script.YeelightKey/data.txt", "r")
    except Exception as e:
        data  = open("/storage/.kodi/addons/script.YeelightKey/data.txt", "w+")
        data.write("notOpen\n")
        data.write("normal")
        data.close()
    state.append(data.readline())
    state.append(data.readline())
    data.close()

    if mode == "data1":
        thelist = [0,"isOpen\n","notOpen\n","isOpen\n","isOpen\n","isOpen\n"]
    elif mode == "data2":
        thelist = [1,"normal","isOpen\n","film","isOpen\n","normal"]

    if state[thelist[0]] == thelist[1]:
        data  = open("/storage/.kodi/addons/script.YeelightKey/data.txt", "w")
        data.write(thelist[2])
        data.write(thelist[3])
        data.close()
    else:
        data  = open("/storage/.kodi/addons/script.YeelightKey/data.txt", "w")
        data.write(thelist[4])
        data.write(thelist[5])
        data.close()

def read_data(mode):
    state = []
    data  = open("/storage/.kodi/addons/script.YeelightKey/data.txt", "r")
    state.append(data.readline())
    state.append(data.readline())
    data.close()

    #In thelist the var1 is the mode-1 and the var2 is the modes in file date
    if mode == "data1":
        thelist = [0,"isOpen\n"]
    elif mode == "data2":
        thelist = [1,"normal"]

    if state[thelist[0]] == thelist[1]:
        return True
    else:
        return False

def change_bright():
    info = get_info(bulb1,"bright")
    if info == "1":
        for i in range(4):
            set_bright(bulbs[i],25)
    elif info == "25":
        for i in range(4):
            set_bright(bulbs[i],50)
    elif info == "50":
        for i in range(4):
            set_bright(bulbs[i],75)
    elif info == "75":
        for i in range(4):
            set_bright(bulbs[i],100)
    elif info == "100":
        for i in range(4):
            set_bright(bulbs[i],1)
    else:
        for i in range(4):
            set_bright(bulbs[i],100)

def change_color():
    info = get_info(bulb1,"rgb")
    if info == "16777215":
        for i in range(4):
            set_rgb(bulbs[i],255)
    elif info == "255":
        for i in range(4):
            set_rgb(bulbs[i],65280)
    elif info == "65280":
        for i in range(4):
            set_rgb(bulbs[i],16711680)
    elif info == "16711680":
        for i in range(4):
            set_rgb(bulbs[i],16711935)
    elif info == "16711935":
        for i in range(4):
            set_rgb(bulbs[i],16776960)
    elif info == "16776960":
        for i in range(4):
            set_rgb(bulbs[i],65535)
    else:
        for i in range(4):
            set_rgb(bulbs[i],16777215)

def number_bulbs():
    info = get_info(bulb4,"power")
    if info == "empty":
        return 3
    else:
        return 4

#-------------------------------------------------------------------------
#Voids witch all light bulbs

def turn_on_all():
    turn_on(bulb1)
    turn_on(bulb2)
    turn_on(bulb3)
    turn_on(bulb4)

def turn_off_all():
    turn_off(bulb1)
    turn_off(bulb2)
    turn_off(bulb3)
    turn_off(bulb4)

#-------------------------------------------------------------------------
#Scenes

def scene1():
    change_state("data1")
    turn_on_all()
    nbulbs = number_bulbs()
    for i in range(nbulbs):
        set_bright(bulbs[i],100)
    while not read_data("data1"):
        for i in range(6):
            set_rgb(bulb1, colors[i%6])
            set_rgb(bulb2, colors[(i+1)%6])
            set_rgb(bulb3, colors[(i+2)%6])
            if nbulbs == 4:
                set_rgb(bulb4, colors[(i+3)%6])
            if read_data("data1"):
                break
            sleep(1)
    for i in range(nbulbs):
        set_rgb(bulbs[i],white)

def default_scene():
    change_state("data2")
    nbulbs = number_bulbs()
    if nbulbs == 3:
        turn_off_all()
        turn_on(bulb1)
        if read_data("data2"):
            set_rgb(bulb1,white)
            set_bright(bulb1,50)
        else:
            set_rgb(bulb3,film)
            set_bright(bulb3,20)
    else:
        turn_off_all()
        turn_on(bulb4)
        if read_data("data2"):
            set_rgb(bulb4,white)
            set_bright(bulb4,100)
        else:
            set_rgb(bulb4,film)
            set_bright(bulb4,50)

#-------------------------------------------------------------------------
#MAIN OF YEELIGHTPRO
#List of conditions: http://kodi.wiki/view/List_of_boolean_conditions
#xbmc.executebuiltin('Action(reloadkeymaps)') #To reload keymaps (or set <r>reloadkeymaps</r> in keymaps.xml)
x = sys.argv[1]
if x == '0':
    turn_off_all()
elif x == '1':
    toggle(bulb1)
elif x == '2':
	toggle(bulb2)
elif x == '3':
	toggle(bulb3)
elif x == '4':
	toggle(bulb4)
elif x == '5':
    turn_on_all()
elif x == '6':
    change_bright()
elif x == '7':
    change_color()
elif x == '8':
    default_scene()
elif x == '9':
    scene1()
elif x == 'pageup':
    if xbmc.getCondVisibility("Window.IsActive(pictures)"):
        xbmc.executebuiltin("Action(ZoomIn)")
    else:
        xbmc.executebuiltin("Action(PageUp)")
elif x == 'pagedown':
    if xbmc.getCondVisibility("Window.IsActive(pictures)"):
        xbmc.executebuiltin("Action(ZoomOut)")
    else:
        xbmc.executebuiltin("Action(PageDown)")
else:
    xbmc.executebuiltin("Notification(YeelightKey,Scene not found: "+x+")")
