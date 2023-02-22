import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean



cpu_list = []
mem_list = []
hpa_list = []
replicas_cpu = []
replicas_mem = []
avg_cpu = []
filename = "50/0/deployment_cpu.csv"
filename2 = "50/0/rep_hpa.csv"
df = pd.read_csv(filename)
df2 = pd.read_csv(filename2)
cpu = list(df['avg'])
rc = list(df['replicas'])
hpa_r = list(df2['observed'])
for h in hpa_r:
    hpa_list.append(h)
for n in cpu:
    if math.isnan(n):
        cpu_list.append(0)
    else:
        cpu_list.append(n)
for r in rc:
    if math.isnan(r):
        replicas_cpu.append(0)
    else:
        replicas_cpu.append(r)
for i in range(len(replicas_cpu)):
    avg_cpu.append(cpu_list[i]/replicas_cpu[i])

filename2 = "50/0/deployment_mem.csv"
df2 = pd.read_csv(filename2)
mem = list(df2['avg'])
rm = list(df2['replicas'])
for n in mem:
    if math.isnan(n):
        mem_list.append(0)
    else:
        mem_list.append(n)
for r in rm:
    if math.isnan(r):
        replicas_mem.append(0)
    else:
        replicas_mem.append(r)

x_axis_cpu = np.arange(len(cpu_list))


fig,ax = plt.subplots()
lns1=ax.plot(x_axis_cpu, cpu_list, linestyle='--', marker='o', color="red",label='Average CPU usage')
# set x-axis label
ax.set_xlabel("STEPS [EACH 15 s]", fontsize=18)
# set y-axis label
ax.set_ylabel("MILLICORES [m]", color='red', fontsize=18)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
lns2=ax2.plot(x_axis_cpu, replicas_cpu, linestyle='--', marker='o', color="blue", label='Active replicas')
lns3=ax2.plot(x_axis_cpu, hpa_list, linestyle='--', marker='o', color="black", label='HPA currentReplicas')
ax2.set_ylabel("REPLICAS", color='blue', fontsize=18)
v=ax2.axvline(8, color='green', linestyle='--', label='Test start')
#plt.title("DEPLOYMENT CPU CONSUMPTION (HPA 50%)", fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.axis(ymin=0, xmin=0, xmax=x_axis_cpu[-1])
plt.yticks(fontsize=18)
lns = lns1+lns2+lns3+[v]
labs = [l.get_label() for l in lns]
labs.append(v.get_label())
plt.legend(lns, labs, fontsize=16, loc='upper right')
#plt.legend(labs, fontsize=16, loc='upper right')
#plt.legend(fontsize=16, loc='upper right')
#ax.set_xticks(np.arange(len(x_axis_cpu)), fontsize=18)
plt.grid()
plt.show()

THRS = [25.0]*len(avg_cpu)
x_axis_cpu = np.arange(len(avg_cpu))
plt.plot(x_axis_cpu, avg_cpu, linestyle='--', marker='o', color="green", label='Average CPU usage')
plt.plot(x_axis_cpu, THRS, color="red", label="Threshold")
plt.axvline(8, color='purple', linestyle='--', label='Test start')
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
plt.legend(fontsize=16, loc='upper right')
plt.axis(ymin=0)
plt.axis(ymin=0, xmin=0, xmax=x_axis_cpu[-1])
plt.xlabel("STEPS [EACH 15 s]", fontsize=18)
plt.ylabel("MILLICORES [m]", fontsize=18)
#plt.title("AVERAGE POD CPU CONSUMPTION (HPA 50%)", fontsize=18)
plt.grid()
plt.show()


