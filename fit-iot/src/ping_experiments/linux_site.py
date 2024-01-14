import ast
import time
import sys
import os
import traceback
import json
import invoke
from fabric import Connection

'''
This will run on each site.
'''

root_dir=""

site = None

connections = dict()

node_id_to_global_address = dict()
global_address_to_node_id = dict() 

ping_measurements = dict()
#retry_addresses = dict()
missing_measurements=None
all_nodes_to_addresses = dict()

#failed_pairs=[]
'''
HELPER 1: CONNECTIONS
'''

def init_connection(node):
    print(f'Openning connection to {node}')
    id = node.split('.')[0]
    connection = Connection(
            f"root@{id}"
    )
    return connection

def close_connections(connections):
    print(f'Closing connections to {connections.keys()}')
    for k, c in connections.items():
        try: 
            c.close()
        except Exception as e:
            print(e)
            print("Error while closing", k)
    connections = {}


'''
HELPER 2: READ AND WRITE FROM/TO A FILE
'''

#TODO: Add root_dir prefix before the open statements.

def read_nodes(path):
    print("Reading nodes from:", path)
    nodes = []
    with open(path, "r") as file:
        for line in file:
            nodes.append(line.strip())
    return nodes

def write_addresses(num=''):
    dir_num="" if num == '' else "_"+num
    global node_id_to_global_address
    with open(f"./linux{dir_num}/node_ids_to_addresses.json", "w") as file:
        json.dump(node_id_to_global_address, file, indent=4)

def read_all_addresses():
    global all_nodes_to_addresses  
    print("Reading all nodes")  
    with open(f"./all_nodes_to_addresses.json", "r") as file:
        all_nodes_to_addresses = json.load(file)
    #print("all_nodes_to_addresses", all_nodes_to_addresses)

def read_missing_measurements(num=''):
    dir_num="" if num == '' else "_"+num
    #TODO: read this differently
    global missing_measurements    
    with open(f"./linux{dir_num}/missing_measurements.json", "r") as file:
        missing_measurements = json.load(file)
    
def write_ping_measurements(num=''):
    global ping_measurements
    dir_num="" if num == '' else "_"+num
    converted_dict = {str(key): value for key, value in ping_measurements.items()}
    with open(f"./linux{dir_num}/ping_measurements.json", 'w') as file:
        json.dump(converted_dict, file)


'''
TASK 1: FETCH ADDRESSES
'''
def read_ifconfig(output):
    splitted = output.split('\n')
    for s in splitted:
        if 'Scope:Global' in s:
            addr = s.split()[2]
            return addr.split('/')[0]
    return None

def run_ifconfig(connections):
    print(f'Starting iteration with: {connections.keys()}')
    failed_hosts = []
    global node_id_to_global_address
    global global_address_to_node_id
    for n, c in connections.items():
        try:
            ifconfig_result = c.run("ifconfig", hide=True)
        except Exception as e:
            print(f"Error node: {n}")
            print(e)
        addr = read_ifconfig(ifconfig_result.stdout)
        if addr != None:
            node_id_to_global_address[n] = addr
            global_address_to_node_id[addr] = n
        else:
            failed_hosts.append(n)
    return failed_hosts


def fetch_addresses(nodes_list):
    print(f'In fetch addresses.')

    if len(nodes_list) == 0:
        print("Nothing to do.")
        return

    iteration_number = len(nodes_list)//10
    last_iteration=len(nodes_list)%10
    print(f'There are {len(nodes_list)} number of hosts.')
    print(f'Executing {iteration_number} iterations.')
    for i in range(iteration_number+1):
        node_per_iteration = last_iteration if i == iteration_number else 10
        print(f'Node per iteration: {node_per_iteration}')
        connections=dict()
        for j in range(node_per_iteration):
            node = nodes_list[i*10+j]
            connections[node] = init_connection(node)
        
        failed_hosts = run_ifconfig(connections)
        #Retry the unsuccessful fetchs
        if len(failed_hosts) > 0:
            count = 0
            while len(failed_hosts) > 0 and count <= 2:
                print(f'Failed to fetch addresses from the following hosts, retrying: {failed_hosts}')
                connections_subset = {k: connections[k] for k in failed_hosts if k in connections}
                failed_hosts = run_ifconfig(connections_subset)
                count += 1

        #TODO: Add a retry to handle the unsuccessful fetchs
        close_connections(connections)

'''
TASK 2: RUN PING
'''

'''
TASK 2.1: RUN INITIAL PING
'''

#TODO: Delete failed pairs

