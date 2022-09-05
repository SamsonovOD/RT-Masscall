# import socket, time, threading

# chan = ''

# def get(s):
    # while True:
        # try:
            # data = s.recv(1024)
            # print(data.decode())
        # except:
            # pass

# def click_to_call(username, password, local_user, phone_to_dial):
    # s = socket.socket()
    # s.connect(('192.168.1.18',5038))
    # s.settimeout(1)
    # lis = threading.Thread(name="listener", target=get, args=(s,), daemon=True)
    # lis.start()
    # p = "Action: Login\n"
    # p += "ActionID: 1\n"
    # p += "Events: on\n"
    # p += "Username: "+username+"\n"
    # p += "Secret: "+password+"\n"
    # for l in p.split('\n'):
        # s.send((l+'\n').encode())
    # time.sleep(3)
    # p = "Action: Originate\n"
    # p += "ActionID: 2\n"
    # p += "Channel: PJSIP/"+local_user+"/"+local_user+"\n"
    # p += "Exten: "+phone_to_dial+"\n"
    # p += "Context: from-internal\n"
    # p += "Priority: 1\n"
    # for l in p.split('\n'):
        # s.send((l+'\n').encode())
    # p = "Action: CoreShowChannels\n"
    # p += "ActionID: 3\n"
    # for l in p.split('\n'):
        # s.send((l+'\n').encode())
    # time.sleep(10)
    # s.close()

# if __name__=='__main__':
    # click_to_call(username='py_manager',password='managpass',phone_to_dial='100',local_user='101')
   
import time
import asterisk.manager as am
def printresp(response):
    for r in response.response:
        print(r,end="")
    print("")  
    
def handle_event(event, manager):
    ch = event.headers['Channel']
    print(ch)
    manager.unregister_event('Newchannel', handle_event)
    printresp(manager.playdtmf(channel=ch, digit="1"))
    time.sleep(2)
    printresp(manager.playdtmf(channel=ch, digit="2"))
    time.sleep(2)
    printresp(manager.playdtmf(channel=ch, digit="3"))
   
manager = am.Manager()
try:
    try:
        manager.connect('192.168.1.18')
        manager.login('py_manager', 'managpass')
        printresp(manager.originate(channel='PJSIP/102/102', exten='100', context='from-internal', priority='1'))
        manager.register_event('Newchannel', handle_event)
        time.sleep(5)
        manager.logoff()
    except (am.ManagerException, am.ManagerSocketException, am.ManagerAuthException) as e:
        print ("Error connecting to the manager: %s" % e)
        exit()
finally:
    try:
        manager.close()
    except:
        exit()