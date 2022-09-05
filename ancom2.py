import time
import pysftp
from datetime import datetime
import PIL.ImageGrab
import win32gui, win32con
import pyautogui

def ancom():
    hwnd = win32gui.FindWindow(None, 'TDA-9 ')
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, 9)
    rect = win32gui.GetWindowRect(hwnd)
    time.sleep(1)
    pyautogui.click(rect[0]+25,rect[1]+50)
    

def connect():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    with pysftp.Connection("10.13.14.64", username="root", password="791", cnopts=cnopts) as sftp:
        print("Connection succesfully stablished.")
        sftp.get('/var/log/asterisk/full', 'full.log')
        print("Logs copied.")

def date2int(s):
    d = 10000000000*int(s.split('-')[0])+100000000*int(s.split('-')[1])+1000000*int(s.split(' ')[0].split('-')[2])+10000*int(s.split(' ')[1].split(':')[0])+100*int(s.split(':')[1])+int(s.split(':')[2])
    return d

def read(n, e):
    file = open("full.log")
    for i, line in enumerate(file):
        if line.find('[') == 0:
            d = date2int(line.split(']')[0].split('[')[1])
        if d >= n and d <= e:
            if line.find("Detected inband DTMF") != -1:
                print("INBAND DTMF")
            elif line.find("Creating END DTMF Frame") != -1:
                print("RFC2833")
            elif line.find("Signal=") != -1:
                print("SIP-INFO DTMF")
            if line.find("DTMF end '") > 1:
                print(line.split("'")[1].split(";")[0])
        if d > e:
            break;
    print("Done scanning.")
    file.close()

def main():
    #core set verbose 5, core set debug 5, pjsip set logger on
    n = int(datetime.now().strftime('%Y%m%d%H%M%S'))
    print("start", n)
    ancom()
    print("Waiting for Ancom...")
    time.sleep(90)
    e = int(datetime.now().strftime('%Y%m%d%H%M%S'))
    print("end", e)
    
    print("Getting logs...")
    connect()
    read(n, e)

if __name__ == "__main__":
    main()