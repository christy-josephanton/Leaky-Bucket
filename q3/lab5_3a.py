import numpy as np
import matplotlib.pyplot as plt

#PARAMETERS
arrival_rate = 100
output_rate = 100
sim_time = 500
queue_sizes = range(0,50)  # Queue sizes from 1 to 1000
token_rate = 200  # token/sec
#PARAMETERS


token_bucket_max = 50  # token bucket limit

packet_loss_rates_data_vary = []
mean_output_rates_data_vary = []

# run for each queue size
for data_bucket_max in queue_sizes:

    total_ticks = int(output_rate * sim_time)  # total clock ticks
    clock_interval = 1 / output_rate           # clock tick time
    avg_arrival_interval = 1 / arrival_rate   # mean inter-arrival time
    token_interval = 1 / token_rate  

    # keeps track of num elements in queue
    data_bucket = 0 
    token_bucket = 0 

    packets_lost = 0
    tokens_lost = 0
    packets_transmitted = 0
    total_arrivals = 0
    total_tokens = 0
    time = 0

    next_arrival = np.random.exponential(avg_arrival_interval)  # first packet arrival
    next_token = 0 # first token arrival

    for tick in range(total_ticks):
    
        time += clock_interval

        #schedule token
        while next_token <= time:
            total_tokens+=1
            if token_bucket < token_bucket_max:
                token_bucket += 1
            else:
                tokens_lost += 1
            next_token += token_interval


        # process all arrival events between last clock tick and this clock tick
        while next_arrival <= time:
            #new arrival
            total_arrivals += 1

            if data_bucket < data_bucket_max: 
                #add to queue if theres space
                data_bucket += 1

            else:
                #dont add to queue if theres no space, keep track of dropped packet
                packets_lost += 1
    
            # schedule next arrival
            next_arrival += np.random.exponential(avg_arrival_interval)  

        # transmit every clock tick if available
        if data_bucket > 0 and token_bucket > 0:
            data_bucket -= 1
            token_bucket -=1
            packets_transmitted += 1

    # Calculate metrics
    
    packet_loss_rate = packets_lost / total_arrivals
    mean_output_rate = packets_transmitted / sim_time

    packet_loss_rates_data_vary.append(packet_loss_rate)
    mean_output_rates_data_vary.append(mean_output_rate)


data_bucket_max = 50

packet_loss_rates_token_vary = []
mean_output_rates_token_vary = []


# run for each queue size
for token_bucket_max in queue_sizes:

    total_ticks = int(output_rate * sim_time)  # total clock ticks
    clock_interval = 1 / output_rate           # clock tick time
    avg_arrival_interval = 1 / arrival_rate   # mean inter-arrival time
    token_interval = 1 / token_rate  

    # keeps track of num elements in queue
    data_bucket = 0 
    token_bucket = 0 

    packets_lost = 0
    tokens_lost = 0
    packets_transmitted = 0
    total_arrivals = 0
    total_tokens = 0
    time = 0

    next_arrival = np.random.exponential(avg_arrival_interval)  # first packet arrival
    next_token = 0 # first token arrival

    for tick in range(total_ticks):
    
        time += clock_interval

        #schedule token
        while next_token <= time:
            total_tokens+=1
            if token_bucket < token_bucket_max:
                token_bucket += 1
            else:
                tokens_lost += 1
            next_token += token_interval


        # process all arrival events between last clock tick and this clock tick
        while next_arrival <= time:
            #new arrival
            total_arrivals += 1

            if data_bucket < data_bucket_max: 
                #add to queue if theres space
                data_bucket += 1

            else:
                #dont add to queue if theres no space, keep track of dropped packet
                packets_lost += 1
    
            # schedule next arrival
            next_arrival += np.random.exponential(avg_arrival_interval)  

        # transmit every clock tick if available
        if data_bucket > 0 and token_bucket > 0:
            data_bucket -= 1
            token_bucket -=1
            packets_transmitted += 1

    # Calculate metrics
    
    packet_loss_rate = packets_lost / total_arrivals
    mean_output_rate = packets_transmitted / sim_time

    packet_loss_rates_token_vary.append(packet_loss_rate)
    mean_output_rates_token_vary.append(mean_output_rate)









plt.figure(figsize=(10, 8))
plt.plot(queue_sizes, packet_loss_rates_data_vary, color='orange',label='Sweep Data Queue Size, Token Queue Size = 50')
plt.plot(queue_sizes, packet_loss_rates_token_vary, color='blue',label='Sweep Token Queue Size, Data Queue Size = 50')
plt.title("Packet Loss Rate vs Queue Size")
plt.xlabel("Queue Size (B)")
plt.ylabel("Packet Loss Rate")
plt.grid()
plt.legend()
plt.savefig('5_3a_loss_rate.png')

plt.clf() 

plt.figure(figsize=(10, 8))
plt.plot(queue_sizes, mean_output_rates_data_vary, color='orange',label='Sweep Data Queue Size, Token Queue Size = 50')
plt.plot(queue_sizes, mean_output_rates_token_vary, color='blue',label='Sweep Token Queue Size, Data Queue Size = 50')
plt.title("Mean Output Rate vs Queue Size")
plt.xlabel("Queue Size (B)")
plt.ylabel("Mean Output Rate (packets/s)")
plt.grid()
plt.legend()
plt.savefig('5_3a_out_rate.png')