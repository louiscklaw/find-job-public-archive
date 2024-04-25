import os
from pathlib import Path
import shutil
import os

def remove_directory(path_to_remove):
    try:
        shutil.rmtree(path_to_remove)
        print(f"Directory '{path_to_remove}' has been successfully deleted.")
    except Exception as e:
        print(f"Error removing directory '{path_to_remove}': {e}")


def list_directories_recursive(start_dir):
    for root, dirs, _ in os.walk(start_dir):
        for dirname in dirs:
            temp = os.path.join(root, dirname)
            if (len(temp.split('/')) > 2):
                remove_directory(temp)

if __name__ == "__main__":
    start_dir = "_output/000_raw_result"
    list_directories_recursive(start_dir)
