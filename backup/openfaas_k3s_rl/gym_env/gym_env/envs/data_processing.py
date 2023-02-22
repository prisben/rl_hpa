import pandas as pd
import time
import numpy as np
from numpy import asarray
from numpy import save
from datetime import datetime
from statistics import mean
from gym_env.envs.test_k8s import get_nodes_avg_cpu, get_nodes_avg_mem, get_deployment_avg_CPU, get_deployment_avg_mem


def get_test_latency(path):
    filename1 = path + "/report1.csv"
    df1 = pd.read_csv(filename1)
    latency_ns = df1['Avg latency'][0]
    resultlat = round(latency_ns / 1000, 3)
    return resultlat

def get_avg_pods(path):
    filename = path + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    avg = mean(list(df['replicas']))
    return avg


def save_qtable(Q_table, path):
    savepath = path + "/QTable.npy"
    save(savepath, asarray(Q_table))


def fetch_nodes_metrics(path, duration_minutes):
    timeout = 60 * duration_minutes
    start_t = int(time.perf_counter())

    datacpu = pd.DataFrame(columns=['time', 'master', 'worker'])
    datamem = pd.DataFrame(columns=['time', 'master', 'worker'])

    while True:
        current = int(time.perf_counter())
        if current >= start_t + timeout:
            break
        cpustats = get_nodes_avg_cpu()
        timestamp = time.time()*1000
        new_row = {'time': timestamp, 'master': cpustats[0], 'worker': cpustats[1]}
        datacpu = datacpu.append(new_row, ignore_index=True)
        memstats = get_nodes_avg_mem()
        new_row_m = {'time': timestamp, 'master': memstats[0], 'worker': memstats[1]}
        datamem = datamem.append(new_row_m, ignore_index=True)
        time.sleep(15)

    path_cpu = path + "/nodes_cpu.csv"
    path_mem = path + "/nodes_mem.csv"
    datacpu.to_csv(path_cpu)
    datamem.to_csv(path_mem)


def fetch_deployment_metrics(path, duration_minutes):
    timeout = 60 * duration_minutes
    start_t = int(time.perf_counter())
    datacpu = pd.DataFrame(columns=['time', 'avg'])
    datamem = pd.DataFrame(columns=['time', 'avg'])

    while True:
        current = int(time.perf_counter())
        if current >= start_t + timeout:
            break
        cpustats = get_deployment_avg_CPU()
        timestamp = time.time()*1000
        new_row = {'time': timestamp, 'avg': cpustats}
        datacpu = datacpu.append(new_row, ignore_index=True)
        memstats = get_deployment_avg_mem()
        new_row_m = {'time': timestamp, 'avg': memstats}
        datamem = datamem.append(new_row_m, ignore_index=True)
        time.sleep(15)

    path_cpu = path + "/deployment_cpu.csv"
    path_mem = path + "/deployment_mem.csv"
    datacpu.to_csv(path_cpu)
    datamem.to_csv(path_mem)

