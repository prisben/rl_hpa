import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import requests
from gym_env.envs.data_processing import get_test_latency, get_test_timeouts, get_test_percentile, get_avg_pods
from gym_env.envs import test_k8s
# from test_k8s import get_existing_app_hpa, kube_one
import os
import kubernetes
from kubernetes import client, config
import json
from subprocess import Popen, PIPE
import time
import yaml
from pprint import pprint
import math
import datetime


class GymEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, app_name, sla_latency, endpoint, general_path):
        super(GymEnv, self).__init__()
        # General variables defining the environment
        self.done = False
        self.slot = "A" #uncomment for training
        self.MAX_PODS = 30
        self.MIN_PODS = 1
        self.DOWNSCALE = 5
        self.currentpods = 1
        self.app_name = app_name
        self.endpoint = endpoint
        self.general_path = general_path
        self.counter = 0
        self.sla_latency = float(sla_latency)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(5),  # latency intervals
            spaces.Discrete(3)))  #replicas intervals

        self.action_space = spaces.Discrete(10) #cpu thresholds

    def step(self, action):
        '''
        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob : List[int]
                an environment-specific object representing your observation of
                the environment.
            reward : float
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            info : Dict
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
      '''
        # create hpa
        #select slot
        modulo = self.counter%2   #uncomment for training 
        if modulo == 0:
           self.slot = "A"
        elif modulo == 1:
           self.slot = "B"
        self._take_action(action)
        path = self.general_path +"/"+ str(self.counter) #folder for the current iteration
        out = self.test(path, self.slot) #azure train
        #out = self.test_evaluation(path, self.counter) #uncomment test
        ob = self._get_state(path)
        print("State object is {}".format(ob))
        # calculate reward
        reward = self._get_reward_new(path)
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.counter +=1
        self.done=True
        return self.currentpods, ob, reward, self.done, {'datetime': dt_string}

    def reset(self):
        return self.get_reset_state()

    def render(self, mode='human'):
        return None

    def close(self):
        pass

    def _take_action(self, discrete_action):
        thrs = THRS_LIST[discrete_action]
        try:
            o = test_k8s.update_hpa(self.app_name, thrs, self.MAX_PODS, self.DOWNSCALE)
            return o     
        except Exception as e:
       	    print("Exception when performing action")
            print(e)    		   
          
    def _get_state(self,path):
        """
      Get the observation.
      pod_cpu_thrs: First number is the current pod cpu threshold
      pods_number: Third number is the number of the current pods
      timeout: discretized
      """
        service_lat = float(get_train_latency(path, self.slot)) #uncommen training
        #service_lat = float(get_test_latency(path, self.counter)) #uncomment test
        avg_pods = math.ceil(get_avg_pods(path))
        self.currentpods = avg_pods 
        return self.encode(service_lat, avg_pods)

    def get_reset_state(self):
        return (0,0)


    def _get_reward(self, path):
        lat = float(get_train_latency(path, self.slot))/1000 # s
        # lat = float(get_test_latency(path, self.slot))/1000 #uncomment test
        print("Latency is {}".format(lat))
        SLA = self.sla_latency/1000
        if lat < SLA:
            reward = 1 / (SLA - lat)
        else:
            reward = (SLA - lat)*1000
        print("Reward is {}".format(reward))
        return reward

    def _get_reward_new(self, path):
        reward = 0
        max_reward = 100
        min_reward = 0
        pod_weight = 0.3
        lat_weight = 0.7
        d=
        lat = float(get_train_latency(path, self.slot)) # s
        # lat = float(get_test_latency(path, self.slot)) #uncomment test
        if self.currentpods == 1 and lat <= self.sla_latency:
            reward = max_reward
            return reward
        else if lat > self.sla_latency:
            reward = min_reward
            return reward
        pod_reward = -100 / (self.MAX_PODS-1)*self.currentpods + 100*self.MAX_PODS/(self.MAX_PODS-1)
        reward = reward + pod_weight*pod_reward
        if lat/self.sla_latency<0.8:
            lat_reward = 100*math.exp(-0.3*d*(0.8-lat/self.sla_latency)**2)
        else if lat/self.sla_latency>0.8:
            lat_reward = 100*math.exp(-10*d*(0.8-lat/self.sla_latency)**2)
        reward = reward + lat_weight*lat_reward
        return reward

    def find_interval(self, lat):
        interval = 0
        if 0 <= lat < 250:
            interval = 0
        elif 250 <= lat < 500:
            interval = 1
        elif 500 <= lat < 750:
            interval = 2
        elif 750 <= lat <= 1000:
            interval = 3
        elif lat > 1000:
            interval = 4
        return interval

    def encode(self, service_lat, avg_pods):
        # 10, 10
        label = 0
        if 1<= avg_pods < 2:
            label = 0
        elif 2 <= avg_pods <= 4:
            label = 1
        elif avg_pods > 5:
            label = 2
        i = self.find_interval(service_lat)
        i *= 3
        i += label
        return i

    def test(self, path, slot):
        ## set for wrk stress test ##
        ## the tool can be changed ##
        f_list_train = ["/home/labtlc/openfaas_k3s_rl/wrk1_{}.lua".format(slot), "/home/labtlc/openfaas_k3s_rl/wrk2_{}.lua".format(slot),
                 "/home/labtlc/openfaas_k3s_rl/wrk3_{}.lua".format(slot), "/home/labtlc/openfaas_k3s_rl/wrk4_{}.lua".format(slot),
                      ]
        cmds_list = []
        cmds_list.append("wrk -c5 -t1 -d4m --timeout 1m -s {} {}".format(f_list_train[0], self.endpoint))
        cmds_list.append("wrk -c1 -t1 -d4m --timeout 1m -s {} {}".format(f_list_train[1], self.endpoint))
        cmds_list.append("wrk -c1 -t1 -d4m --timeout 1m -s {} {}".format(f_list_train[2], self.endpoint))
        cmds_list.append("wrk -c1 -t1 -d4m --timeout 1m -s {} {}".format(f_list_train[3], self.endpoint))  #one or more wrk lua scripts
        cmds_list = []
        cmds_list.append("wrk -c5 -t1 -d4m --timeout 1m -s {} {}".format(f_list_train[0], self.endpoint))
        procs_list = [Popen(cmd.split(), stdout=PIPE, stderr=PIPE, cwd=path) for cmd in cmds_list]
        for proc in procs_list:
            proc.wait()
        return 1

    def test_evaluation(self, path, counter):
        f_list = ["/home/labtlc/openfaas_k3s_rl/evaluation/{}/wrk1_A.lua".format(counter), "/home/labtlc/openfaas_k3s_rl/evaluation/{}/wrk2_A.lua".format(counter)]
        cmds_list = []
        cmds_list.append("wrk -c5 -t1 -d4m --timeout 1m -s {} {}".format(f_list[0], self.endpoint))
        cmds_list.append("wrk -c1 -t1 -d4m --timeout 1m -s {} {}".format(f_list[1], self.endpoint))
        procs_list = [Popen(cmd.split(), stdout=PIPE, stderr=PIPE, cwd=path) for cmd in cmds_list]
        for proc in procs_list:
            proc.wait()
        return 1

THRS_LIST = {
     0: 10,
     1: 20,
     2: 30,
     3: 40,
     4: 50,
     5: 60,
     6: 70,
     7: 80,
     8: 90,
     9: 100,
 }
