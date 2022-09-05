import os, time
import shutil, psutil
import threading
from subprocess import Popen
import pywinauto

def backup(reset):
    accounts = []
    with open('auths.txt') as file:
        lines = file.readlines()
    for l in lines:
        accounts.append(l.strip().split(' '))
    if reset == True:
        if os.path.exists('MicroSIP0'):
            shutil.rmtree('MicroSIP0')
        shutil.copytree('MicroSIP', 'MicroSIP0')
    return accounts

def gen(accounts):
    import warnings
    warnings.filterwarnings("ignore")
    app = pywinauto.Application().start('MicroSIP0/microsip.exe')
    for proc in psutil.process_iter():
        if proc.name() == "microsip.exe":
            app = pywinauto.Application().connect(process=proc.pid)
            break
    micro = app.MicroSIP
    menu = micro["Menu"].wrapper_object()
    first = True
    for a in accounts:
        micro.get_focus()
        menu.click()
        for i in range(8):
            menu.send_keystrokes('{VK_UP}')
        if first == True:
            menu.send_keystrokes('{VK_UP}')
            first = False
        menu.send_keystrokes('{ENTER}')   
        acc = pywinauto.Application().connect(handle=pywinauto.Desktop().Account.handle).Dialog
        acc.get_focus()
        acc.Edit2.set_text("192.168.1.18")
        acc.Edit4.set_text(a[0])
        acc.Edit5.set_text("192.168.1.18")
        acc.Edit7.set_text(a[1])
        acc["Publish Presence"].wrapper_object().click()
        acc["Save"].wrapper_object().click()
        if micro.StatusBar.element_info.name == "Incorrect Password":
            print("Invalid account", a)
            acc["Cancel"].wrapper_object().click()
            a[0] = "-"
    micro.close()

def copy(accounts):
    import tempfile
    tempdir = tempfile.mkdtemp()
    print(tempdir)
    for i in range(len(accounts)):
        dir = tempdir+'/MicroSIP'+str(i)
        shutil.copytree('MicroSIP0', dir)
        with open(dir+'/microsip.ini', 'r', encoding='utf-16-le') as file:
            data = file.readlines()
        data[1] = "accountId="+str(i+1)+"\n"
        with open(dir+'/microsip.ini', 'w', encoding='utf-16-le') as file:
            file.writelines(data)
    return tempdir

def call(accounts, tempdir):
    DTMF = '100,1,,2,,3,,4,,5,,6,,7,,8,,9,,*,,#,,,,,,1,,2,,3,,4,,5,,6,,7,,8,,9,,*,,#,,0,,'
    # threads = []
    for i in range(len(accounts)):
        if accounts[i][0] != "-":
            Popen(tempdir+'/MicroSIP'+str(i)+'/microsip.exe '+DTMF)
            # threads.append(threading.Thread(target=tstart,args=(tempdir, i, DTMF)))
    # for t in threads:
        # t.start()
    time.sleep(len(DTMF)/2)
    for i in range(len(accounts)):
        if accounts[i][0] != "-":
            os.system(tempdir+'/MicroSIP'+str(i)+'/microsip.exe /exit')
    time.sleep(0.5)
    shutil.rmtree(tempdir)
    
def tstart(tempdir, i, DTMF):
    Popen(tempdir+'/MicroSIP'+str(i)+'/microsip.exe '+DTMF)

def sshconnect():
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.1.18", 22, "root", "qwaqwa33")
    stdin, stdout, stderr = ssh.exec_command("asterisk -rx 'core show version'")
    print(stdout.read().decode(), stderr.read().decode())
    t = threading.Thread(target=check,args=(ssh, time.time()+200))
    t.start()
        
def check(ssh, tout):
    while time.time() < tout:
        time.sleep(0.5)
        stdin, stdout, stderr = ssh.exec_command("asterisk -rx 'core show channels count'")
        print(stdout.read().decode(), stderr.read().decode())

if __name__ == "__main__":
    reset = False
    accounts = backup(reset)
    if reset: gen(accounts)
    tempdir = copy(accounts)
    sshconnect()
    call(accounts, tempdir)