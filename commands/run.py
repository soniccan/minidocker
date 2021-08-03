from typing import List
from pprint import pprint
import linux
import os
import commands.cgroup as cgroup
import commands.local as local
import commands.data as data
import uuid


def child_proc_callback(option:dict):
    pid = os.getpid()
    cpu = option['cpu']
    command = option['command']

    linux.sethostname('childprocess')

    if cpu:
        cg = cgroup.CGroup('hoge')
        cg.set_cpu_limit(cpu)
        cg.add(pid)
    

    utc = os.uname()[1]
    # print(pid)
    # ここに3-2~3-3
    images = local.find_images()

    for index in range(len(images)):

        if images[index].name == os.path.join("library",command[0]):
            image =images[index]
            
    # image = images[0]
    # tmp ="var/opt/app/container"
    # dir = os.path.join(tmp,f"{ image.name.replace('/','_') }_{ image.version }_{ uuid.uuid4() }")
    # workdir =os.path.join(dir,"work")
    # rw_dir =os.path.join(dir,"rw")
    
    container = data.Container.init_from_image(image)
    # pprint(vars(container))
    rootdir = container.root_dir
    upperdir = container.rw_dir
    workdir = container.work_dir
    lowerdir = image.content_dir
    
    linux.mount('overlay',rootdir,'overlay',linux.MS_NODEV,f"lowerdir={lowerdir},upperdir={upperdir},workdir={workdir}")
    
    os.chdir(rootdir)
    os.chroot(rootdir)
    pprint(container)
    os.execvp(command[0],command)


def exec_run(cpu:float,command:List[str]):
    # print(f'run command called!')
   
    flags = 1
    option = {'command':command,'cpu':cpu}
    pid = linux.clone(child_proc_callback,linux.CLONE_NEWUTS and linux.CLONE_NEWPID,(option,))
    
    os.waitpid(pid,0)
    