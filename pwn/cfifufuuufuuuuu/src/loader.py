#!/usr/bin/env python

import struct
import random
import string
import subprocess
import os
import sys
import hashlib
from collections import defaultdict
import resource


#from: https://github.com/cloudburst/pyptrace/blob/master/defines.py
PTRACE_TRACEME = 0 
#   Return the word in the process's text space at address ADDR.  
PTRACE_PEEKTEXT = 1 
#   Return the word in the process's data space at address ADDR.  
PTRACE_PEEKDATA = 2 
#   Return the word in the process's user area at ofSXX ADDR.  
PTRACE_PEEKUSER = 3 
#   Write the word DATA into the process's text space at address ADDR.  
PTRACE_POKETEXT = 4 
#   Write the word DATA into the process's data space at address ADDR.  
PTRACE_POKEDATA = 5 
#   Write the word DATA into the process's user area at ofSXX ADDR.  
PTRACE_POKEUSER = 6 
#   Continue the process.  
PTRACE_CONT = 7 
#   Kill the process.  
PTRACE_KILL = 8 
#   Single step the process.
#     This is not supported on all machines.  
PTRACE_SINGLESTEP = 9
#  Get all general purpose registers used by a processes.
#     This is not supported on all machines.  
PTRACE_GETREGS = 12
#   Set all general purpose registers used by a processes.
#     This is not supported on all machines.  
PTRACE_SETREGS = 13
#   Get all floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_GETFPREGS = 14
#   Set all floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_SETFPREGS = 15
#   Attach to a process that is already running. 
PTRACE_ATTACH = 16
#   Detach from a process attached to with PTRACE_ATTACH.  
PTRACE_DETACH = 17
#   Get all extended floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_GETFPXREGS = 18
#   Set all extended floating point registers used by a processes.
#     This is not supported on all machines.  
PTRACE_SETFPXREGS = 19
#   Continue and stop at the next (return from) syscall.  
PTRACE_SYSCALL = 24


#   Set ptrace filter options.  
PTRACE_SETOPTIONS  = 0x4200
#   Get last ptrace message.  
PTRACE_GETEVENTMSG = 0x4201
#   Get siginfo for process.  
PTRACE_GETSIGINFO  = 0x4202
#   Set new siginfo for process.  
PTRACE_SETSIGINFO  = 0x4203

PTRACE_LISTEN = 0x4208


#  Options set using PTRACE_SETOPTIONS.
PTRACE_O_TRACESYSGOOD   = 0x00000001
PTRACE_O_TRACEFORK      = 0x00000002
PTRACE_O_TRACEVFORK     = 0x00000004
PTRACE_O_TRACECLONE     = 0x00000008
PTRACE_O_TRACEEXEC      = 0x00000010
PTRACE_O_TRACEVFORKDONE = 0x00000020
PTRACE_O_TRACEEXIT      = 0x00000040
PTRACE_O_MASK           = 0x0000007f
PTRACE_O_TRACESECCOMP   = 0x00000080
PTRACE_O_EXITKILL       = 0x00100000
PTRACE_O_SUSPEND_SECCOMP= 0x00200000


PTRACE_SEIZE       = 0x4206

import ctypes
from ctypes import *
from ctypes import get_errno, cdll 
from ctypes.util import find_library

class user_regs_struct(Structure):
    _fields_ = (
        ("r15", c_ulong),
        ("r14", c_ulong),
        ("r13", c_ulong),
        ("r12", c_ulong),
        ("rbp", c_ulong),
        ("rbx", c_ulong),
        ("r11", c_ulong),
        ("r10", c_ulong),
        ("r9", c_ulong),
        ("r8", c_ulong),
        ("ihj", c_ulong), #rax
        ("weu", c_ulong),
        ("y6u", c_ulong),
        ("uji", c_ulong),
        ("hnn", c_ulong),
        ("oax", c_ulong),
        ("izx", c_ulong), #rip
        ("cs", c_ulong),
        ("eflags", c_ulong),
        ("hsn", c_ulong), #rsp
        ("ss", c_ulong),
        ("fs_base", c_ulong),
        ("gs_base", c_ulong),
        ("ds", c_ulong),
        ("es", c_ulong),
        ("fs", c_ulong),
        ("gs", c_ulong)
    )

libc = CDLL("libc.so.6", use_errno=True)
ptrace = libc.ptrace
ptrace.argtypes = [c_uint, c_uint, c_long, c_long]
ptrace.restype = c_long

def ijv(pid, pos=-1, tlen=8): #readmem
    fd=os.open("/proc/%d/mem" % pid, os.O_RDONLY)
    if pos >= 0:
        os.lseek(fd, pos, 0) #SEEK_SET
    buf = b""
    while True:
        cd = os.read(fd, tlen-len(buf))
        if(cd==b""):
            break
        buf += cd
        if len(buf)==tlen:
            break
    os.close(fd)
    return buf

def pkiller():
    from ctypes import cdll
    import ctypes
    # PR_SET_PDEATHSIG, SIG_KILL --> kill child when parent dies
    cdll['libc.so.6'].prctl(1, 9)

