from gym_env.envs.test_k8s import get_deployment_avg_CPU, get_deployment_avg_mem, get_hpa_current_replicas
import time
import numpy as np
import pandas as pd
import sys
import os


#### save cpu and memory stats for a namespace (set in gym_env/gym_env/envs/test_k8s.py)

path = sys.argv[1] #csv destination path
duration_minutes = int(sys.argv[2]) #measurement duration (minutes)

timeout = 60 * duration_minutes
start_t = int(time.perf_counter())
rows_cpu = []
rows_mem = []



while True:
    current = int(time.perf_counter())
    if current >= start_t + int(timeout) - 15:
        break
    dict_cpu = {}
    dict_mem = {}
    dict_hpa = {}
    cpustats, rep, single = get_deployment_avg_CPU()
    os.system("echo \"{}-------------------------------------------------------------------------------\" >> {}/hpalog.txt".format(step,path))
    os.system("kubectl describe hpa namehpa -n namespace >> {}/hpalog.txt".format(path)) #print hpa log
    timestamp = time.time()*1000
    cpu_row = {'time': timestamp, 'avg': cpustats, 'replicas': rep, 'for pod':  single}
    dict_cpu.update(cpu_row)
    memstats, rep, single = get_deployment_avg_mem()
    mem_row = {'time': timestamp, 'avg': memstats, 'replicas': rep, 'for pod':  single}
    dict_mem.update(mem_row)
    rows_cpu.append(dict_cpu)
    rows_mem.append(dict_mem)
    time.sleep(15) #metrics server granularity

datacpu = pd.DataFrame(rows_cpu, columns=['time', 'avg', 'replicas', 'for pod'])
datamem = pd.DataFrame(rows_mem, columns=['time', 'avg', 'replicas', 'for pod'])
path_cpu = path + "/deployment_cpu.csv"
path_mem = path + "/deployment_mem.csv"
datacpu.to_csv(path_cpu)
datamem.to_csv(path_mem)
print("DONE!")
