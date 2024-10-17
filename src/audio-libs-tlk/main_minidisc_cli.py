from .lib_scan import scan_and_process
import os

def main():
    scan_and_process(path_to_library_data=str(os.getcwd()),
                 create_minidisc_labels=True)