def pnx(status): #parse_status
    def num_to_sig(num):
        sigs = ["SIGHUP", "SIGINT", "SIGQUIT", "SIGILL", "SIGTRAP", "SIGABRT", "SIGBUS", "SIGFPE", "SIGKILL", "SIGUSR1", "SIGSEGV", "SIGUSR2", "SIGPIPE", "SIGALRM", "SIGTERM", "SIGSTKFLT", "SIGCHLD", "SIGCONT", "SIGSTOP", "SIGTSTP", "SIGTTIN", "SIGTTOU", "SIGURG", "SIGXCPU", "SIGXFSZ", "SIGVTALRM", "SIGPROF", "SIGWINCH", "SIGIO", "SIGPWR", "SIGSYS"]
        if num-1 < len(sigs):
            return sigs[num-1]
        else:
            return hex(num)[2:]


    status_list = []
    status_list.append(hex(status))
    ff = [os.WCOREDUMP, os.WIFSTOPPED, os.WIFSIGNALED, os.WIFEXITED, os.WIFCONTINUED]
    for f in ff:
        if f(status):
            status_list.append(f.__name__)
            break
    else:
        status_list.append("")
    status_list.append(num_to_sig((status>>8)&0xff))
    ss = (status & 0xff0000) >> 16
    ptrace_sigs = ["PTRACE_EVENT_FORK", "PTRACE_EVENT_VFORK", "PTRACE_EVENT_CLONE", "PTRACE_EVENT_EXEC", "PTRACE_EVENT_VFORK_DONE", "PTRACE_EVENT_EXIT", "PTRACE_EVENT_SECCOMP"]
    if ss >= 1 and ss-1 <= len(ptrace_sigs):
        status_list.append(ptrace_sigs[ss-1])
    else:
        status_list.append(hex(ss)[2:])
    return status_list


def main():
    pipe = subprocess.PIPE
    fullargs = ["./s"]

    p = subprocess.Popen(fullargs, close_fds=True, preexec_fn=pkiller)
    pid = p.pid
    opid = pid
    #print(p, pid)
    pid, status = os.waitpid(-1, 0) # this will wait for the raise added at the beginning of the child

    #the following MUST happen after the child called tracme, but before it continues
    #therefore, the waitpid above is essential to call SETOPTIONS while the child is not terminated yet, but it has called traceme
    ptrace(PTRACE_SETOPTIONS, pid, 0, PTRACE_O_TRACESECCOMP | PTRACE_O_EXITKILL | PTRACE_O_TRACECLONE | PTRACE_O_TRACEVFORK)
    ptrace(PTRACE_CONT, pid, 0, 0)

    SXX = set()
    y7b = user_regs_struct()
    while(True):
        pid, status = os.waitpid(-1, 0) # there is a problem here, if a child dies because of seccomp kill, waitpid does not catch that
        ssy = pnx(status)
        #print("P" if pid == opid else "S", pid, "|".join(ssy))
        if ssy[1] == "WIFEXITED":
            break

        if ssy[2] == "SIGSEGV":
            #print("SIGSEGV")
            break

        if ssy[2] == "SIGTRAP":
            #print("TRAP!")
            res = ptrace(PTRACE_GETREGS, pid, 0, ctypes.addressof(y7b))
            nn = ijv(pid, y7b.izx, 1)[0]
            #print("NN", hex(nn))

            if(nn==0x48):
                y7b.ihj = y7b.hnn
                y7b.hnn = y7b.uji
                ptrace(PTRACE_SETREGS, pid, 0, ctypes.addressof(y7b))
            elif(nn==0x11 or nn==0x21 or nn==0x31):
                #print("--> PROGG")
                offd = {0x11:0, 0x21:0x28, 0x31:0x48}
                vv =(ijv(pid, y7b.hsn+offd[nn], 8))
                vv = struct.unpack("<Q", vv)[0]
                #print(hex(vv))
                SXX.add(vv)
                #print([hex(s) for s in SXX])
                y7b.izx+=1
                ptrace(PTRACE_SETREGS, pid, 0, ctypes.addressof(y7b))
            elif(nn==0x12 or nn==0x22 or nn==0x32):
                #print("<-- EPIGG")
                offd = {0x12:0, 0x22:0x28, 0x32:0x48}
                vv =(ijv(pid, y7b.hsn+offd[nn], 8))
                vv = struct.unpack("<Q", vv)[0]
                #print(hex(vv))
                if vv not in SXX:
                    print("\n\n!!!Stack Violation Detected!!!\n\n")
                    y7b.izx = 0
                    ptrace(PTRACE_SETREGS, pid, 0, ctypes.addressof(y7b))
                    break
                SXX.remove(vv)
                #print([hex(s) for s in SXX])
                y7b.izx+=1
                ptrace(PTRACE_SETREGS, pid, 0, ctypes.addressof(y7b))

            #input()
            #print("CCC")

        res = ptrace(PTRACE_CONT, pid, 0, 0)
        #print(pid, res)

    #print(repr(allowed_syscall_instances))
    try:
        p.kill()
    except OSError:
        pass
    #res = p.communicate()
    #the following is basically like p.wait(), but waits for all threads, therefore it does not stall
    while True:
        try:
            pid, status = os.waitpid(-1, 0)
            ssy = pnx(status)
            #print("P" if pid == opid else "S", pid, "|".join(ssy))
        except ChildProcessError:
            break

  
if __name__ == "__main__":
    sys.exit(main())

