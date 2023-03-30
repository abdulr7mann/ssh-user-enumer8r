# SSH User Enumeration

This Python script can be used to enumerate valid usernames on a target SSH server. It uses the Paramiko library to perform the SSH connection and authentication.
## Prerequisites

- Python 3
- Paramiko library

## Installation

- Clone the repository: `git clone https://github.com/abdulr7mann/ssh-user-enumer8r.git`
- Install the Paramiko library: `pip install paramiko`

## Usage
```bash 
python3 enumer8r.py [--host 127.0.0.1 | --ip-list ips.txt | --user root | --user-list users.txt] [--port 22]
```
Arguments:

- `--host`: single IP address to attack
- `--ip-list`: file with a list of IP addresses
- `--user`: single username to use for attacking
- `--user-list`: file with a list of usernames to use for attacking
- `--port`: SSH port (default is 22)

At least one IP and one username must be provided.
## Examples
```bash 
# Attack a single host with a single username
python3 enumer8r.py --host 127.0.0.1 --user root

# Attack a list of hosts with a single username
python3 enumer8r.py --ip-list ips.txt --user root

# Attack a single host with a list of usernames
python3 enumer8r.py --host 127.0.0.1 --user-list users.txt

# Attack a list of hosts with a list of usernames
python3 enumer8r.py --ip-list ips.txt --user-list users.txt
```


## License
-------
This tool is released under the GNU General Public License v3.0. You can find a copy of the license in the LICENSE file.

### Disclaimer
- This tool is provided as-is and without any warranty. The author assumes no responsibility or liability for any errors or omissions that may occur while using this tool. Use at your own risk.
- This tool is intended for legal and authorized use only. Misuse of this tool can result in criminal charges and/or damage to systems. The author is not responsible for any misuse or damage caused by this tool. Use at your own risk.

