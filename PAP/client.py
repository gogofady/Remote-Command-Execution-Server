import socket

# Step 1: Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))  # Connect to the server at localhost:12345

# Step 2: Authentication
server_message = client.recv(1024).decode()
print(server_message)

username = input("Enter your username: ")
password = input("Enter your password: ")
client.send(f"{username}:{password}".encode())

response = client.recv(1024).decode()
print(response)

if "Access Denied" in response:
    client.close()
    exit()  # Exit if authentication fails

# Step 3: Command Execution Loop
while True:
    command_prompt = client.recv(1024).decode()
    print(command_prompt)

    command = input(">>> ")
    client.send(command.encode())

    if command.lower() == 'exit':
        break

    # Receive the result from the server
    result = client.recv(1024).decode()
    print(result)

# Step 4: Close the connection
client.close()
