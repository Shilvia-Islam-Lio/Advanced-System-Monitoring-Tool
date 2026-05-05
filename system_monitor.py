import psutil
import time
import os
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_data(cpu, memory):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} | CPU: {cpu}% | RAM: {memory.percent}%\n")

def show_system_info():
    clear_screen()

    print(Fore.YELLOW + "===== SYSTEM MONITOR TOOL =====\n")

    # CPU
    cpu = psutil.cpu_percent(interval=1)
    if cpu > 80:
        print(Fore.RED + f"CPU Usage: {cpu}% ⚠ HIGH!")
    else:
        print(Fore.GREEN + f"CPU Usage: {cpu}%")

    # Memory
    memory = psutil.virtual_memory()
    print(Fore.CYAN + f"\nMemory Used: {memory.percent}%")

    # Log save
    log_data(cpu, memory)

    print(Fore.YELLOW + "\n--- Top 5 Processes ---")

    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(process.info)
        except:
            pass

    top = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    for p in top:
        print(f"PID: {p['pid']} | {p['name']} | CPU: {p['cpu_percent']}%")

while True:
    show_system_info()
    time.sleep(2)