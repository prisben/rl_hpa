import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from statistics import mean

tot_requests = 44301

basepath = "TRA/evaluation_TRA/"
trainpath = "hpa50/evaluation_hpa50/"
trainpath2 = "hpa80/evaluation_hpa80/"
trainpath3 = "SRA/evaluation_SRA/"
trainpath4 = "TLA/evaluation_TLA/"
trainpathred1 = "hpa50_DSR/evaluation_hpa50_DSR/"
trainpathred2 = "hpa80_DSR/evaluation_hpa80_DSR/"
avg_lat_list = []
avg_lat_list_tr = []
avg_lat_list_tr2 = []
avg_lat_list_tr3 = []
avg_lat_list_tr4 = []
avg_lat_list_trred1 = []
avg_lat_list_trred2 = []
for i in list(range(0, 19)):
        filename = basepath + str(i) + "/report1.csv"
        df = pd.read_csv(filename)
        p1 = int(df['Avg latency']) / 1000
        filename = basepath + str(i) + "/report2.csv"
        df = pd.read_csv(filename)
        p2 = int(df['Avg latency']) / 1000
        avg_lat_list.append((p1 + p2) / 2)
for i in list(range(0, 19)):
    filename = trainpath + str(i) + "/report1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Avg latency']) / 1000
    filename = trainpath + str(i) + "/report2.csv"
    df = pd.read_csv(filename)
    p2 = int(df['Avg latency']) / 1000
    avg_lat_list_tr.append((p1 + p2) / 2)
for i in list(range(0, 19)):
    filename = trainpath2 + str(i) + "/report1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Avg latency']) / 1000
    filename = trainpath2 + str(i) + "/report2.csv"
    df = pd.read_csv(filename)
    p2 = int(df['Avg latency']) / 1000
    avg_lat_list_tr2.append((p1 + p2) / 2)
for i in list(range(0, 19)):
    filename = trainpath3 + str(i) + "/report1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Avg latency']) / 1000
    filename = trainpath3 + str(i) + "/report2.csv"
    df = pd.read_csv(filename)
    p2 = int(df['Avg latency']) / 1000
    avg_lat_list_tr3.append((p1 + p2) / 2)
for i in list(range(0, 19)):
    filename = trainpath4 + str(i) + "/report1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Avg latency']) / 1000
    filename = trainpath4 + str(i) + "/report2.csv"
    df = pd.read_csv(filename)
    p2 = int(df['Avg latency']) / 1000
    avg_lat_list_tr4.append((p1 + p2) / 2)
for i in list(range(0, 19)):
    filename = trainpathred1 + str(i) + "/report1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Avg latency']) / 1000
    filename = trainpathred1 + str(i) + "/report2.csv"
    df = pd.read_csv(filename)
    p2 = int(df['Avg latency']) / 1000
    avg_lat_list_trred1.append((p1 + p2) / 2)
for i in list(range(0, 19)):
    filename = trainpathred2 + str(i) + "/report1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Avg latency']) / 1000
    filename = trainpathred2 + str(i) + "/report2.csv"
    df = pd.read_csv(filename)
    p2 = int(df['Avg latency']) / 1000
    avg_lat_list_trred2.append((p1 + p2) / 2)


meanlat = [avg_lat_list,  avg_lat_list_tr, avg_lat_list_tr2]

fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
left, right = plt.xlim()
plt.hlines(1000, xmin=left, xmax=right, color='r', linestyles='--')
ax.set_xticklabels(['TRA', 'HPA 50%', 'HPA 80%'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('LATENCY [ms]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("AVERAGE LATENCY", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [avg_lat_list,  avg_lat_list_trred1, avg_lat_list_trred2]

fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
left, right = plt.xlim()
plt.hlines(1000, xmin=left, xmax=right, color='r', linestyles='--')
ax.set_xticklabels(['TRA', 'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('LATENCY [ms]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("AVERAGE LATENCY", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()

meanlat = [avg_lat_list,  avg_lat_list_tr, avg_lat_list_tr2, avg_lat_list_trred1, avg_lat_list_trred2]

fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
left, right = plt.xlim()
plt.hlines(1000, xmin=left, xmax=right, color='r', linestyles='--')
ax.set_xticklabels(['TRA', 'HPA 50%', 'HPA 80%', 'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('LATENCY [ms]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("AVERAGE LATENCY", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [avg_lat_list, avg_lat_list_tr4, avg_lat_list_tr3]

fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
left, right = plt.xlim()
plt.hlines(1000, xmin=left, xmax=right, color='r', linestyles='--')
ax.set_xticklabels(['TRA', 'TLA', 'SRA'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('LATENCY [ms]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
#plt.title("AVERAGE LATENCY", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


rep = []
rep_tr = []
rep_tr2 = []
rep_tr3 = []
rep_tr4 = []
rep_trred1 = []
rep_trred2 = []
cpu_avg = []
mem_avg = []
cpu_avg_tr = []
mem_avg_tr = []
cpu_avg_tr2 = []
mem_avg_tr2 = []
cpu_avg_tr3 = []
mem_avg_tr3 = []
cpu_avg_tr4 = []
mem_avg_tr4 = []
cpu_avg_trred1 = []
mem_avg_trred1 = []
cpu_avg_trred2 = []
mem_avg_trred2 = []



for i in list(range(0, 19)):
    filename = basepath + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    cpu = df['avg'].mean()
    cpu_avg.append(cpu)
    r = math.ceil(df['replicas'].mean())
    rep.append(r)
    filename2 = basepath + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg.append(mem)

for i in list(range(0, 19)):
    filename = trainpath + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    r = math.ceil(df['replicas'].mean())
    rep_tr.append(r)
    cpu = df['avg'].mean()
    cpu_avg_tr.append(cpu)
    filename2 = trainpath + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg_tr.append(mem)

for i in list(range(0, 19)):
    filename = trainpath2 + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    r = math.ceil(df['replicas'].mean())
    rep_tr2.append(r)
    cpu = df['avg'].mean()
    cpu_avg_tr2.append(cpu)
    filename2 = trainpath2 + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg_tr2.append(mem)

for i in list(range(0, 19)):
    filename = trainpath3 + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    r = math.ceil(df['replicas'].mean())
    rep_tr3.append(r)
    cpu = df['avg'].mean()
    cpu_avg_tr3.append(cpu)
    filename2 = trainpath3 + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg_tr3.append(mem)

for i in list(range(0, 19)):
    filename = trainpath4 + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    r = math.ceil(df['replicas'].mean())
    rep_tr4.append(r)
    cpu = df['avg'].mean()
    cpu_avg_tr4.append(cpu)
    filename2 = trainpath4 + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg_tr4.append(mem)

for i in list(range(0, 19)):
    filename = trainpathred1 + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    r = math.ceil(df['replicas'].mean())
    rep_trred1.append(r)
    cpu = df['avg'].mean()
    cpu_avg_trred1.append(cpu)
    filename2 = trainpathred1 + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg_trred1.append(mem)

for i in list(range(0, 19)):
    filename = trainpathred2 + str(i) + "/deployment_cpu.csv"
    df = pd.read_csv(filename)
    r = math.ceil(df['replicas'].mean())
    rep_trred2.append(r)
    cpu = df['avg'].mean()
    cpu_avg_trred2.append(cpu)
    filename2 = trainpathred2 + str(i) + "/deployment_mem.csv"
    df2 = pd.read_csv(filename2)
    mem = df2['avg'].mean()
    mem_avg_trred2.append(mem)



meanlat = [cpu_avg,  cpu_avg_tr, cpu_avg_tr2]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA', 'HPA 50%', 'HPA 80%'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MILLICORES [m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT CPU USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [rep,  rep_tr, rep_tr2]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA',  'HPA 50%', 'HPA 80%'], fontsize=18)
plt.yticks(fontsize=18)
#plt.ylabel('[m]', fontsize=18)
plt.ylabel('REPLICAS', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("REPLICAS", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [mem_avg,  mem_avg_tr, mem_avg_tr2]



fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA',  'HPA 50%', 'HPA 80%'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MEMORY [MB]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT MEMORY USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()

meanlat = [cpu_avg,  cpu_avg_trred1, cpu_avg_trred2]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA', 'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MILLICORES [m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT CPU USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [rep,  rep_trred1, rep_trred2]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA',  'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
#plt.ylabel('[m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("REPLICAS", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [mem_avg,  mem_avg_trred1, mem_avg_trred2]



fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA',  'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MEMORY [MB]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT MEMORY USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()

meanlat = [cpu_avg,  cpu_avg_tr, cpu_avg_tr2, cpu_avg_trred1, cpu_avg_trred2]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA', 'HPA 50%', 'HPA 80%', 'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MILLICORES [m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT CPU USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [rep,  rep_tr, rep_tr2, rep_trred1, rep_trred2]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA',  'HPA 50%', 'HPA 80%', 'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('REPLICAS', fontsize=18)
#plt.ylabel('[m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
#plt.title("REPLICAS", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [mem_avg,  mem_avg_tr, mem_avg_tr2, mem_avg_trred1, mem_avg_trred2]



fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA',  'HPA 50%', 'HPA 80%', 'HPA 50% DSR', 'HPA 80% DSR'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MEMORY [MB]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT MEMORY USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [cpu_avg, cpu_avg_tr4, cpu_avg_tr3]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA', 'TLA', 'SRA'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MILLICORES [m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
plt.title("DEPLOYMENT CPU USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [rep, rep_tr4, rep_tr3]


fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA', 'TLA', 'SRA'], fontsize=18)
plt.ylabel('REPLICAS', fontsize=18)
plt.yticks(fontsize=18)
#plt.ylabel('[m]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
#plt.title("REPLICAS", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


meanlat = [mem_avg, mem_avg_tr4, mem_avg_tr3]



fig, ax = plt.subplots()
ax.boxplot(meanlat, autorange='True', showmeans='True')
ax.set_xticklabels(['TRA', 'TLA', 'SRA'], fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('MEMORY [MB]', fontsize=18)
#plt.xlabel('Test ', fontsize=18)
#plt.title("DEPLOYMENT MEMORY USAGE", fontsize=18)
plt.axis(ymin=0)
plt.grid()
plt.show()


timeout_base = []
timeout_tr = []
timeout_tr2= []
timeout_tr3= []
timeout_tr4= []
timeout_trred1= []
timeout_trred2= []
for i in list(range(0, 19)):
    filename = basepath + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_base.append(p1)
for i in list(range(0, 19)):
    filename = trainpath + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_tr.append(p1)
for i in list(range(0, 19)):
    filename = trainpath2 + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_tr2.append(p1)
for i in list(range(0, 19)):
    filename = trainpath3 + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_tr3.append(p1)
for i in list(range(0, 19)):
    filename = trainpath4 + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_tr4.append(p1)
for i in list(range(0, 19)):
    filename = trainpathred1 + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_trred1.append(p1)
for i in list(range(0, 19)):
    filename = trainpathred2 + str(i) + "/summary1.csv"
    df = pd.read_csv(filename)
    p1 = int(df['Total completed'])
    timeout_trred2.append(p1)


avg_t = (100*(tot_requests-sum(timeout_base)))/tot_requests
avg_t_tr = (100*(tot_requests-sum(timeout_tr)))/tot_requests
avg_t_tr2 = (100*(tot_requests-sum(timeout_tr2)))/tot_requests
avg_t_tr3 = (100*(tot_requests-sum(timeout_tr3)))/tot_requests
avg_t_tr4 = (100*(tot_requests-sum(timeout_tr4)))/tot_requests
avg_t_trred1 = (100*(tot_requests-sum(timeout_trred1)))/tot_requests
avg_t_trred2 = (100*(tot_requests-sum(timeout_trred2)))/tot_requests

types = ['TRA',  'HPA 50%', 'HPA 80%']
values = [avg_t, avg_t_tr, avg_t_tr2]
#x_pos = [0, 0.5]
x_axis = np.arange(len(types))
plt.bar(x_axis, values, width=0.2, color='red',zorder=3)
plt.ylabel('LOSS [%]', fontsize=18)
plt.xticks(x_axis, types, fontsize=18)
plt.yticks(fontsize=18)
plt.title("LOSS PERCENTAGE",fontsize=18)
plt.axis(ymin=0)
plt.grid(zorder=0)
plt.show()



types = ['TRA',  'HPA 50%', 'HPA 80%', 'HPA 50% DSR', 'HPA 80% DSR']
values = [avg_t,  avg_t_tr, avg_t_tr2, avg_t_trred1, avg_t_trred2]
#x_pos = [0, 0.5]
x_axis = np.arange(len(types))
plt.bar(x_axis, values, width=0.2, color='red',zorder=3)
plt.ylabel('LOSS [%]', fontsize=18)
plt.xticks(x_axis, types, fontsize=18)
plt.yticks(fontsize=18)
plt.title("LOSS PERCENTAGE",fontsize=18)
plt.axis(ymin=0)
plt.grid(zorder=0)
plt.show()


types = ['TRA',  'HPA 50% DSR', 'HPA 80% DSR']
values = [avg_t, avg_t_trred1, avg_t_trred2]
#x_pos = [0, 0.5]
x_axis = np.arange(len(types))
plt.bar(x_axis, values, width=0.2, color='red',zorder=3)
plt.ylabel('LOSS [%]', fontsize=18)
plt.xticks(x_axis, types, fontsize=18)
plt.yticks(fontsize=18)
plt.title("LOSS PERCENTAGE",fontsize=18)
plt.axis(ymin=0)
plt.grid(zorder=0)
plt.show()



types = ['TRA', 'TLA', 'SRA']
values = [avg_t, avg_t_tr4, avg_t_tr3]
#x_pos = [0, 0.5]
x_axis = np.arange(len(types))
plt.bar(x_axis, values, width=0.2, color='red',zorder=3)
plt.ylabel('LOSS [%]', fontsize=18)
plt.xticks(x_axis, types, fontsize=18)
plt.yticks(fontsize=18)
plt.title("LOSS PERCENTAGE",fontsize=18)
plt.axis(ymin=0)
plt.grid(zorder=0)
plt.show()
