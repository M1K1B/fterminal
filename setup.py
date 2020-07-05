import os

os.system("clear")

def install():
    os.system("sudo apt install python3-pip")
    os.system("pip3 install geocoder")
    os.system("mkdir tools")
    os.chdir('tools')
    os.system("git clone https://github.com/GouveaHeitor/nipe.git")
    os.chdir('nipe')
    os.system("sudo cpan install Try::Tiny Config::Simple JSON")
    os.system("perl nipe.pl install")
    os.chdir('../..')

print("""
    \033[0;31;40m______ \033[0;37;40m _____                   _             _             _               
    \033[0;31;40m|  ___|\033[0;37;40m|_   _|                 (_)           | |           | |              
    \033[0;31;40m| |_   \033[0;37;40m  | | ___ _ __ _ __ ___  _ _ __   __ _| |   ___  ___| |_ _   _ _ __  
    \033[0;31;40m|  _|  \033[0;37;40m  | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |  / __|/ _ \ __| | | | '_ \ 
    \033[0;31;40m| |    \033[0;37;40m  | |  __/ |  | | | | | | | | | | (_| | |  \__ \  __/ |_| |_| | |_) |
    \033[0;31;40m\_|    \033[0;37;40m  \_/\___|_|  |_| |_| |_|_|_| |_|\__,_|_|  |___/\___|\__|\__,_| .__/ 
                                                                         | |    
                                                                         |_|    
                                                                            \033[0;36;40mv1.0\033[0;37;40m
""")

command = input("Install packages needed for fterminal(yes/no): ")

if command == "yes" or command == "y":
    install()
else:
    print("OK, take care, bye!")
