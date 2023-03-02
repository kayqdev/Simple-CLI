import json
import subprocess
import os
from tqdm import tqdm
from termcolor import colored
settings_obj = 'settings/settings.json'

class CommandLine:
	def __init__(self):
		with open(settings_obj) as f_obj:
			self.configs = json.load(f_obj)
			self.username = self.configs['username']
			self.version = self.configs['version']

			try:
				self.standard_path = self.configs['standard-path']
				os.chdir(self.standard_path)
			except FileNotFoundError:
				print(colored(f'O caminho padrão definido em settings.json "{self.standard_path}" não existe.\n', 'red'))
				self.standard_path = input(f'Digite um caminho válido: ')
				with open(settings_obj) as f_obj:
					self.configs = json.load(f_obj)

				with open(settings_obj, 'w') as f_obj:
					self.configs['standard-path'] = self.standard_path
					json.dump(self.configs, f_obj, indent=2)

	def list_dir(self):
		print('\n')
		output = subprocess.check_output(['ls'])
		print(output.decode('utf-8'))

	def change_dir(self, path):
		self.path = path
		try:
			os.chdir(self.path)
		except FileNotFoundError:
			print(f'O diretório "{self.path}" não existe.')
		except NotADirectoryError:
			print(f'"{self.path}" não é um diretório.')
		print(f'Diretório de trabalho atual: {os.getcwd()}')

	def create_archive(self, name_archive):
		self.name_archive = name_archive
		os.system(f'touch {self.name_archive}')

	def install_package(self, package_name):
		self.package_name = package_name

		output = subprocess.Popen(['apt', 'install', self.package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		total_size = 0
		for linha in output.stderr:
			if "After this operation" in linha.decode():
				total_size = int(linha.decode().split()[-2])
		progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=f"Instalando {self.package_name}...")

		while True:
			linha = output.stderr.readline()
			if not linha:
				break
			progress_bar.update(len(linha))

		output_code = output.wait()
		if output_code == 0:
			progress_bar.write(f"{self.package_name} instalado com sucesso.")
		else:
			progress_bar.write(f"Erro ao instalar {self.package_name}.")

	def makedir(self, dir_name):
		self.dir_name = dir_name

		try:
			subprocess.run(['mkdir', self.dir_name], check=True)
			print(f"A pasta {self.dir_name} foi criada com sucesso!")
		except subprocess.CalledProcessError as e:
			print(f"Ocorreu um erro ao criar a pasta: {e}")

	def open(self, app_name):
		self.app_name = app_name

		try:
			app_process = subprocess.Popen([self.app_name])
			app_process.wait()
			print(f"O processo do {self.app_name} foi encerrado.")
		except subprocess.CalledProcessError as e:
			print(f"Ocorreu um erroa o iniciar o processo do {self.app_name}: {e}")

	def rename(self, old_name, new_name):
		self.old_name = old_name
		self.new_name = new_name

		try:
			subprocess.run(['mv', self.old_name, self.new_name], check=True)
			print(f"O arquivo {self.old_name} foi renomeado para {self.new_name} com sucesso!")
		except subprocess.CalledProcessError as e:
			print(colored("Ocorreu um erro ao renomear o arquivo.", 'red'))

	def about(self):
		print(f"{self.version} | simple-cli")

cmd = CommandLine()

def execute_cli():
	while True:
		command = input(colored(f'{cmd.username}', 'cyan')).split()
		if command[0] == 'cd':
			path = command[-1]
			cmd.change_dir(path)

		elif command[0] == 'ls':
			cmd.list_dir()

		elif command[0] == 'clear':
			os.system('clear')

		elif command[0] == 'install':
			cmd.install_package(command[-1])

		elif command[0] == 'touch':
			cmd.create_archive(command[-1])

		elif command[0] == 'makedir':
			cmd.makedir(command[-1])

		elif command[0] == 'open':
			cmd.open(command[-1])

		elif command[0] == 'rename':
			cmd.rename(command[1], command[-1])

		elif command[0] == 'about':
			cmd.about()

		elif command[0] == 'exit':
			break

		else:
			print(colored(f"{command[0]}: comando não econtrado.", "red"))