x_axis_mem = np.arange(len(mem_list))
fig,ax = plt.subplots()
ax.plot(x_axis_mem, mem_list, linestyle='--', marker='o', color="red")
# set x-axis label
ax.set_xlabel("STEPS [EACH 15 s]", fontsize=18)
# set y-axis label
ax.set_ylabel("MEMORY USAGE [MB]", color='red', fontsize=18)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(x_axis_mem, replicas_mem, linestyle='--', marker='o', color="blue")
plt.axvline(8, color='purple', label='START TEST')
ax2.set_ylabel("REPLICAS", color='blue', fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.yticks(fontsize=18)
plt.axis(ymin=0, xmin=0, xmax=x_axis_cpu[-1])
#ax.set_xticks(np.arange(len(x_axis_mem)), fontsize=18)
plt.title("DEPLOYMENT MEMORY CONSUMPTION (HPA 50%)", fontsize=18)
plt.legend()
plt.grid()
plt.show()

cpu_list = []
mem_list = []
replicas_cpu = []
replicas_mem = []
avg_cpu=[]

filename = "80/0/deployment_cpu.csv"
df = pd.read_csv(filename)
cpu = list(df['avg'])
rc = list(df['replicas'])
for n in cpu:
    if math.isnan(n):
        cpu_list.append(0)
    else:
        cpu_list.append(n)
for r in rc:
    if math.isnan(r):
        replicas_cpu.append(0)
    else:
        replicas_cpu.append(r)
for i in range(len(replicas_cpu)):
    avg_cpu.append(cpu_list[i]/replicas_cpu[i])

hpa_list = []
filename2 = "80/0/deployment_mem.csv"
filename3 = "80/0/rep_hpa.csv"
df3 = pd.read_csv(filename3)
df2 = pd.read_csv(filename2)
mem = list(df2['avg'])
rm = list(df2['replicas'])
hpa_r = list(df3['observed'])
for h in hpa_r:
    hpa_list.append(h)
for n in mem:
    if math.isnan(n):
        mem_list.append(0)
    else:
        mem_list.append(n)
for r in rm:
    if math.isnan(r):
        replicas_mem.append(0)
    else:
        replicas_mem.append(r)

x_axis_cpu = np.arange(len(cpu_list))


fig,ax = plt.subplots()
lns1=ax.plot(x_axis_cpu, cpu_list, linestyle='--', marker='o', color="red",label='Average CPU usage')
# set x-axis label
ax.set_xlabel("STEPS [EACH 15 s]", fontsize=18)


# set y-axis label
ax.set_ylabel("MILLICORES [m]", color='red', fontsize=18)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
lns2=ax2.plot(x_axis_cpu, replicas_cpu, linestyle='--', marker='o', color="blue", label='Active replicas')
lns3=ax2.plot(x_axis_cpu, hpa_list, linestyle='--', marker='o', color="black", label='HPA currentReplicas')
v=ax2.axvline(8, color='green', linestyle='--', label='Test start')
ax2.set_ylabel("REPLICAS", color='blue', fontsize=18)
#plt.title("DEPLOYMENT CPU CONSUMPTION (HPA 80%)", fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.yticks(fontsize=18)
plt.axis(ymin=0)
plt.axis(ymin=0, xmin=0, xmax=x_axis_cpu[-1])
#ax.set_xticks(np.arange(len(x_axis_cpu)), fontsize=18)
lns = lns1+lns2+lns3+[v]
labs = [l.get_label() for l in lns]
labs.append(v.get_label())
plt.legend(lns, labs, fontsize=16, loc='lower center')
plt.grid()
plt.show()

THRS = [40.0]*len(avg_cpu)
x_axis_cpu = np.arange(len(avg_cpu))
plt.plot(x_axis_cpu, avg_cpu, linestyle='--', marker='o', color="green", label='Average CPU usage')
plt.axvline(8, color='purple', linestyle='--', label='Test start')
plt.plot(x_axis_cpu, THRS, color="red", label="Threshold")
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
plt.legend(fontsize=18)
plt.axis(ymin=0)
plt.axis(ymin=0, xmin=0, xmax=x_axis_cpu[-1])
plt.xlabel("STEPS [EACH 15 s]", fontsize=18)
plt.ylabel("MILLICORES [m]", fontsize=18)
#plt.title("AVERAGE POD CPU CONSUMPTION (HPA 80%)", fontsize=18)
plt.grid()
plt.show()


x_axis_mem = np.arange(len(mem_list))
fig,ax = plt.subplots()
ax.plot(x_axis_mem, mem_list, linestyle='--', marker='o', color="red")
# set x-axis label
ax.set_xlabel("STEPS [EACH 15 s]", fontsize=18)
# set y-axis label
ax.set_ylabel("MEMORY USAGE [MB]", color='red', fontsize=18)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(x_axis_mem, replicas_mem, linestyle='--', marker='o', color="blue")
ax2.set_ylabel("REPLICAS", color='blue', fontsize=18)
plt.axvline(8, color='purple', label='START TEST')
ax.tick_params(axis='both', which='major', labelsize=18)
plt.yticks(fontsize=18)
plt.axis(ymin=0, xmin=0, xmax=x_axis_cpu[-1])
#ax.set_xticks(np.arange(len(x_axis_mem)), fontsize=18)
plt.title("DEPLOYMENT MEMORY CONSUMPTION (HPA 80%)", fontsize=18)
plt.legend()
plt.grid()
plt.show()

