import re
import shlex
import subprocess


def process_count(username: str) -> int:
    # к-во процессов, запущенных из-под текущего пользователя
    result = 0
    command = shlex.split(f"ps -u {username}")
    processes = subprocess.run(command, capture_output=True, text=True)
    for _ in processes.stdout.splitlines():
        result += 1
    return result - 1


def total_memory_usage(root_pid: int) -> int:
    # суммарное потребление памяти древа процессов
    command = shlex.split(f'pstree -up {root_pid}')
    processes = subprocess.run(command, capture_output=True, text=True)
    result = re.findall(r'\b\d{5}\b', processes.stdout)
    pids = list(map(int, set(result)))
    total_rss = 0
    for pid in pids:
        com = shlex.split(f'ps -o rss {pid}')
        proc = subprocess.run(com, capture_output=True, text=True)
        rss_pid = re.findall(r'\b\d{4,7}\b', proc.stdout)
        if len(rss_pid) == 1:
            total_rss += int(rss_pid[0])
    return total_rss


if __name__ == '__main__':
    name = input("input username: ")
    print(f'к-во процессов, запущенных из-под текущего пользователя: {process_count(username=name)}')
    print(f'суммарное потребление памяти древа процессов: {total_memory_usage(1)}')
