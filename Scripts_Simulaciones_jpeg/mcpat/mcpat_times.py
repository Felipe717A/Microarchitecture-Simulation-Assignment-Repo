# mcpat.py
import csv
import subprocess
import time

def run_command(command):
    start_time = time.time()
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        if process.returncode != 0:
            print(f"Command failed with exit code {process.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def main():
    cmd1 = "python2 gem5toMcPAT_cortexA76.py stats.txt config.json ARM_A76_2.1GHz.xml"
    cmd2 = "./mcpat/mcpat -infile config.xml > power_data.log"
    time_cmd1 = run_command(cmd1)
    print(f"Comando 1 tomó {time_cmd1:.2f} segundos en ejecutarse.")
    time_cmd2 = run_command(cmd2)
    print(f"Comando 2 tomó {time_cmd2:.2f} segundos en ejecutarse.")

if __name__ == "__main__":
    main()