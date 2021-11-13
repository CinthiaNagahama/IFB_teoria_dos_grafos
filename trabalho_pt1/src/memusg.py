#!/usr/bin/env python3
import sys
import os
from time import sleep
from subprocess import Popen, PIPE


def log(*args):
    if DEBUG:
        print(*args)


def get_rssize(sid: int, *ignore_comms: str) -> int:
    rssize = 0

    # Example: /bin/ps -o rssize= -o cmd= --sid 23928 -> [(xxxx)kb, full command]
    proc = Popen(
        ["ps", "-o", "rss=", "-o", "cmd=", "--sid", str(sid)], stdout=PIPE, stderr=None, shell=False, text=True
    )
    stdout, _ = proc.communicate()

    # Iterate over each process within the process tree of our process session
    # (this ensures that we include processes launched by a child bash script, etc.)
    process_lines = [line.split() for line in stdout.split("\n") if len(line) > 0]
    log("all processes:", process_lines)
    for line in process_lines:
        if all(comm not in line for comm in ignore_comms):
            log("measured process:", line)
            rssize += int(line[0])

    return rssize


DEBUG = False
try:
    command = sys.argv[0]
    if sys.argv[-1] in ("-d", "--debug"):
        DEBUG = True
        child_command = sys.argv[1:-1]
    else:
        child_command = sys.argv[1:]

except IndexError:
    print("Argument(s) is missing")
    sys.exit()


log(command, child_command)

# Create a new process session for this process so that we can
# easily calculate the memory usage of the whole process tree using ps
#
# Since we need a new session using os.setsid(), we must first fork()
pid = os.getpid()
sid = os.getsid(pid)

fork_pid = os.fork()
if fork_pid == 0:
    # We *are* the new fork (not the original process)
    pid = os.getpid()
    sid = os.getsid(pid)

    os.setsid()
    sid = os.getsid(pid)

    proc = Popen(child_command, stdin=None, stdout=PIPE, stderr=None, env=None, shell=False, text=True)

    rsspeak = -1
    while proc.returncode is None:
        rsspeak = max(get_rssize(sid, command, "ps"), rsspeak)
        proc.poll()
        sleep(0.001)  # Time in seconds (float)

    print(rsspeak)

    status = proc.returncode
    sys.exit(status)

else:
    # This is the branch of fork that continues the original process
    _, full_status = os.waitpid(fork_pid, 0)
    status = full_status >> 8
    sys.exit(status)
