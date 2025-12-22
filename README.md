:code:Eura Pass`: Secure Graphical Password Manager

.. image:: media/banner.png :align: center :width: 100% :alt: Eura Pass Banner

|Python| |CustomTkinter| |SQLite|

Eura Pass is a modern desktop application designed to manage your digital identity with a sleek, dark-themed interface. Built with CustomTkinter, it provides a secure vault for your credentials, ensuring that your sensitive data is never stored in plain text.

The application uses industry-standard encryption: Fernet (AES-128) for data and PBKDF2HMAC with 480,000 iterations for secure key derivation.
What does it look like?

.. image:: media/screenshot.png :align: center :width: 80% :alt: App Screenshot

The interface is designed for speed and security:

    Zero-Knowledge Architecture: Your master password is never stored; encryption keys are derived on-the-fly.

    Encrypted Metadata: Unlike many managers, Eura Pass encrypts titles, usernames, and notes—not just the password.

    Animated Sidebar: A smooth sliding window for adding new credentials.

    Deep Integration: Built-in support for TOTP keys, websites, and custom notes.

Installation

    Clone the repository:

.. code-block:: bash

git clone [https://github.com/yourusername/eurapass.git](https://github.com/Hans-4/Eura-Pass.git)
cd eurapass

    Install dependencies:

.. code-block:: bash

pip install customtkinter pillow cryptography

    Run the application:

.. code-block:: bash

python main.py

Project Structure

::

Eura Pass ├── main.py # Main entry point ├── media/ # README documentation images (Banner, Screenshots) ├── assets/ # App UI icons (close_icon.png, plus_icon.png) ├── services/ # Encryption and Database logic ├── ui/ # Window and Frame components └── config/ # Theme and color settings
Dependencies

    CustomTkinter <https://github.com/TomSchimansky/CustomTkinter>_ - Modern UI components.

    Cryptography <https://cryptography.io/>_ - Secure Fernet primitives.

    Pillow <https://python-pillow.org/>_ - Icon rendering and scaling.

License

Copyright (c) 2025 Eura Pass. Distributed under the MIT License.

.. |Python| image:: https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square .. |CustomTkinter| image:: https://img.shields.io/badge/UI-CustomTkinter-orange.svg?style=flat-square .. |SQLite| image:: https://img.shields.io/badge/Database-SQLite-green.svg?style=flat-square

Tipp: Wenn du die Datei auf GitHub hochlädst, stelle sicher, dass die Dateinamen in media/ (z.B. banner.png) exakt so geschrieben werden wie im README (Groß-/Kleinschreibung beachten!).

Soll ich dir noch helfen, eine passende .gitignore Datei zu erstellen, damit die Datenbank (passwords.db) nicht aus Versehen mit hochgeladen wird?
