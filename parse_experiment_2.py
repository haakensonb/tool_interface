import csv
import matplotlib.pyplot as plt
# redundant, should be merged with parse_experiment_data.py

FILENAME = "log4.txt"

# data for timing creation of graph
csv_data_time = [["Number of roles", "Average of 3 runs"]]

# x axis is same for both graphs
x = []
y_time = []

with open(FILENAME) as f:
    line = f.readline()
    times = []
    node_num = 0
    while line:
        split_line = line.strip().split(" ")
        first_word = split_line[0]
        # check if start of new input
        if first_word == "Running":
            node_num = int(split_line[4])
        elif first_word == "experiment_2_helper":
            times.append(float(split_line[3]))            
        elif first_word == "Ending":
            # calc average runtime
            average_time = sum(times) / len(times)
            csv_data_time.append([node_num, average_time])
            y_time.append(average_time)
            # roles for x axis
            x.append(node_num)
            # reset values
            times = []
        
        # read nextline if there is one
        line = f.readline()

with open("runtime_experiment_2_data.csv", "w", newline="") as csv_file_1:
    writer = csv.writer(csv_file_1)
    writer.writerows(csv_data_time)

# create runtime graph
plt.figure(1)
line_time = plt.plot(x, y_time, marker="o")
plt.title("Runtime For Key Derivation Algorithm")
plt.ylabel("Seconds")
plt.xlabel("Roles")
plt.legend()
plt.savefig("runtime_experiment_2_graph.pdf", bbox_inches="tight")