def run_ping_round(nodes_list):
    global ping_measurements
    global all_nodes_to_addresses
    #global failed_pairs
    global site
    print(f'In run ping round')

    
    #print("nodes_list:", nodes_list)
    all_nodes = list(all_nodes_to_addresses.keys())
    #print("all nodes:", all_nodes)
    total_number_of_nodes = len(all_nodes)
    number_of_iterations=total_number_of_nodes//20
    rest = total_number_of_nodes % 20 != 0
    range_list=[]
    #Initialize the range list
    for i in range(number_of_iterations):
        start_index=i*20
        end_index=start_index+20
        range_list.append((start_index, end_index))
    if rest:
        print("Here!")
        start = range_list[-1][-1] if len(range_list) > 0 else 0
        range_list.append((start, -1))

    print("range list", range_list)
    #If there are no nodes, only do the site ping and return
    if len(nodes_list) == 1 and nodes_list[0] == site:
        print("Only running ping on ",site)
        run_ping_on_site(all_nodes, range_list)
        return
    #TODO: Carry this functionality to somewhere else and give nodes_list as a parameter
    iteration_number = None
    last_iteration = None
    if len(nodes_list)%15==0:
        iteration_number = len(nodes_list)//15
    else:
        iteration_number = len(nodes_list)//15 + 1
        last_iteration=len(nodes_list)%15
    print(f'There are {len(nodes_list)} number of hosts.')
    print(f'Executing {iteration_number} iterations.')
    for i in range(iteration_number):
        node_per_iteration = last_iteration if i == iteration_number-1 and last_iteration!=None else 15
        print(f'Node per iteration: {node_per_iteration}')
        connections=dict()
        for j in range(node_per_iteration):
            node = nodes_list[i*15+j]
            connections[node] = init_connection(node)           
        run_ping(connections, all_nodes, range_list)
        close_connections(connections)

    run_ping_on_site(all_nodes, range_list)

#TODO: Running on linux site do not include the last address 

#TODO: You also have to store global addresses to node ids 
def run_ping(connections, all_nodes, range_list):
    global all_nodes_to_addresses
    global ping_measurements
    #global failed_pairs
    print("range list:", range_list)
    print(f'Starting iteration with: {connections.keys()}')
    for i, r in enumerate(range_list):
        start = time.time()
        promises = dict()
        destinations = None
        #destinations = all_nodes[r[0]:r[-1]]
        if i == len(range_list) - 1:
            destinations = all_nodes[r[0]:]
        else:
            destinations = all_nodes[r[0]:r[-1]]
        destination_addresses = [all_nodes_to_addresses[k] for k in destinations]
        for n, c in connections.items():
            promises[n] = c.run(f"cd ~/shared && python3 linux_script.py '{str(destination_addresses)}'", asynchronous=True)

        for k, p in promises.items():
            res = p.join()
            result_dict = ast.literal_eval(res.stdout)
            for j, d in enumerate(destination_addresses):
                destination_id = destinations[j]
                #print("result_dict", result_dict)
                ping_measurements[(k, destination_id)] = result_dict[d]
        print(f'Finished executing the {i}. range in {time.time()-start} secs.')

#With fabric or invoke
def run_ping_on_site(all_nodes, range_list):
    print('Running ping on site device.')
    #connection = Connection(f"eracar@{self.site}.iot-lab.info")
    global site
    #global failed_pairs
    global ping_measurements
    global all_nodes_to_addresses
    for i, r in enumerate(range_list):
        start = time.time()
        destinations = None
        #destinations = all_nodes[r[0]:r[-1]]
        if i == len(range_list) - 1:
            destinations = all_nodes[r[0]:]
        else:
            destinations = all_nodes[r[0]:r[-1]]
        destination_addresses = [all_nodes_to_addresses[k] for k in destinations]
        promise = invoke.run(f"cd ~/shared && python3 linux_script.py '{str(destination_addresses)}'", asynchronous=True)

        res = promise.join()
        result_dict = ast.literal_eval(res.stdout)
        for j, d in enumerate(destination_addresses):
            destination_id = destinations[j]
            # if result_dict[d] == 'NA':  
            #     failed_pairs.append((site, destination_id))
            ping_measurements[(site, destination_id)] = result_dict[d]
        
        print(f'Finished executing the {i}. range in {time.time()-start} secs.')
    #connection.close()

'''
TASK 2.2: RETRY PING
'''

def define_destination_ranges(destinations):
    total_number_of_nodes = len(destinations)
    number_of_iterations=total_number_of_nodes//20
    rest = total_number_of_nodes % 20 != 0
    range_list=[]
    for i in range(number_of_iterations):
        start_index=i*20
        end_index=start_index+20
        range_list.append((start_index, end_index))
    if rest:
        start = range_list[-1][-1] if len(range_list) > 0 else 0
        range_list.append((start, -1))
    return range_list

