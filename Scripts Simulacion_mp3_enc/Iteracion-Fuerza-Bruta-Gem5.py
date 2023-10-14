import os
import subprocess
import time

archivo_salida = "new2.txt"
archivo_entrada = "m5out/stats.txt"

#---------------------------------------------------------------------------
GEM5PATH = os.path.expanduser("~/gem5/gem5/build/ARM")
SCRIPTPATH = os.path.expanduser("~/gem5/gem5/configs/CortexA76")
WORKLOADS = os.path.expanduser("~/gem5/gem5/workloads")
OUTPUT_DIR = os.path.join(WORKLOADS, "mp3_enc/m5out")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.csv")
BLACKLIST_FILE = os.path.join(OUTPUT_DIR,"blacklist_combinations.csv")
CMD = os.path.join(WORKLOADS, "mp3_enc/mp3_enc")
OPTIONS = "mp3enc_testfile.wav mp3enc_outfile.mp3"
#---------------------------------------------------------------------------

cache_sizes_L1 = ['16kB','32kB', '64kB']
cache_sizes_L2 = ['512kB', '1024kB', '2048kB']
cache_sizes_L3 = ['8192kB', '16384kB']
assocs_L1 = [2, 4, 6]
assocs_L2 = [8, 16]
assocs_L3 = [32, 64, 128]

lq_entries_values = [68, 136, 272]
sq_entries_values = [72, 144, 288]
btb_entries_values = [8192, 16384]

num_fu_intDIVMUL_values = [1, 2]
num_fu_FP_SIMD_ALU_values = [2, 4]
cpi=0
ipc=0


for cache_L1 in cache_sizes_L1:
    for assoc_L1 in assocs_L1:
        for cache_L2 in cache_sizes_L2:
            for assoc_L2 in assocs_L2:
                for cache_L3 in cache_sizes_L3:
                    for assoc_L3 in assocs_L3:
                        for lq_entries in lq_entries_values:
                            for sq_entries in sq_entries_values:
                                for btb_entries in btb_entries_values:
                                    for num_fu_intDIVMUL in num_fu_intDIVMUL_values:
                                        for num_fu_FP_SIMD_ALU in num_fu_FP_SIMD_ALU_values:
                                            
                                            MOREOPTIONS = f"--l1i_size={cache_L1} --l1i_assoc={assoc_L1} --l2_size={cache_L2} --l2_assoc={assoc_L2} --l3_size={cache_L3} --l3_assoc={assoc_L3} --lq_entries={lq_entries} --sq_entries={sq_entries} --btb_entries={btb_entries} --num_fu_intDIVMUL={num_fu_intDIVMUL} --num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}"
                                            
                                            command = f"{GEM5PATH}/gem5.fast {SCRIPTPATH}/CortexA76.py --cmd={WORKLOADS}/mp3_enc/mp3_enc --options=\"workloads/mp3_enc/mp3enc_testfile.wav mp3enc_outfile.mp3\" {MOREOPTIONS}"
                                            os.system(command)
                                            
                                            with open(f"m5out/stats.txt") as stats_file:
                                                for line in stats_file:
                                                    if "system.cpu.cpi" in line:
                                                        cpi = line.split()[1]
                                                    elif "system.cpu.ipc" in line:
                                                        ipc = line.split()[1]
                                            
                                            #--------------------------------------------------- Modificacion Portatil Felipe
                                            with open(archivo_entrada, "r") as f_entrada:
                                                # Leer todas las líneas del archivo
                                                lineas = f_entrada.readlines()
                                                                
                                            
                                            linea_deseada = None
                                            for linea in lineas:
                                                if linea.startswith("system.cpu.cpi "):
                                                    linea_deseada = linea.split("#")[0].replace(" ", "").replace("cpi","cpi.")+MOREOPTIONS+ " \n"
                                                    break
                                                if linea.startswith("system.cpu.ipc "):
                                                    linea_deseada += linea.split("#")[0].replace(" ", "").replace("ipc","ipc.")+MOREOPTIONS+ " \n"
                                                    break
                                            
                                            
                                            if linea_deseada:
                                                with open(archivo_salida, "a") as f_salida:  # Abrir en modo "a" (append) para no borrar lo anterior
                                                    f_salida.write(linea_deseada)
                                                print("La línea 'system.cpu.cpi' se ha guardado en el archivo de salida.")
                                                
                                            
                                            Nwextx=f"l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.txt"
                                            os.system(f"cp m5out/stats.txt mp3enc/{Nwextx}" )
                                            
                                            Nwextx="Config_"+f"l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.json"
                                            os.system(f"cp m5out/config.json mp3enc/{Nwextx}" )
