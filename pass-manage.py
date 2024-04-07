import sys
import json
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def load_passwords(filename="passwords.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_passwords(passwords, filename="passwords.json"):
    with open(filename, "w") as f:
        json.dump(passwords, f)

def add_password(service, username, password, key, filename="passwords.json"):
    encrypted_password = encrypt_password(password, key)
    passwords = load_passwords(filename)
    passwords[service] = {"username": username, "password": encrypted_password}
    save_passwords(passwords, filename)

def get_password(service, key, filename="passwords.json"):
    passwords = load_passwords(filename)
    if service not in passwords:
        print(f"No password found for {service}")
        return None
    encrypted_password = passwords[service]["password"]
    password = decrypt_password(encrypted_password, key)
    return password

def delete_password(service, key, filename="passwords.json"):
    passwords = load_passwords(filename)
    if service not in passwords:
        print(f"No password found for {service}")
        return
    del passwords[service]
    save_passwords(passwords, filename)

def main():
    if len(sys.argv) < 2:
        print("Usage: python password_manager.py [command] [options]")
        print("Commands:")
        print("  generate-key: Generate a new encryption key")
        print("  add [service] [username] [password]: Add a new password for a service")
        print("  get [service]: Get a password for a service")
        print("  delete [service]: Delete a password for a service")
        return
    
    command = sys.argv[1]
    if command == "generate-key":
        key = generate_key()
        print(key.decode())
    elif command == "add":
        if len(sys.argv) < 5:
            print("Usage: python password_manager.py add [service] [username] [password]")
            return
        service = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        key = generate_key()
        add_password(service, username, password, key)
        print(f"Password for {service} added.")
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python password_manager.py get [service]")
            return
        service = sys.argv[2]
        key = generate_key()
        password = get_password(service, key)
        if password:
            print(f"Password for {service}: {password}")
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python password_manager.py delete [service]")
            return
        service = sys.argv[2]
        key = generate_key()
        delete_password(service, key)
        print(f"Password for {service} deleted.")
    else:
        print("Invalid command.")

if _name_ == "_main_":
    main()
