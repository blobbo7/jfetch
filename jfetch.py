#!/usr/bin/env python3


# jfetch 0.4
# unknown distro safety, better dependencies

import subprocess
import platform
import sys
import os
import re

def resource_path(relative_path):
    """ Get path to resource in both PyInstaller bundle and normal run """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

width = 10

disname = "grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2 | tr -d '\"'"
cpuinfo = "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs"
gpyou = "lspci | grep -i 'vga' | cut -d ':' -f3- | xargs"

def get_memory_info(): #memory
    with open('/proc/meminfo') as f:
        meminfo = {}
        for line in f:
            key, value = line.split(':')
            meminfo[key.strip()] = int(value.strip().split()[0])  # kB

    total = meminfo['MemTotal'] // 1024  # MB
    available = meminfo.get('MemAvailable', meminfo['MemFree']) // 1024  # fallback if needed
    used = total - available
    return used, total

used, total = get_memory_info()

def get_disk_info(path="/"):  #disk info
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize // (1024 ** 3)  # in GB
    free = st.f_bavail * st.f_frsize // (1024 ** 3)
    used = total - free
    return used, total

dused, dtotal = get_disk_info()

fill=' '

user = subprocess.check_output("whoami", shell=True, text=True)
hostname = subprocess.check_output("hostname", shell=True, text=True)
distro = subprocess.check_output(disname, shell=True, text=True)
uptime = subprocess.check_output("uptime -p", shell=True, text=True)
de = subprocess.check_output("echo $DESKTOP_SESSION", shell=True, text=True)
shell = subprocess.check_output("echo $SHELL", shell=True, text=True)
cpu = subprocess.check_output(cpuinfo, shell=True, text=True)
gpu = subprocess.check_output(gpyou, shell=True, text=True)
term = subprocess.check_output("echo $TERM", shell=True, text=True)



ANSI_PATTERN = re.compile(r'(\x1b\[[0-9;]*m)')

def lineprint(line_number, filename="example.txt"): #really weird stuff idk:
    with open(filename, "r", encoding="utf-8") as file:
        active_codes = []
        for current_line, content in enumerate(file, start=1):
            codes = ANSI_PATTERN.findall(content)
            for code in codes:
                if code == '\x1b[0m':
                    active_codes.clear()
                else:
                        active_codes.append(code)

            if current_line == line_number:
                prefix = ''.join(active_codes)
                return f"{prefix}{content.rstrip('\n')}"  # return line without printing



idcmd = "grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '\"'"

id = subprocess.check_output(idcmd, shell=True, text=True)

id2 = id.strip('\n')

arg = None


for a in sys.argv[1:]:
    if a.startswith('--'):
        arg = a[2:]  # remove --
        break

if arg:
    id2 = arg

    if os.path.isfile(resource_path(f"ascii/{arg}.txt")) == False:
        print("distro not found")
        id2 = "poo"

else:
    if os.path.isfile(resource_path(f"ascii/{id2}.txt")) == False:
        print("distro not found")
        id2 = "poo"

print(lineprint(1, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m user: \033[0m", end=''); print(user, end='') #user
print(lineprint(2, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m hostname: \033[0m", end=''); print(hostname, end='') #hostname
print(lineprint(3, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m distro: \033[0m", end=''); print(distro, end='') #distro
print(lineprint(4, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m uptime:\033[0m", end=''); print(uptime.replace('up', ''), end='') #uptime
print(lineprint(5, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m de: \033[0m", end=''); print(de, end='') #de
print(lineprint(6, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m shell: \033[0m", end=''); print(shell, end='') #shell
print(lineprint(7, resource_path(f"ascii/{id2}.txt")), end='');      print(width*fill, end=''); print("\033[34m terminal: \033[0m", end=''); print(term, end='') #term
print(lineprint(8, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m memory: \033[0m", end=''); print(f"{used} MB/{total} MB", end='') #mem
print() #hacky fix
print(lineprint(9, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m disk: \033[0m", end=''); print(f"{dused}GB/{dtotal}GB") #disk
print(lineprint(10, resource_path(f"ascii/{id2}.txt")), end='');       print(width*fill, end=''); print("\033[34m cpu: \033[0m", end=''); print(cpu, end='') #cpu
print(lineprint(11, resource_path(f"ascii/{id2}.txt")), end='');      print(width*fill, end=''); print("\033[34m gpu: \033[0m", end=''); print(gpu, end='') #gpu
print(lineprint(12, resource_path(f"ascii/{id2}.txt")), end='')
print('',end='')
