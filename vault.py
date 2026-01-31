import sqlite3
import subprocess
import os
import sys
from cryptography.fernet import Fernet

# --- 1. THE DATABASE (The Keychain) ---
def init_db():
    conn = sqlite3.connect('vault.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS keys 
                    (file_name TEXT PRIMARY KEY, encryption_key BLOB)''')
    conn.commit()
    conn.close()
    # Use PowerShell to hide the database file from File Explorer
    subprocess.run(["powershell", "-Command", "attrib +h vault.db"])

# --- 2. POWERSHELL INTERFACE (The Secure Prompt) ---
def get_master_password():
    print("--- WINDOWS SECURE VAULT ---")
    ps_cmd = (
        "$p = Read-Host 'Enter Master Password to Authenticate' -AsSecureString; "
        "$ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($p); "
        "$plain = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr); "
        "Write-Output $plain"
    )
    result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    return result.stdout.strip()

# --- 3. ENCRYPTION LOGIC ---
def encrypt_file(target_file, master_pw):
    if master_pw != "Password123": # Change this password!
        print("!! ACCESS DENIED !!")
        return

    if not os.path.exists(target_file):
        print("File not found.")
        return

    # Create Key
    file_key = Fernet.generate_key()
    cipher = Fernet(file_key)

    with open(target_file, 'rb') as f:
        data = f.read()

    # Scramble data
    encrypted_data = cipher.encrypt(data)

    with open(target_file, 'wb') as f:
        f.write(encrypted_data)

    # Store key in hidden SQL DB
    conn = sqlite3.connect('vault.db')
    conn.execute("INSERT OR REPLACE INTO keys VALUES (?, ?)", (target_file, file_key))
    conn.commit()
    conn.close()
    print(f"DONE: {target_file} is now encrypted and locked.")

# --- 4. DECRYPTION LOGIC ---
def decrypt_file(target_file, master_pw):
    if master_pw != "Password123":
        print("!! ACCESS DENIED !!")
        return

    conn = sqlite3.connect('vault.db')
    cursor = conn.execute("SELECT encryption_key FROM keys WHERE file_name = ?", (target_file,))
    row = cursor.fetchone()
    conn.close()

    if row:
        cipher = Fernet(row[0])
        with open(target_file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        
        with open(target_file, 'wb') as f:
            f.write(decrypted_data)
        print(f"DONE: {target_file} has been decrypted.")
    else:
        print("No key found for this file.")

# --- MAIN MENU ---
if __name__ == "__main__":
    init_db()
    action = input("Type 'E' to Encrypt or 'D' to Decrypt: ").upper()
    filename = input("Enter the full filename (e.g., data.txt): ")
    password = get_master_password()

    if action == 'E':
        encrypt_file(filename, password)
    elif action == 'D':
        decrypt_file(filename, password)
    else:
        print("Invalid Choice.")