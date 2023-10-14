import os
import subprocess
import time

archivo_salida = "new2.txt"
archivo_entrada = "m5out/stats.txt"


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

count=0
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
                                            
                                            #MOREOPTIONS = f"--l1i_size={cache_L1} --l1i_assoc={assoc_L1} --l2_size={cache_L2} --l2_assoc={assoc_L2} --l3_size={cache_L3} --l3_assoc={assoc_L3} --lq_entries={lq_entries} --sq_entries={sq_entries} --btb_entries={btb_entries} --num_fu_intDIVMUL={num_fu_intDIVMUL} --num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}"
                                            linea_deseada = None
                                            linea_deseada2 = None
                                            
                                            
                                            stats=f"~/Dock/gem5/mp3enc/l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.txt"
                                            config=f"~/Dock/gem5/mp3enc/Config_l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.json"
                                            configxml=f"Config_l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.xml"
                                            
                                            
                                            #--------------------------------------------------- Modificacion Portatil Felipe
                                            
                                                                
                                            os.system(f"python2 gem5toMcPAT_cortexA76.py  {stats} {config} ARM_A76_2.1GHz.xml")
                                            os.system(f"./mcpat -infile {configxml} > power_data.log")
                                            
                                            with open("power_data.log", "r") as f_entrada2:
                                                # Leer todas las líneas del archivo
                                                lineas2 = f_entrada2.readlines()
                                            
                                            
                                            for linea in lineas2:
                                                if linea.startswith("  Total Leakage ="):
                                                    #linea_deseada = linea.split("#")[0].replace(" ", "").replace("cpi","cpi.")+MOREOPTIONS+ " \n"
                                                    linea_deseada = linea.replace(" ", "").replace("W","").replace("=","/").replace(".",",").replace("\n","")+"/"
                                                    #print(linea_deseada)
                                                if linea.startswith("  Runtime Dynamic ="):
                                                    linea_deseada += linea.replace(" ", "").replace("W","").replace("=","/").replace(".",",").replace("\n","")+"/"
                                                    #print(linea_deseada)
                                                    
                                            #f"/l1i_size={cache_L1}/l1i_assoc={assoc_L1}/l2_size={cache_L2}/l2_assoc={assoc_L2}/l3_size={cache_L3}/l3_assoc={assoc_L3}/lq_entries={lq_entries}/sq_entries={sq_entries}/btb_entries={btb_entries}/num_fu_intDIVMUL={num_fu_intDIVMUL}/num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}"+ " \n" 
                                                  
                                            with open("new2.txt", "r") as f_entrada:
                                                # Leer todas las líneas del archivo
                                                lineas = f_entrada.readlines()
        
                                            aux=linea_deseada+lineas[count]
                                            #print(linea_deseada)
                                            #print(lineas[count])
                                            print(aux)
                                            #if linea_deseada:
                                            with open("new3.txt", "a") as f_salida:  # Abrir en modo "a" (append) para no borrar lo anterior
                                                    f_salida.write(aux)
                                                
                                                
                                                
                                            #linea_actual = lineas[count]
                                            #print(linea_actual)
                                            count+=1
                                            #Nwextx=f"l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.txt"
                                            #os.system(f"cp m5out/stats.txt mp3enc/{Nwextx}" )
                                            
                                            #Nwextx="Config_"+f"l1i_size={cache_L1},l1i_assoc={assoc_L1},l2_size={cache_L2},l2_assoc={assoc_L2},l3_size={cache_L3},l3_assoc={assoc_L3},lq_entries={lq_entries},sq_entries={sq_entries},btb_entries={btb_entries},num_fu_intDIVMUL={num_fu_intDIVMUL},num_fu_FP_SIMD_ALU={num_fu_FP_SIMD_ALU}.json"
                                            #os.system(f"cp m5out/config.json mp3enc/{Nwextx}" )
