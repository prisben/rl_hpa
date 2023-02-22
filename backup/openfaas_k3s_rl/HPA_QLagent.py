import gym
import numpy as np
import time
import subprocess
from gym_env.envs.data_processing import save_qtable
import os

# Import and initialize RL environment

env = gym.make('gym_env:gym_env', app_name='log-station', sla_latency="1000", endpoint="http://127.0.0.1:31112/function/log-station",general_path="/home/labtlc/openfaas_k3s_rl")



def train_agent(num_episodes):
    # Hyperparameters
    alpha = 0.5
    gamma = 0.9
    epsilon = 1
    min_eps = 200
    q_table = np.zeros([15, 10])
    # Initialize variables to track rewards
    reward_list = []
    reduction = (epsilon - min_eps) / num_episodes  # reduction starts after a certain n
    state = env.reset()
    print("Initial state is {}".format(state))
    epochs, reward, total_reward, = 0, 0, 0
    done = False
    for x in range(num_episodes):
        print("Iteration num {}".format(x))
        print("Done is {}".format(done))
        print("Initial state is {}".format(state))
        cwd = os.getcwd()
        current_path =cwd+"/"+str(x)
        print("Current path is {}".format(current_path))
        os.mkdir(current_path)
        if np.random.random() < 1 - epsilon:
            print("EXPLOIT")
            action = np.argmax(q_table[state])
        else:
            print("EXPLORE")
            action = env.action_space.sample()
        print('action:' + str(action))
        nodes_command = "python3 nodes_stats.py {} {}".format(current_path, ) #insert duration
        process1 = subprocess.Popen(nodes_command.split())
        dep_command = "python3 dep_stats.py {} {}".format(current_path, ) #insert duration
        process2 = subprocess.Popen(dep_command.split())
        current_pods, next_state, reward, done, info = env.step(action)
        mytuple = current_pods, next_state, reward, done, info
        print("Tuple is:")
        print(mytuple)
            ####save historical tuple###
        filep = current_path + "/k8s_historical_states_discrete.csv"
        with open(filep, 'a') as f:
            f.write(','.join(str(s) for s in mytuple) + ',' + str(action))
            f.write('\n')
            f.close()

        old_value = q_table[state, action]
        next_max = np.max(q_table[
                                  next_state])  # q-table update is always greedy (np.max). q-learning is off-police since the action taken can be of different policy (non-greedy, random) (NG)
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value
        if epsilon > min_eps:
            epsilon -= reduction
        print('state: ' + str(state), 'action:' + str(action),
             'new_value: ' + str(new_value), 'next_state: ' + str(next_state), 'reward: ' + str(reward))
        save_qtable(q_table, current_path)
        reward_list.append(reward)
        total_reward += reward
        state = next_state
        epochs += 1
    timestamp = int(time.time())
    name = "Tot_reward_training_finished_at_{}.txt".format(timestamp)
    with open("reward_list.txt", "w") as f:
         for s in reward_list:
             f.write(str(s) + "\n")
    with open(name, 'w') as f:
        f.write("Total reward is {}".format(total_reward))
        f.write('\n')
        f.write("Number of epochs {}".format(epochs))
        f.close()

    print("Training finished.\n")

def test_agent(num_episodes):
        # Hyperparameters
    alpha = 0.5
    gamma = 0.9
    q_table = np.load("LastQTable.npy") #load last QTable of the training process

    # Initialize variables to track rewards
    reward_list = []

    state = env.reset()
    print("Initial state is {}".format(state))
    epochs, reward, total_reward, = 0, 0, 0
    done = False

    for x in range(num_episodes):
        print("Iteration num {}".format(x))
        print("Done is {}".format(done))
        print("Initial state is {}".format(state))
        cwd = os.getcwd()
        current_path =cwd+"/"+str(x)
        print("Current path is {}".format(current_path))
        os.mkdir(current_path)
        action = np.argmax(q_table[state]) #only exploitation
        print('action:' + str(action))
        nodes_command = "python3 nodes_stats.py {} {}".format(current_path, ) #insert duration
        process1 = subprocess.Popen(nodes_command.split())
        dep_command = "python3 dep_stats.py {} {}".format(current_path, ) #insert duration
        process2 = subprocess.Popen(dep_command.split())
        current_pods, next_state, reward, done, info = env.step(action)
        mytuple = current_pods, next_state, reward, done, info
        print("Tuple is:")
        print(mytuple)
        filep = current_path + "/k8s_historical_states_discrete.csv"
        with open(filep, 'a') as f:
            f.write(','.join(str(s) for s in mytuple) + ',' + str(action))
            f.write('\n')
            f.close()
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value
        print('state: ' + str(state), 'action:' + str(action),
                     'new_value: ' + str(new_value), 'next_state: ' + str(next_state), 'reward: ' + str(reward))
        save_qtable(q_table, current_path)
        reward_list.append(reward)
        total_reward += reward
        state = next_state
        epochs += 1
    timestamp = int(time.time())
    name = "Tot_reward_training_finished_at_{}.txt".format(timestamp)
    with open("reward_list.txt", "w") as f:
        for s in reward_list:
            f.write(str(s) + "\n")
    with open(name, 'w') as f:
        f.write("Total reward is {}".format(total_reward))
        f.write('\n')
        f.write("Number of epochs {}".format(epochs))
        f.close()
    print("Testing finished.\n")

