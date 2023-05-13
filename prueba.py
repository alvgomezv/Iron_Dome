import os
import psutil
import pySMART
import time

path_to_monitor = "."

def monitor_disk_read():
    disk_usage = psutil.disk_usage(path_to_monitor)
    read_bytes = disk_usage.read_bytes
    threshold = 1000000  # Set the threshold for disk read abuse

    if read_bytes > threshold:
        print("Disk read abuse detected!")
    else:
        print("Disk read activity within normal range.")

def monitor_cryptographic_activity():
    cryptographic_processes = ["openssl", "gnupg", "cryptsetup"]  # Add relevant cryptographic processes

    for process in psutil.process_iter(["name"]):
        if process.info["name"] in cryptographic_processes:
            print("Intensive cryptographic activity detected!")
            break
    else:
        print("No intensive cryptographic activity found.")

def monitor_disk_health():
    disk = pySMART.Device("/dev/sda")  # Replace with the appropriate device path
    smart_attributes = disk.attributes

    # Check relevant SMART attributes for disk health
    if smart_attributes["read_error_rate"].normalized > 80:
        print("Disk read error rate is high. Disk health may be compromised.")

while True:
    monitor_disk_read()
    monitor_cryptographic_activity()
    monitor_disk_health()
    # Adjust the sleep duration as per your needs
    time.sleep(60)  # Sleep for 60 seconds before running the monitoring functions again
