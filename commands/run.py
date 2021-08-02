from typing import List
import linux
import os
import commands.cgroup as cgroup
import commands.local as local

def child_proc_callback(option:dict):
    pid = os.getpid()
    cpu = option['cpu']

    linux.sethostname('childprocess')

    if cpu:
        cg = cgroup.CGroup('hoge')
        cg.set_cpu_limit(cpu)
        cg.add(pid)
    

    utc = os.uname()[1]
   
    # print(pid)
    # ここに3-2~3-3
    images = local.find_images()

    




    command = option['command']
    os.execvp(command[0],command)

    

def exec_run(cpu:float,command:List[str]):
    # print(f'run command called!')
   
    flags = 1
    option = {'command':command,'cpu':cpu}
    pid = linux.clone(child_proc_callback,linux.CLONE_NEWUTS and linux.CLONE_NEWPID,(option,))
    
    os.waitpid(pid,0)
    