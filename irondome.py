
import argparse
import os
import time
import daemon
import threading
import logging
import magic
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import math
import psutil

g_time_frame = 5    # Time frame in which counts the number of events
g_max_mod = 20     # Max number of modifications
g_max_create = 5    # Max number of creations
g_max_del = 5       # Max number of deletions

def parse_arguments():
    parser = argparse.ArgumentParser(description="Program that detects anomalous activity inside a critical zone")                 
    parser.add_argument("args", nargs='*')
    arg = parser.parse_args()
    return arg

def is_root_user():
    return os.geteuid() == 0

def cryptographic_processes():
    crypto_processes = ["openssl", "gpg", "sha256sum", "md5sum"]
    try:
        running_processes = [proc.name() for proc in psutil.process_iter()]
        for crypto_process in crypto_processes:
            if crypto_process in running_processes:
                logging.info(f"Warning! Cryptographic process '{crypto_process}' is being executed!")
    except:
        pass

def disk_abuse(past_disk_read, past_disk_write):
    disk_usage_threshold = 30  # 30% disk usage threshold
    read_ops_threshold = 20  # Number of read operations threshold
    write_ops_threshold = 20 # Number of write operations threshold

    disk_usage = psutil.disk_usage('/')
    if disk_usage.percent > disk_usage_threshold:
        logging.info("DANGER! Disk read abuse, high disk usage detected!")
    disk_io = psutil.disk_io_counters(perdisk=True)

    # Here you select the disk (vda)
    new_disk_read = disk_io['vda'].read_count
    new_disk_write = disk_io['vda'].write_count
    if (new_disk_read - past_disk_read) > read_ops_threshold:
        logging.info("DANGER! Disk read abuse, abnormal disk I/O activity detected!")
    if (new_disk_write - past_disk_write) > write_ops_threshold:
        logging.info("DANGER! Disk write abuse, abnormal disk I/O activity detected!")
    return new_disk_read, new_disk_write

def magic_changes(path, ext, past_magic):
    file_magic = magic.Magic()
    files = os.listdir(path)
    file_paths = [os.path.join(path, file) for file in files if os.path.isfile(os.path.join(path, file))]
    if ext is not None:
        file_paths = [file for file in file_paths if os.path.splitext(file)[1] in ext]
    new_magic = {}
    for file_path in file_paths:
        if os.path.exists(file_path):
            new_magic[file_path] = file_magic.from_file(file_path)
    for key, value in past_magic.items():
        if os.path.exists(os.path.join(path, key)):
            if value != new_magic[key]:
                logging.info(f"Warning! Magic changes in: {key}")
    return new_magic

def calculate_entropy(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    byte_count = {}
    total_bytes = len(data)
    for byte in data:
        if byte in byte_count:
            byte_count[byte] += 1
        else:
            byte_count[byte] = 1
    entropy = 0
    for count in byte_count.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)
    return entropy

def entropy_changes(path, ext, past_entropy):
    files = os.listdir(path)
    file_paths = [os.path.join(path, file) for file in files if os.path.isfile(os.path.join(path, file))]
    if ext is not None:
        file_paths = [file for file in file_paths if os.path.splitext(file)[1] in ext]
    new_entropy = {}
    for file_path in file_paths:
        if os.path.exists(file_path):
            new_entropy[file_path] = calculate_entropy(file_path)
    for key, value in past_entropy.items():
        if os.path.exists(os.path.join(path, key)):
            if value != new_entropy[key]:
                logging.info(f"Warning! Entropy changes in: {key}")
    return new_entropy

def memory_usage():
    memory_threshold_MB = 100
    memory_threshold = memory_threshold_MB * 1024 * 1024
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    if memory_usage > memory_threshold:
        logging.info(f"DANGER! Memory usage exeeded {memory_threshold_MB} MB, program stoped")
        exit()

class Events(FileSystemEventHandler):
    def __init__(self, file_path, ext, time_frame, max_mod, max_create, max_del):
        super().__init__()
        self.file_path = file_path
        self.ext = ext
        self.time_frame = time_frame
        self.max_mod = max_mod
        self.max_create = max_create
        self.max_del = max_del
        self.mod_counter = 0
        self.create_counter = 0
        self.del_counter = 0

    def on_modified(self, event):
        if self.ext is not None:
            if os.path.splitext(event.src_path)[1] in self.ext:
                self.mod_counter += 1
        else:
            self.mod_counter += 1

    def on_created(self, event):
        if self.ext is not None:
            if os.path.splitext(event.src_path)[1] in self.ext:
                self.create_counter += 1
        else:
            self.create_counter += 1

    def on_deleted(self, event):
        if self.ext is not None:
            if os.path.splitext(event.src_path)[1] in self.ext:
                self.del_counter += 1
        else:
            self.del_counter += 1

    def file_changes(self):
        if self.mod_counter >= self.max_mod:
            logging.info(f"Warning! Modified files:  {self.mod_counter} times within {self.time_frame} seconds.")
        if self.create_counter >= self.max_create:
            logging.info(f"Warning! Created files: {self.create_counter} times within {self.time_frame} seconds.")
        if self.del_counter >= self.max_del:
            logging.info(f"Warning! Deleted files: {self.del_counter} times within {self.time_frame} seconds.")
        self.mod_counter = 0 
        self.create_counter = 0
        self.del_counter = 0

def monitoring(path, ext=None):
    with daemon.DaemonContext():
        logging.basicConfig(filename="/var/log/irondome/irondome.log",
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        e_handler = Events(path, ext, g_time_frame, g_max_mod, g_max_create, g_max_del)
        observer = Observer()
        observer.schedule(e_handler, path, recursive=True)
        observer.start()
        past_entropy = {}
        past_magic = {}
        past_disk_read = psutil.disk_io_counters(perdisk=True)['vda'].read_count
        past_disk_write = psutil.disk_io_counters(perdisk=True)['vda'].write_count
        while True:
            try:
                timer = time.time()
                while (time.time() - timer) < e_handler.time_frame:
                    memory_usage()
                    past_entropy = entropy_changes(path, ext, past_entropy)
                    past_magic = magic_changes(path, ext, past_magic)
                    cryptographic_processes()
                e_handler.file_changes()
                past_disk_read, past_disk_write = disk_abuse(past_disk_read, past_disk_write)
            except:
                continue

if __name__ == "__main__":
    args = parse_arguments()
    if is_root_user():
        if len(args.args) > 0:
            if os.path.isdir(args.args[0]):
                if len(args.args) > 1:
                    monitoring(args.args[0], args.args[1:])
                else:
                    monitoring(args.args[0])
            else:
                print("Path is not a directory")
        else:
            print("Usage: ./irondome <monitoring_path> <file_ext(opt)> ... &")
    else:
        print("The program can only be executed by a root user")

