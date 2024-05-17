import subprocess

# Comando para definir a política de execução
set_execution_policy_command = 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force'

# Execute o comando no PowerShell para definir a política de execução
subprocess.run(['powershell', '-Command', set_execution_policy_command], shell=True)

# Caminho para o script de ativação do ambiente virtual
activate_script_path = r'.\venv\Scripts\Activate.ps1'

# Execute o script de ativação do ambiente virtual no PowerShell
subprocess.run(['powershell', '-Command', activate_script_path], shell=True)
