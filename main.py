from termcolor import colored
import sys
import os
import time

while True:
    if cmd == 'ls':
        diretorio = os.getcwd()
        print(colored(diretorio, 'blue'))
        
    if cmd == 'encode':
        args = input('Nome do arquivo: ')
        if os.path.isfile(args):
            arquivoencode = os.fsencode(args)
            print(colored(arquivoencode, 'blue'))
        else:
            print(colored(f'O arquivo {args} não foi encontrado.', 'red'))
            
    if cmd == 'sair':
        time.sleep(1)
        print(colored('Saindo...', 'red'))
        
        time.sleep(3)
        
        exit()
        
    try:
         if cmd == 'mkdir':
             pastanome = input('Nome da pasta: \n')
        
             os.mkdir(f'/storage/emulated/0/{pastanome}')
        
             time.sleep(1)
        
             pastacaminho = f'/storage/emulated/0/{pastanome}'
             print(colored(pastacaminho, 'blue'))
    except FileExistsError:
        print(colored('Não é possível criar uma pasta sem nome.', 'red'))
        
