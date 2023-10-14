import os
import shutil

# Set the source directory
src_dir = "/home/santiago/universidad/arquitectura/gem5_McPAT"

# Set the destination directories
dest_dir_json = "/home/santiago/universidad/arquitectura/jpeg2k_dec/config_json"
dest_dir_xml = "/home/santiago/universidad/arquitectura/jpeg2k_dec/config"
dest_dir_power = "/home/santiago/universidad/arquitectura/jpeg2k_dec/power"
dest_dir_stats = "/home/santiago/universidad/arquitectura/jpeg2k_dec/stats"

# Get list of all files in source directory
all_files = os.listdir(src_dir)
def move_files(files, dest):
    for file in files:
        shutil.move(os.path.join(src_dir, file), os.path.join(dest, file))

json_files = [file for file in all_files if file.endswith(".json")]
move_files(json_files, dest_dir_json)

xml_files = [file for file in all_files if file.endswith(".xml")]
move_files(xml_files, dest_dir_xml)

power_files = [file for file in all_files if file.startswith("power_data")]
move_files(power_files, dest_dir_power)

stats_files = [file for file in all_files if file.startswith("stats")]
move_files(stats_files, dest_dir_stats)
