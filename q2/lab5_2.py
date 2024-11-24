import numpy as np
import matplotlib.pyplot as plt

#PARAMETERS
arrival_rate = 100
output_rate = 1_000_000 # 1 Mpbs 
sim_time = 1000
clock_ticks = [0.01, 0.05, 0.1]
packet_sizes = [500, 1000, 1500, 2000, 2500] # in bits 
queue_sizes = range(1, 1001) # queue size in packets
#PARAMETERS


results = {}

for tick in clock_ticks:
       
    packet_loss_rates = []
    mean_output_rates = []
    # run for each queue size
    for queue_size in queue_sizes:

        total_ticks = int(sim_time/tick)  # total clock ticks
        clock_interval = tick           # clock tick time
        avg_arrival_interval = 1 / arrival_rate   # mean inter-arrival time

        queue = [] # keeps track of num elements in queue
        counter = 0
        packets_lost = 0
        packets_transmitted = 0
        total_arrivals = 0
        transmitted_bits = 0
        time = 0

        next_arrival = np.random.exponential(avg_arrival_interval)  # first packet arrival
        for _ in range(total_ticks):
        
            time += clock_interval
            counter = output_rate * clock_interval # counter to bytes per tick 

            # process all arrival events between last clock tick and this clock tick
            while next_arrival <= time:
                #new arrival
                total_arrivals += 1
                packet_size = np.random.choice(packet_sizes) # pick random packet size from our list
                if len(queue) < queue_size: 
                    #add to queue if theres space
                    queue .append(packet_size)

                else:
                    #dont add to queue if theres no space, keep track of dropped packet
                    packets_lost += 1
        
                # schedule next arrival
                next_arrival += np.random.exponential(avg_arrival_interval)  

            # Transmit a packet if the counter has space 
            while queue and queue[0] <= counter:
                packet_size = queue.pop(0)
                counter -= packet_size
                packets_transmitted += 1
                transmitted_bits += packet_size

        # Calculate metrics
        
        packet_loss_rate = packets_lost / total_arrivals
        mean_output_rate = packets_transmitted / sim_time

        packet_loss_rates.append(packet_loss_rate)
        mean_output_rates.append(mean_output_rate)
    
    results[tick] = (packet_loss_rate, mean_output_rates)
    # Plot results for the current clock tick
    plt.figure(figsize=(10, 8))
    plt.plot(queue_sizes, packet_loss_rates, color='blue')
    plt.title(f"Packet Loss Rate vs Queue Size (Tick = {tick}s)")
    plt.xlabel("Queue Size (Packets)")
    plt.ylabel("Packet Loss Rate")
    plt.grid()
    plt.savefig(f'loss_rate_tick_{tick}.png')

    plt.clf()

    plt.figure(figsize=(10, 8))
    plt.plot(queue_sizes, mean_output_rates, color='orange')
    plt.title(f"Mean Output Rate vs Queue Size (Tick = {tick}s)")
    plt.xlabel("Queue Size (Packets)")
    plt.ylabel("Mean Output Rate (bps)")
    plt.grid()
    plt.savefig(f'out_rate_tick_{tick}.png')

    plt.clf()

# Summary Plots
plt.figure(figsize=(12, 6))
for tick, (loss_rates, _) in results.items():
    plt.plot(queue_sizes, loss_rates, label=f"Tick = {tick}s")
plt.title("Packet Loss Rate vs Queue Size (All Ticks)")
plt.xlabel("Queue Size (Packets)")
plt.ylabel("Packet Loss Rate")
plt.legend()
plt.grid()
plt.savefig('combined_loss_rate.png')

plt.clf()

plt.figure(figsize=(12, 6))
for tick, (_, out_rates) in results.items():
    plt.plot(queue_sizes, out_rates, label=f"Tick = {tick}s")
plt.title("Mean Output Rate vs Queue Size (All Ticks)")
plt.xlabel("Queue Size (Packets)")
plt.ylabel("Mean Output Rate (bps)")
plt.legend()
plt.grid()
plt.savefig('combined_out_rate.png')