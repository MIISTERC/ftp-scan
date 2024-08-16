#!/usr/bin/python3
import argparse
import ftplib
import os
from colorama import Fore,Style
import socket
import sys
import re
parser = argparse.ArgumentParser()
parser.add_argument('-t','--target',required=True,help="Enter target ip")
parser.add_argument('-p','--port',required=False,default=21,help="Enter target port")
args = parser.parse_args()
target = args.target
port = args.port
port = int(port)
class scanner:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        timeout_value = 4
        self.ftp = ftplib.FTP(timeout=timeout_value)
    def connect(self):
        try:
            self.ftp.connect(self.ip,self.port)
        except Exception as e:
            print(f"[-] Connection failed , error :-") 
            print(e)
            return False
        return True
    def check_anon_login(self):
        if self.connect():
            try:
                self.ftp.login()
                print(f"[+] Anonymous login is enabled!")
                try:
                    print(f"[+] Trying to list all the files..")
                    print(self.ftp.dir("-a"))
                except Exception as e:
                    print("Error Listing files ,please check manually... error :- ")
                    print(e)
            except Exception as e:
                print(f"[-] Anonymous Login is Disabled.")
class VulnScan():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)
    def grabBanner(self):
        try:
            self.s.connect((self.ip, self.port))
        except Exception as e:
            sys.exit(0)
            
        banner = self.s.recv(1024)
        final = banner.decode('utf-8')
        self.s.close()
        if final.startswith('220'):
            final = final[4:]
        return final
    @staticmethod
    def vuln_check(banner):
        try:
            with open('ftp-vuln.db', 'r') as fp:
                print(f"[*] Searching Exploits in the database for banner {banner}")
                exploit_counter = 0

            # Try to extract software and version
                match = re.findall(r'\((.*?) (.*?)\)', banner)
                if match:
                    fsoftware, fsversion = match[0]
                else:
                # If no version info, use the entire banner as software name
                    fsoftware = banner.strip()
                    fsversion = ''

                for line in fp:
                    match = re.match(r'(\d+),"(.+)"', line)
                    if match:
                        id, exploit = match.groups()
                        id = int(id)
                    
                    # Case-insensitive match for software name and version
                    if fsoftware.lower() in exploit.lower() and (fsversion.lower() in exploit.lower() or fsversion == ''):
                        print(Fore.GREEN + "[+] FTP Version is vulnerable!! ")
                        print(Fore.WHITE + Style.BRIGHT + f"[+] Exploit: {exploit}")
                        print(Fore.WHITE + Style.BRIGHT + f"[*] Exploit DB : http://exploit-db.com/download/{id}")
                        exploit_counter += 1

            if exploit_counter == 0:
                print("[+] No exploits found in DB file..")
                
        except FileNotFoundError:
            print("[-] Failed to open the ftp-vuln.db file.")
        except Exception as e:
            print(f"[-] Error: {e}")




    

def menu():

    banner='''
╭━━━┳╮
┃╭━┳╯╰╮
┃╰━┻╮╭╋━━╮╱╱╭━━┳━━┳━━┳━╮
┃╭━━┫┃┃╭╮┣━━┫━━┫╭━┫╭╮┃╭╮╮
┃┃╱╱┃╰┫╰╯┣━━╋━━┃╰━┫╭╮┃┃┃┃
╰╯╱╱╰━┫╭━╯╱╱╰━━┻━━┻╯╰┻╯╰╯
╱╱╱╱╱╱┃┃
╱╱╱╱╱╱╰╯
'''
    print(Fore.RED+banner+Fore.RESET)
    print(Fore.RED+"Author - Sc17"+Fore.RESET)
    print(Fore.RED+"Github - https://github.com/MIISTERC"+Fore.RESET)
menu()
scan = scanner(target,port)
scan.check_anon_login()
vuln = VulnScan(target,port)
banner = vuln.grabBanner()
print("Banner Grabbed! : ",banner)
vuln.vuln_check(banner)
