import numpy as np
import matplotlib.pyplot as plt

#PARAMETERS
arrival_rate = 100 
output_rate = 1000 # (R)
sim_time = 500
queue_sizes = range(0,500)  # (B)
#PARAMETERS


packet_loss_rates = []
mean_output_rates = []

# run for each queue size
for queue_size in queue_sizes:

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
plt.plot(queue_sizes, packet_loss_rates, color='blue')
plt.title("Packet Loss Rate vs Queue Size")
plt.xlabel("Queue Size (B)")
plt.ylabel("Packet Loss Rate")

plt.ylim(bottom=0)  # Set Y-axis minimum to 0
plt.grid()
plt.savefig('5_1a_loss_rate.png')

plt.clf() 

plt.figure(figsize=(10, 8))
plt.plot(queue_sizes, mean_output_rates, color='orange')
plt.title("Mean Output Rate vs Queue Size")
plt.xlabel("Queue Size (B)")

plt.ylim(bottom=0)  # Set Y-axis minimum to 0
plt.ylabel("Mean Output Rate (packets/s)")
plt.grid()
plt.savefig('5_1a_out_rate.png')