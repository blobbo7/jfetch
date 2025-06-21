# jfetch 0.1
# open source babyyyyyyyyyyyyyyyyyy

import subprocess
import psutil
import platform
import sys
import os

def resource_path(relative_path):
    """ Get path to resource in both PyInstaller bundle and normal run """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

width = 0

disname = "grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2 | tr -d '\"'"
cpuinfo = "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs"
gpyou = "lspci | grep -i 'vga' | cut -d ':' -f3- | xargs"

mem = psutil.virtual_memory()
used = mem.used // (1024 * 1024)
total = mem.total // (1024 * 1024)

usage = psutil.disk_usage('/')
used = usage.used // (1024 ** 3)
total = usage.total // (1024 ** 3)

fill=' '

user = subprocess.check_output("whoami", shell=True, text=True)
hostname = subprocess.check_output("hostname", shell=True, text=True)
distro = subprocess.check_output(disname, shell=True, text=True)
uptime = subprocess.check_output("uptime -p", shell=True, text=True)
de = subprocess.check_output("echo $DESKTOP_SESSION", shell=True, text=True)
shell = subprocess.check_output("echo $SHELL", shell=True, text=True)
cpu = subprocess.check_output(cpuinfo, shell=True, text=True)
gpu = subprocess.check_output(gpyou, shell=True, text=True)



print(width*fill, end=''); print("\033[34m user: \033[0m", end=''); print(user, end='') #user
print(width*fill, end=''); print("\033[34m hostname: \033[0m", end=''); print(hostname, end='') #hostname
print(width*fill, end=''); print("\033[34m distro: \033[0m", end=''); print(distro, end='') #distro
print(width*fill, end=''); print("\033[34m uptime:\033[0m", end=''); print(uptime.replace('up', ''), end='') #uptime
print(width*fill, end=''); print("\033[34m de: \033[0m", end=''); print(de, end='') #de
print(width*fill, end=''); print("\033[34m shell: \033[0m", end=''); print(shell, end='') #shell
print(width*fill, end=''); print("\033[34m memory: \033[0m", end=''); print(f"{used} MB/{total} MB", end='') #mem
print() #hacky fix
print(width*fill, end=''); print("\033[34m disk: \033[0m", end=''); print(f"{used}GB/{total}GB") #disk
print(width*fill, end=''); print("\033[34m cpu: \033[0m", end=''); print(cpu, end='') #cpu
print(width*fill, end=''); print("\033[34m gpu: \033[0m", end=''); print(gpu, end='') #gpu


#ascii

print() #break

idcmd = "grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '\"'"

id = subprocess.check_output(idcmd, shell=True, text=True)

id2 = id.strip('\n')

arg = None


for a in sys.argv[1:]:
    if a.startswith('--'):
        arg = a[2:]  # remove --
        break

if arg:
    with open("ascii/" + arg + ".txt", "r") as file:
        for line in file:
            print(line, end='')
        
else:
    with open("ascii/" + id2 + ".txt", "r") as file:
        for line in file:
            print(line, end='')
