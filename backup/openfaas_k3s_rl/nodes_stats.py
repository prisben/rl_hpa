from gym_env.envs.test_k8s import get_nodes_avg_cpu, get_nodes_avg_mem
import time
import pandas as pd
import sys

######### example for two nodes cluster (master,worker), change with nodes' names

duration_minutes = int(sys.argv[2]) ##duration in minutes of the measurement
path = sys.argv[1] #csv destination path
timeout = 60 * duration_minutes
start_t = int(time.perf_counter())


rows_cpu = []
rows_mem = []

while True:
    current = int(time.perf_counter())
    if current >= start_t + int(timeout):
        break
    dict_cpu = {}
    dict_mem = {}
    cpustats = get_nodes_avg_cpu()
    timestamp = time.time()*1000
    new_row = {'time': timestamp, 'master': cpustats[0], 'worker': cpustats[1]}
    dict_cpu.update(new_row)
    memstats = get_nodes_avg_mem()
    new_row_m = {'time': timestamp, 'master': memstats[0], 'worker': memstats[1]}
    dict_cpu.update(new_row_m)
    rows_cpu.append(dict_cpu)
    rows_mem.append(dict_mem)
    time.sleep(15)  #metric server granularity

datacpu = pd.DataFrame(rows_cpu,columns=['time','master','worker'])
datamem = pd.DataFrame(rows_mem,columns=['time','master','worker'])
path_cpu = path + "/nodes_cpu.csv"
path_mem = path + "/nodes_mem.csv"
datacpu.to_csv(path_cpu)
datamem.to_csv(path_mem)
print("DONE!")
