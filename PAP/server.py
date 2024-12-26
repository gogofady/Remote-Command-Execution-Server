import socket
import subprocess
import os
import platform
import logging  # Import the logging module

# Configure logging
logging.basicConfig(
    filename="server.log",  # Log output to a file named 'server.log'
    level=logging.INFO,     # Set logging level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # Define the log message format
)

# User database with predefined username-password pairs
users = {
    "george": "12345",
    "alice": "password",
    "john": "hello123"
}

# Check if the operating system is Windows
is_windows = platform.system().lower() == "windows"

# Set up the server socket for communication
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
server.bind(('localhost', 12345))  # Bind the server to localhost on port 12345
server.listen(5)  # Listen for up to 5 incoming connections
logging.info("Server is running and waiting for connections...")

while True:
    client_socket, client_address = server.accept()  # Accept an incoming connection
    logging.info(f"Connection received from {client_address}")

    # Authenticate user
    client_socket.send("Please provide your username:password".encode())  # Request credentials from client
    credentials = client_socket.recv(1024).decode()  # Receive and decode the credentials
    username, password = credentials.split(":")  # Split the credentials into username and password

    if username in users and users[username] == password:  # Check if credentials are valid
        logging.info(f"User '{username}' authenticated successfully.")
        client_socket.send("Access Granted. You can now execute commands.".encode())
    else:
        logging.warning(f"Authentication failed for username: {username}")
        client_socket.send("Access Denied. Disconnecting...".encode())  # Inform client of authentication failure
        client_socket.close()  # Close the connection
        continue  # Return to waiting for the next connection

    current_dir = os.getcwd()  # Store the initial working directory

    while True:
        # Prompt the user for a command
        client_socket.send(f"Current Directory: {current_dir}\nEnter a command to execute or type 'exit' to disconnect:".encode())
        command = client_socket.recv(1024).decode()  # Receive the command from the client

        if command.lower() == 'exit':  # Check if the user wants to exit
            client_socket.send("Goodbye!".encode())  # Send a farewell message
            logging.info(f"User '{username}' disconnected.")
            break  # Exit the command loop

        try:
            if command.startswith('cd '):  # Check if the command is to change directories
                new_dir = command[3:].strip()  # Extract the target directory
                new_path = os.path.join(current_dir, new_dir)  # Construct the absolute path

                if os.path.isdir(new_path):  # Verify if the directory exists
                    current_dir = os.path.abspath(new_path)  # Update the current directory
                    client_socket.send(f"Changed directory to {current_dir}".encode())
                    logging.info(f"User '{username}' changed directory to {current_dir}")
                else:
                    client_socket.send(f"The directory '{new_dir}' does not exist.".encode())  # Notify about invalid directory
                    logging.warning(f"Invalid directory change attempt by user '{username}': {new_dir}")
            else:
                if is_windows and command.strip() == 'ls':  # Map 'ls' to 'dir' for Windows compatibility
                    command = 'dir'

                # Execute the command in a subprocess
                result = subprocess.run(command, shell=True, cwd=current_dir, capture_output=True, text=True)

                if result.stdout:  # Send the command's standard output back to the client
                    client_socket.send(result.stdout.encode())
                    logging.info(f"Command executed by user '{username}': {command}")
                elif result.stderr:  # Send any error messages from the command
                    client_socket.send(result.stderr.encode())
                    logging.error(f"Error during command execution by user '{username}': {result.stderr}")
                else:  # Notify if the command executed successfully but had no output
                    client_socket.send("Command executed successfully with no output.".encode())

        except Exception as e:
            # Handle any unexpected errors during command execution
            client_socket.send(f"Error executing command: {str(e)}".encode())
            logging.error(f"Exception during command execution by user '{username}': {str(e)}")

    client_socket.close()  # Close the connection after exiting the loop
    logging.info(f"Connection closed with {client_address}")
