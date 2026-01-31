*# Windows Secure Vault 🛡️*

A multi-layered file security system that integrates **Python** for cryptographic logic, **SQLite** for persistent metadata management, and **PowerShell** for secure Windows OS interaction.

*## 🌟 Overview*
This project addresses the challenge of securing local files while ensuring recovery. Unlike simple scripts that store keys in plaintext, this tool manages unique AES-128 keys in a hidden SQL database and utilizes native Windows APIs for secure user authentication.

*## 🛠️ Technical Architecture*


* **Encryption Engine:** Implements the `cryptography.fernet` library (Symmetric AES-128 in CBC mode with HMAC authentication).
* **Persistent Storage:** Utilizes **SQLite** to map filenames to their respective encryption keys, allowing for multi-file management.
* **Secure Input:** Invokes **PowerShell** subprocesses to use the `Read-Host -AsSecureString` API, preventing master passwords from appearing in terminal history or plaintext memory.
* **Anti-Deletion Measures:** Leverages Windows file attributes (`attrib +h`) via subprocess calls to obfuscate the database from standard File Explorer views.

*## 🚀 Getting Started*

**### Prerequisites**
- Windows OS
- Python 3.8+
- `pip install cryptography`

**### Installation**
1. Clone the repository:
   ```bash
   git clone [https://github.com/RShasikiran/windows-secure-vault.git](https://github.com/RShasikiran/windows-secure-vault.git)
