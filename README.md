# Eura Pass: Secure Graphical Password Manager

 ![Python]( https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square) ![CustomTkinter]( https://img.shields.io/badge/UI-CustomTkinter-orange.svg?style=flat-square ) ![SQLite]( https://img.shields.io/badge/Database-SQLite-green.svg?style=flat-square)

* * *

Eura Pass is a modern desktop application designed to manage your digital identity with a sleek, dark-themed interface. Built with **CustomTkinter**, it provides a secure vault for your credentials, ensuring that your sensitive data is never stored in plain text.

The application uses industry-standard encryption: **Fernet (AES-128)** for data and **PBKDF2HMAC** with 480,000 iterations for secure key derivation.

# What does it look like?

<div class="top-screenshot">
    <img src="https://raw.githubusercontent.com/Hans-4/Eura-Pass/main/media/home-example-img.png" style="max-width: 100%; max-height: 35em;">
</div>

The interface is designed for speed and security:

- **Zero-Knowledge Architecture**: Your master password is never stored; encryption keys are derived on-the-fly.
- **Encrypted Metadata**: Unlike many managers, Eura Pass encrypts titles, usernames, and notes—not just the password.
- **Animated Sidebar**: A smooth sliding window for adding new credentials.
- **Deep Integration**: Built-in support for TOTP keys, websites, and custom notes.

# Languages

- **German**

Eura Pass currently supports only German; English support is coming soon!

# Project Structure

<pre>
Eura Pass  
├── main.py       # Main entry point  
├── media/        # README documentation images 
├── assets/       # App UI icons (close_icon.png, plus_icon.png)  
├── services/     # Encryption and Database logic  
├── ui/           # Window and Frame components  
└── config/       # Theme and color settings
</pre>

# Dependencies

- CustomTkinter : https://customtkinter.tomschimansky.com/
- Cryptography: https://cryptography.io/en/latest/
- Pillow : https://github.com/python-pillow/Pillow/blob/main/README.md

# License

Copyright (c) 2025 Eura Pass. Distributed under the MIT License.