def retry_ping_round():
    global missing_measurements
    print(f"Starting retry ping with {len(missing_measurements.keys())} sources..")
    for k, v in missing_measurements.items():
        if k != site:
            
            run_retry_ping(k, v, define_destination_ranges(v))
        else:
            run_retry_ping_on_site(k, v, define_destination_ranges(v))    
    

def run_retry_ping(source, dests, range_list):
    #TODO: Do this after you decide on how to read the retry pairs
    global ping_measurements
    global all_nodes_to_addresses
    print("In retry ping with", source)
    print("Number of destinations:", len(dests))
    conn = init_connection(source)
    destinations = None
    for i, r in enumerate(range_list):
        start = time.time()
        if i == len(range_list) - 1:
            destinations = dests[r[0]:]
        else:
            destinations = dests[r[0]:r[-1]]
#        destinations = dests[r[0]:r[1]]
        destination_addresses = [all_nodes_to_addresses[k] for k in destinations]
        result = conn.run(f"cd ~/shared && python3 linux_script.py '{str(destination_addresses)}'", hide=True)
        result_dict = ast.literal_eval(result.stdout)
        print(result_dict)
        for j, d in enumerate(destination_addresses):
            destination_id = destinations[j]
            # if result_dict[d] == 'NA':  
            #     failed_pairs.append((source, destination_id))
            ping_measurements[(source, destination_id)] = result_dict[d]

        print(f"{i}. range of {source} is finished in {time.time() - start} secs.")
    conn.close()

def run_retry_ping_on_site(source, dests, range_list):
    #TODO: Do this after you decide on how to read the retry pairs
    global ping_measurements
    global all_nodes_to_addresses
    print("In retry ping with", source)
    print("Number of destinations:", len(dests))
    destinations = None
    for i, r in enumerate(range_list):
        start = time.time()
        if i == len(range_list) - 1:
            destinations = dests[r[0]:]
        else:
            destinations = dests[r[0]:r[-1]]
        destination_addresses = [all_nodes_to_addresses[k] for k in destinations]
        result = invoke.run(f"cd ~/shared && python3 linux_script.py '{str(destination_addresses)}'", hide=True)
        result_dict = ast.literal_eval(result.stdout)
        #print(result_dict)
        for j, d in enumerate(destination_addresses):
            destination_id = destinations[j]
            # if result_dict[d] == 'NA':  
            #     failed_pairs.append((source, destination_id))
            ping_measurements[(source, destination_id)] = result_dict[d]

        print(f"{i}. range of {source} is finished in {time.time() - start} secs.")



'''
-----  MAIN  -----
'''

def parse_nodes_list(input_str):
    nodes = input_str.strip("[]").split(',')
    return [node.strip() for node in nodes]

def main(): 
    method = None
    global site
    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        print("No method provided.")
        return

    if len(sys.argv) > 2:
        site = sys.argv[2]
        print(f"Site: {site}")
    else:
        print("No site provided")
        return

    nodes = None
    if len(sys.argv) > 3:
        nodes = parse_nodes_list(sys.argv[3])
        print(f"Nodes received: {nodes}")
   
        

    #Fetch Addresses
    if "fetch_addresses_" in method:

        num = method.split('_')[-1]
        file_path = f'./linux_{num}/nodes.txt'
        if os.path.isfile(file_path):
            nodes = read_nodes(file_path)
        else:
            print(file_path, "does not exist!!")
            return
        fetch_addresses(nodes)
        write_addresses(num)
        print("SUCCESS")
        
    #Retry Fetch Addresses
    elif method == "retry_fetch_addresses":
        num = method.split('_')[-1]
        file_path = f'./linux_{num}/nodes.txt'
        if os.path.isfile(file_path):
            nodes = read_nodes(file_path)
        else:
            print(file_path, "does not exist!!")
            return
        if nodes == None:
            print("No nodes have been given as config parameters.")
            return    
        fetch_addresses(nodes)
        write_addresses(num)
        print("SUCCESS")
        
    #Run Ping
    elif "run_ping" in method:
        num = method.split('_')[-1]
        file_path = f'./linux_{num}/nodes.txt'
        if os.path.isfile(file_path):
            nodes = read_nodes(file_path)
        else:
            print(file_path, "does not exist!!")
            return
        read_all_addresses()
        try:
            run_ping_round(nodes)
        except Exception as e:
            print(e)
            write_ping_measurements(num)
            print("ERROR")
        write_ping_measurements(num)
        print("SUCCESS")

    #Retry Ping
    elif "retry_ping" in method:
        num = method.split('_')[-1]
        read_all_addresses()
        read_missing_measurements(num)
        try:
            retry_ping_round()
        except Exception as e:
            print(e)
            write_ping_measurements(num)
            print("ERROR")
        write_ping_measurements(num)
        print("SUCCESS")

    else:
        raise Exception("Method did not match anything")
    

if __name__ == "__main__":
    main()
