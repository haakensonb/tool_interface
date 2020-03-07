import csv
import matplotlib.pyplot as plt

FILENAME = "log3.txt"

# data for timing creation of random graph
csv_data_time = [["Number of roles", "Average of 3 runs"]]
# data for memory size of random graph
csv_data_memory = [["Number of roles", "Average of 3 runs"]]

# x axis is same for both graphs
x = []
y_time = []
y_mem = []

with open(FILENAME) as f:
    line = f.readline()
    times = []
    memory_consumptions = []
    node_num = 0
    while line:
        split_line = line.strip().split(" ")
        first_word = split_line[0]
        # check if start of new input
        if first_word == "Running":
            node_num = int(split_line[3])
        elif first_word == "Size":
            memory_consumptions.append(int(split_line[5]))
        elif first_word == "create_sketch":
            times.append(float(split_line[3]))            
        elif first_word == "Ending":
            # calc average runtime
            average_time = sum(times) / len(times)
            csv_data_time.append([node_num, average_time])
            y_time.append(average_time)
            # calc average memory consumption
            average_mem_consumption = sum(memory_consumptions) / len(memory_consumptions)
            csv_data_memory.append([node_num, average_mem_consumption])
            y_mem.append(average_mem_consumption)
            # roles for x axis
            x.append(node_num)
            # reset values
            times = []
            memory_consumptions = []
        
        # read nextline if there is one
        line = f.readline()

with open("runtime_experiment_data.csv", "w", newline="") as csv_file_1:
    writer = csv.writer(csv_file_1)
    writer.writerows(csv_data_time)

with open("memory_experiment_data.csv", "w", newline="") as csv_file_2:
    writer = csv.writer(csv_file_2)
    writer.writerows(csv_data_memory)

# create runtime graph
plt.figure(1)
line_time = plt.plot(x, y_time, marker="o")
plt.title("Runtime for DAG creation Algorithm")
plt.ylabel("Seconds")
plt.xlabel("Roles")
plt.legend()
plt.savefig("runtime_experiment_graph.pdf", bbox_inches="tight")

# create mem graph
plt.figure(2)
line_mem = plt.plot(x, y_mem, marker="o")
plt.title("Memory Consumption")
plt.ylabel("Bytes")
plt.xlabel("Roles")
plt.legend()
plt.savefig("memory_experiment_graph.pdf", bbox_inches="tight")
