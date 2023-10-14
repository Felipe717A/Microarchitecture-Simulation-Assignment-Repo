# mcpat.py
import csv
import subprocess


def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        print(f"Command failed with exit code {process.returncode}")


def main():
    try:
        with open('output.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                ident_uiid = row['unique_id']
                cmd1 = f"python2 gem5toMcPAT_cortexA76.py stats_{ident_uiid}.txt " \
                       f"config_{ident_uiid}.json ARM_A76_2.1GHz.xml > config_{ident_uiid}.xml"
                run_command(cmd1)
                cmd2 = f"./mcpat/mcpat -infile config_{ident_uiid}.xml > power_data_{ident_uiid}.log"
                run_command(cmd2)
    except FileNotFoundError:
        print(f"output.csv not found in path")


if __name__ == "__main__":
    main()
