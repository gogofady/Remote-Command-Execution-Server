# Remote Command Execution Server

This repository contains a Python-based server and client application that enables remote command execution. The server handles multiple client connections, authenticates users, and executes commands securely in the context of the connected client's working directory.

## Features

- **Authentication:** Clients must provide valid username-password pairs to access the server.
- **Command Execution:** Authenticated clients can execute commands on the server.
- **Directory Navigation:** Clients can navigate the server's file system using `cd` commands.
- **Logging:** Server activities, including successful authentications, errors, and command executions, are logged to `server.log`.

## Getting Started

### Prerequisites

- Python 3.6 or later
- A terminal or command-line interface

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/remote-command-server.git
   cd remote-command-server
   ```
2. Ensure Python is installed on your system.

### Usage

#### Running the Server

1. Start the server script:
   ```bash
   python server.py
   ```
2. The server will listen on `localhost` and port `12345`.

#### Connecting a Client

1. Start the client script:
   ```bash
   python client.py
   ```
2. Follow the prompts to authenticate with the server.
3. Enter commands to execute on the server, or type `exit` to disconnect.

### Example Interaction

**Server Output:**
```
Server is running and waiting for connections...
Connection received from ('127.0.0.1', 54321)
User 'george' authenticated successfully.
User 'george' changed directory to /path/to/directory
```

**Client Interaction:**
```
Please provide your username:password
Enter your username: george
Enter your password: 12345
Access Granted. You can now execute commands.
Current Directory: /home/user
Enter a command to execute or type 'exit' to disconnect:
>>> ls
file1.txt  file2.txt
>>> exit
Goodbye!
```

## Code Overview

### Server Code (`server.py`)

- **Socket Setup:**
  Creates a TCP socket and binds to `localhost:12345`.
- **Authentication:**
  Validates username-password pairs against a predefined dictionary.
- **Command Execution:**
  Executes shell commands securely within the client's session context.
- **Logging:**
  Logs activities and errors to `server.log`.

### Client Code (`client.py`)

- **Server Connection:**
  Connects to the server at `localhost:12345`.
- **Authentication:**
  Sends credentials to the server for validation.
- **Command Execution Loop:**
  Allows users to send commands and receive results.

## Security Considerations

- **Authentication:**
  Uses plaintext credentials. Future improvements could include encryption (e.g., TLS).
- **Command Injection:**
  Commands are executed in the shell, which could lead to vulnerabilities. Use with trusted clients only.

## Logging

The server logs all activities to `server.log`, including:
- Successful authentications
- Command executions
- Errors and warnings

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

