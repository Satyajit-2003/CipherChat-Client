# CipherChat Client

- CipherChat is a secure messaging application that uses end-to-end encryption to ensure that only the sender and the recipient can read the messages. 
- This repository contains the client-side code for the CipherChat application.
- The technologies used in this project are:
    - Python
    - Flask
    - Socket Programming
    - Cryptography
    - SQLite
    - HTML
    - CSS
    - JavaScript
- The server-side code for this project can be found at [this link](https://github.com/Satyajit-2003/CipherChat-Server).
- The client side features end-to-end encryption using the RSA algorithm for key exchange and AES algorithm for message encryption when stored locally in the database.
- The client allows simultaneous 1-1 chat with multiple users.

### Prerequisites

- Windows, Linux or macOS
- Python 3.6 or higher

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/Tannu-ck21/CipherChat-Client
```
2. Change the directory
```bash
cd CipherChat-Client
```
3. Install the requirements
```bash
pip install -r requirements.txt
```
3. Change the configuration in the `config.py` files and set the `SERVER_API` to required endpoint.
> [!WARNING]
> **IMPORTANT**: Be sure to change the `SECRET_KEY`, `AES_KEY` and `AES_IV` in the `config.py` file.
4. Run the server
```bash
python run.py
```


### Installing

A step by step series of examples that tell you how to get a development environment running:

1. No installation required.
2. You can visit the client at [http://localhost:5500](http://localhost:5500/)

## Contributing

- You are welcome to contribute to this project. Please create a pull request and I will review it.
- If you find any bugs, please create an issue.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
