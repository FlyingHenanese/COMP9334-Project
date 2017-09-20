import random
import math
#use pylab to draw diagram
import pylab as pl


#use final list to record response time in each simulation
global Final_list

#There if no build in function to implement Pareto distribution in python
#But it can be represent by uniform distribution.
#This function calculate the inverse function of the probability density function f(ts)
def subserver_service_time(n):
    return (10.3846/(n**1.65))/((1-random.uniform(0,1))**(1/2.08))


#inter_arrival_time distribute in two part
#1.The sequence a1k is exponentially distributed with a mean arrival rate 0.85 requests per time unit.
#2.The sequence a2k is uniformly distributed in the interval [0.05, 0.25].
#formula is same as the one in sim_mm1.m
#random.random() could generate float in range[0.0,1.0)
def inter_arrival_time(rate):
    return (-math.log(1-random.random())/rate)+random.uniform(0.05,0.25)

#Preprocess time is exponentially distributed with a mean service time of n/10 per request
#which means the rate is 10/n
def pre_process_time(n):
    return -math.log(1-random.random())/(10/n)

#Request will distribute in to n sub_tasks and send to sub_servers randomly choosed
#Here I use build in random.sample() to generate a list with distinct server number
#in range[0,10)(assume there are 10 sub_server), each number is the index of the subserver
def distribute_server(n):
    return random.sample(range(0,10),n)

#main loop of simulation, which takes num of subservers n, total simulation time unit tend
#a list which record all response time during this simulation Final_list
def start(n, tend,Final_list):
    #init arrive time
    Arrive_time = 0
    #Record the finish time for preprocess task
    pre_processor = 0
    rate = 0.85
    #array represent the subservers, each element record subtask's finish time
    sub_servers = [0]*10
    #record arrival time in order to draw diagram
    draw_x = []
    #Since the buffer of each part if unlimited large, preprocessor use the first
    # in first serve strategy, we can calculate the process with each task's arrival
    # time and renew preprocessor and sub_servers by calculation
    while(Arrive_time<tend):
        #Arrive time = previous Arrive time plus inter_arrival time
        Arrive_time+=inter_arrival_time(rate)
        #if preprocessor is busy, calculate when it can finish current request
        if Arrive_time<pre_processor:
            period = pre_processor + pre_process_time(n)
            pre_processor = pre_processor+pre_process_time(n)
        #Preprocessor not busy, calculate current request's finish time
        else:
            period = Arrive_time + pre_process_time(n)
            pre_processor = Arrive_time+pre_process_time(n)
        #record finish time for subtasks of hole request
        temp = []
        #Handle each sub_server as what i have done for preprocessor
        for server in distribute_server(n):
            if sub_servers[server] < period:
                sub_servers[server] = period + subserver_service_time(n)
                temp.append(sub_servers[server])
            else:
                sub_servers[server]+=subserver_service_time(n)
                temp.append(sub_servers[server])
        #Find  the longest sub_task's process time which is the
        # finish time at joint point
        temp.sort()
        period = temp[n-1]
        #As I didn't use master clock to record time unit, I have
        # to judge whether the request finished in simulation period
        #if not , the request will be abandoned, and hole simulation
        # will finish
        if(period<tend):
            #confident interval
            if period-Arrive_time<30:
                Final_list.append(period-Arrive_time)
            #record the Arrive time for diagram
                draw_x.append(Arrive_time)
    # draw diagram
    # pl.plot(draw_x,Final_list)
    # pl.show()
    return Final_list


def sim_start(tend):
    #simulate the situations for n in range[1,11)
    for n in range(1,11):
        Final_list=[]
        start(n,tend,Final_list)
        sum = 0
        iter = 0
        for a in Final_list:
            sum+=a
            iter+=1
        result = sum/iter
        print(n," : ",result)
    return


if __name__ == '__main__':
    #use seed to make program reproducable
    random.seed(0)
    #for i in range(10000,100000,10000):
    sim_start(300000)
    #draw diagram
    # Final_list = []
    # start(8,100000,Final_list)