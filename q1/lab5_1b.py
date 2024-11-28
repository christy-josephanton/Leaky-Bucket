import numpy as np
import matplotlib.pyplot as plt

#PARAMETERS
arrival_rate = 100
output_rates = range(1,501) # output rates from 1 to 1000
sim_time = 500
queue_size = 3 
#PARAMETERS


packet_loss_rates = []
mean_output_rates = []

# run for each queue size
for output_rate in output_rates:

    total_ticks = int(output_rate * sim_time)  # total clock ticks
    clock_interval = 1 / output_rate           # clock tick time
    avg_arrival_interval = 1 / arrival_rate   # mean inter-arrival time

    queue = 0 # keeps track of num elements in queue

    packets_lost = 0
    packets_transmitted = 0
    total_arrivals = 0
    time = 0

    next_arrival = np.random.exponential(avg_arrival_interval)  # first packet arrival
    for tick in range(total_ticks):
    
        time += clock_interval

        # process all arrival events between last clock tick and this clock tick
        while next_arrival <= time:
            #new arrival
            total_arrivals += 1

            if queue < queue_size: 
                #add to queue if theres space
                queue += 1

            else:
                #dont add to queue if theres no space, keep track of dropped packet
                packets_lost += 1
    
            # schedule next arrival
            next_arrival += np.random.exponential(avg_arrival_interval)  

        # transmit every clock tick if available
        if queue > 0:
            queue -= 1
            packets_transmitted += 1

    # Calculate metrics
    
    packet_loss_rate = packets_lost / total_arrivals
    mean_output_rate = packets_transmitted / sim_time

    packet_loss_rates.append(packet_loss_rate)
    mean_output_rates.append(mean_output_rate)


plt.figure(figsize=(10, 8))
plt.plot(output_rates, packet_loss_rates, color='blue')
plt.title("Packet Loss Rate vs Output Rate")
plt.xlabel("Output Rate (packets/s)")
plt.ylabel("Packet Loss Rate")
plt.grid()
plt.savefig('5_1b_loss_rate.png')

plt.clf() 

plt.figure(figsize=(10, 8))
plt.plot(output_rates, mean_output_rates, color='orange')
plt.title("Mean Output Rate vs Output Rate")
plt.xlabel("Output Rate (packets/s)")
plt.ylabel("Mean Output Rate (packets/s)")
plt.grid()
plt.savefig('5_1b_out_rate.png')