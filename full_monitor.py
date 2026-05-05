import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from datetime import datetime
import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)

cpu_data = []
paused = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_data(cpu, memory, disk):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} | CPU: {cpu}% | RAM: {memory}% | Disk: {disk}%\n")

def beep_alert():
    try:
        if os.name == 'nt':
            import winsound
            winsound.Beep(1000, 300)
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()
    except:
        pass

def on_key(event):
    global paused
    if event.key == 'p':
        paused = not paused

def show_text(cpu):
    clear_screen()

    print(Fore.YELLOW + "="*50)
    print(Style.BRIGHT + Fore.CYAN + "      ULTIMATE SYSTEM MONITOR TOOL")
    print(Fore.YELLOW + "="*50)

    # CPU
    if cpu > 80:
        print(Fore.RED + Style.BRIGHT + f"CPU Usage: {cpu}% ⚠ HIGH!")
        beep_alert()
    elif cpu < 10:
        print(Fore.BLUE + f"CPU Usage: {cpu}% (Idle)")
    else:
        print(Fore.GREEN + f"CPU Usage: {cpu}%")

    # CPU Bar
    bar_length = int(cpu / 2)
    bar = "█" * bar_length
    space = " " * (50 - bar_length)
    print(Fore.MAGENTA + f"CPU Load: [{bar}{space}]")

    # Average & Peak
    if len(cpu_data) > 0:
        avg_cpu = sum(cpu_data) / len(cpu_data)
        peak_cpu = max(cpu_data)
        print(Fore.CYAN + f"Average CPU: {round(avg_cpu,2)}%")
        print(Fore.CYAN + f"Peak CPU: {peak_cpu}%")

    # Per Core
    cores = psutil.cpu_percent(percpu=True)
    print(Fore.YELLOW + Style.BRIGHT + "\nCPU per core:")
    for i, c in enumerate(cores):
        print(Fore.WHITE + f"Core {i}: {c}%")

    # Memory
    memory = psutil.virtual_memory()
    print(Fore.GREEN + f"\nMemory Usage: {memory.percent}%")
    print(Fore.WHITE + f"Total RAM: {round(memory.total / (1024**3), 2)} GB")
    print(Fore.WHITE + f"Available RAM: {round(memory.available / (1024**3), 2)} GB")

    if memory.percent > 80:
        print(Fore.RED + Style.BRIGHT + "⚠ High Memory Usage!")

    # Disk
    disk = psutil.disk_usage('/')
    print(Fore.YELLOW + f"\nDisk Usage: {disk.percent}%")

    # Processes
    print(Fore.BLUE + f"Total Running Processes: {len(psutil.pids())}")

    # Uptime
    uptime = time.time() - psutil.boot_time()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    print(Fore.CYAN + f"System Uptime: {hours}h {minutes}m")

    # Network
    net = psutil.net_io_counters()
    print(Fore.MAGENTA + f"\nNetwork Sent: {round(net.bytes_sent / (1024**2),2)} MB")
    print(Fore.MAGENTA + f"Network Received: {round(net.bytes_recv / (1024**2),2)} MB")

    # Log
    log_data(cpu, memory.percent, disk.percent)

    print(Fore.YELLOW + Style.BRIGHT + "\n--- Top 5 Processes ---")

    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            name = process.info['name'] or ""
            if process.info['cpu_percent'] is not None and "Idle" not in name:
                processes.append(process.info)
        except:
            pass

    top = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    for p in top:
        print(Fore.WHITE + f"PID: {p['pid']} | {p['name']} | CPU: {p['cpu_percent']}% | RAM: {round(p['memory_percent'],2)}%")

def update(frame):
    global paused

    if paused:
        return

    cpu = psutil.cpu_percent()
    cpu_data.append(cpu)

    if len(cpu_data) > 20:
        cpu_data.pop(0)

    show_text(cpu)

    plt.cla()
    plt.plot(cpu_data)
    plt.ylim(0, 100)
    plt.title("Live CPU Usage")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU %")
    plt.grid()

    plt.savefig("cpu_graph.png")

ani = FuncAnimation(plt.gcf(), update, interval=1000)

plt.gcf().canvas.mpl_connect('key_press_event', on_key)

plt.tight_layout()
plt.show()