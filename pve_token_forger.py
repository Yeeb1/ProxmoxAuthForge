import sys
import time
import tempfile
import logging
import subprocess
import base64

def generate_ticket(authkey_path, system_type, username, time_offset=-30):
    if system_type not in ['PVE', 'PMG']:
        raise ValueError("Invalid system type. Must be 'PVE' or 'PMG'.")

    valid_domains = ['@pve', '@pmg', '@pam']
    if not any(username.endswith(domain) for domain in valid_domains):
        raise ValueError(f"Username must end with one of the following: {', '.join(valid_domains)}.")

    timestamp = hex(int(time.time()) + time_offset)[2:].upper()
    plaintext = f'{system_type}:{username}:{timestamp}'

    with open(authkey_path, 'rb') as file:
        authkey_bytes = file.read()

    authkey_temp = tempfile.NamedTemporaryFile(delete=False)
    logging.info(f'writing authkey to {authkey_temp.name}')
    authkey_temp.write(authkey_bytes)
    authkey_temp.close()

    txt_temp = tempfile.NamedTemporaryFile(delete=False)
    logging.info(f'writing plaintext to {txt_temp.name}')
    txt_temp.write(plaintext.encode('utf-8'))
    txt_temp.close()

    logging.info('calling openssl to sign')
    sig = subprocess.check_output(
        ['openssl', 'dgst', '-sha1', '-sign', authkey_temp.name, '-out', '-', txt_temp.name])
    sig = base64.b64encode(sig).decode('latin-1')

    ret = f'{plaintext}::{sig}'
    logging.info(f'generated ticket for {username} on {system_type}: {ret}')

    return ret

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python script.py <path_to_authkey> <system_type> <username>")
        sys.exit(1)
    authkey_path = sys.argv[1]
    system_type = sys.argv[2]
    username = sys.argv[3]
    ticket = generate_ticket(authkey_path, system_type, username)
    print(ticket)
