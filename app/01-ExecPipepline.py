# Python - Run the Pipeline

# Imports
import subprocess
import time

# Function to execute terminal commands
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"\nCommand '{command}' executed successfully.")
        print("\nOutput:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\nError executing command '{command}'.")
        print("\Error:\n", e.stderr)

# Function to execute other Python scripts
def run_pipeline(script_name):
    try:
        result = subprocess.run(['poetry', 'run', 'python', script_name], check=True, capture_output=True, text=True)
        print(f"\nScript {script_name} executed successfully.")
        print("\nOutput:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\nError executing script {script_name}.")
        print("\nError:\n", e.stderr)

# Commands for creating the Docker container and installing packages
docker_command = "docker run --name fraud-detection -p 5553:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin1010 -e POSTGRES_DB=transactiondb -d postgres:16.1"
# pip_command = "pip install -r requirements.txt"
# poetry install

# Start the timer
start_time = time.time()

# Run terminal commands
run_command(docker_command)
# run_command(pip_command)

# Script list
scripts = [
    '02-CreateTables.py',
    '03-LoadData.py',
    # '04-RunLLM.py'
]

# Runs scripts in a loop
for script in scripts:
    run_pipeline(script)

# Command to destroy Docker container
destroy_docker_command = "docker rm -f fraud-detection"
run_command(destroy_docker_command)

# Calculates total execution time
end_time = time.time()
total_time = end_time - start_time

print(f"\nPipeline executado com sucesso.")
print(f"Tempo total de execução: {total_time:.2f} segundos.\n")
