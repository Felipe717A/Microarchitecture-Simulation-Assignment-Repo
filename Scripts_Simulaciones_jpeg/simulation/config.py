# config.py
import os

GEM5PATH = os.path.expanduser("~/gem5/gem5/build/ARM")
SCRIPTPATH = os.path.expanduser("~/gem5/gem5/configs/CortexA76")
WORKLOADS = os.path.expanduser("~/gem5/gem5/workloads")
OUTPUT_DIR = os.path.join(WORKLOADS, "jpeg2k_dec/m5out")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.csv")
BLACKLIST_FILE = os.path.join(OUTPUT_DIR,"blacklist_combinations.csv")
CMD = os.path.join(WORKLOADS, "jpeg2k_dec/jpg2k_dec")
OPTIONS = "-i jpg2kdec_testfile.j2k -o jpg2kdec_outfile.bmp"

cache_sizes_L1 = ['64kB','128kB','256kB', '512kB']
cache_sizes_L2 = ['512kB', '1024kB', '2048kB']
cache_sizes_L3 = ['2048kB', '4096kB', '8192kB']
assocs_L1 = [2, 4, 6, 8, 16]
assocs_L2 = [8, 16, 32]
assocs_L3 = [32, 64, 128]

fetch_width_values = [4, 8, 16, 32, 64]
decode_width_values = [4, 8, 16, 32, 64]

rob_entries_values = [128, 256, 512]