import asyncio
import time
import sys
import os
import traceback
import json
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
missing_measurements=None
all_nodes_to_addresses = dict()

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

def write_addresses():
    global node_id_to_global_address
    with open(f"./m3/node_ids_to_addresses.json", "w") as file:
        json.dump(node_id_to_global_address, file, indent=4)

def read_all_addresses():
    global all_nodes_to_addresses    
    with open(f"./all_nodes_to_addresses.json", "r") as file:
        all_nodes_to_addresses = json.load(file)

def read_missing_measurements():
    global missing_measurements    
    with open(f"./m3/missing_measurements.json", "r") as file:
        missing_measurements = json.load(file)
    
def write_ping_measurements():
    global ping_measurements
    converted_dict = {str(key): value for key, value in ping_measurements.items()}
    with open("./m3/ping_measurements.json", 'w') as file:
        json.dump(converted_dict, file)

'''
TASK 1: FETCH ADDRESSES
'''
def read_ifconfig(line):
    global site
    global node_id_to_global_address
    key=None
    addr=None
    if "-- 2" in line:
        print("--2 in line!")
        splitted = line.split(";")
        key = f"{splitted[1]}.{site}.iot-lab.info"
        addr = splitted[-1].split()[1]
    return key, addr



'''
TASK 1.1: INITIAL FETCH ADDRESSES
'''
# async def fetch_addresses():
#     global node_id_to_global_address
#     print("In fetch addresses")
#     aggregator = await asyncio.create_subprocess_exec(
#                 "serial_aggregator", 
#                 stdin=asyncio.subprocess.PIPE, 
#                 stdout=asyncio.subprocess.PIPE
#                 )

#     output_list=[]
#     command = "ip-addr\n"
#     aggregator.stdin.write(command.encode())
#     await aggregator.stdin.drain()
#     print('drain awaited')

#     output_list = []
#     time.sleep(1)
#     #await aggregator.stdin.drain()
#     output = await aggregator.stdout.readline()
#     output = output.decode("utf-8", errors='ignore')
#     read_ifconfig(output)
#     output_list.append(output)
#     i = 0
#     while True:
#         try:
#             output_inner = await asyncio.wait_for(asyncio.shield(aggregator.stdout.readline()), timeout=0.5)
#             output_inner = output_inner.decode("utf-8", errors='ignore')
#             read_ifconfig(output_inner)
#             output_list.append(output_inner)
#             if i %5 == 0:
#                 print(f"{len(node_id_to_global_address.keys())} number of adresses read!")
#             i+=1
#         except Exception as e:
#             traceback.format_exc()
#             print("Output list: ", output_list)
#             print("In exception")
#             print(e)
#             break

#     print(output_list)
#     aggregator.kill()

async def fetch_addresses():
    global node_id_to_global_address
    print("In fetch addresses")
    aggregator = await asyncio.create_subprocess_exec(
                "serial_aggregator", 
                stdin=asyncio.subprocess.PIPE, 
                stdout=asyncio.subprocess.PIPE
                )

    output_list=[]
    command = "ip-addr\n"
    await aggregator.stdin.write(command.encode())
   # await aggregator.stdin.drain()
    #print('drain awaited')

    while True:
        try:
            output = await asyncio.wait_for(asyncio.shield(aggregator.stdout.read(1000)), timeout=1.0)
            if not output:
                break
            output = output.decode("utf-8", errors='ignore').split('\n')
            for line in output:
                key, addr = read_ifconfig(line)
                if key != None and addr != None:
                    node_id_to_global_address[key] = addr
                output_list.append(line)
            print(f"{len(node_id_to_global_address.keys())} number of addresses read!")
        except Exception as e:
            traceback.format_exc()
            print("Output list: ", output_list)
            print("In exception")
            print(e)
            break

    print(output_list)
    aggregator.kill()

'''
TASK 1.2: RETRY FETCH ADDRESSES
'''
# async def retry_fetch_addresses_contiki(nodes):
#     global node_id_to_global_address
#     global site
#     for node in nodes:
#         print("node:", node)
#         node = node.split(".")[0]
#         print("Opening netcat command to the node:", node)
#         connection = await asyncio.create_subprocess_exec(
#                 "nc", node, "20000", 
#                 stdin=asyncio.subprocess.PIPE, 
#                 stdout=asyncio.subprocess.PIPE
#         )
#         command = "ip-addr\n"
#         connection.stdin.write(command.encode())
#         output = await connection.stdout.readline()
#         output = output.decode("utf-8", errors='ignore')
#         start=time.time()
#         read = True
#         out_list=[output]
#         count=0
#         while count < 6:
#             try:
#                 if time.time()-start > 1:
#                     print("Timeout fetch address on", node)
#                     read = False
#                     break
#                 if "--" in output:
#                     print("output found!")
#                     break
#                 #output = await connection.stdout.readline()
                
#                 output = await asyncio.wait_for(asyncio.shield(connection.stdout.readline()), timeout=0.2)
#                 output = output.decode("utf-8", errors='ignore')
#                 out_list.append(output)
#                 count+=1
#                 #asyncio.sleep(0.1)
#                 #print("output", output)
#             except Exception as e:
#                 print(e)
#                 read = False
#                 print("Timeout retry fetch address on", node)
#                 #connection.kill()
#                 break
#             finally:
                
#                 connection.kill()

#         for s in out_list:
#             if "-- 2" in s:
#                 addr = output.split()[1]
#                 node_id_to_global_address[node] = addr
#         # if read:
#         #     addr = output.split()[1]
#         #     node_id_to_global_address[node] = addr
#         #connection.kill()

async def retry_fetch_addresses_contiki(nodes):
    global node_id_to_global_address
    global site
    for node in nodes:
        print("node:", node)
        node = node.split(".")[0]
        print("Opening netcat command to the node:", node)
        connection = await asyncio.create_subprocess_exec(
                "nc", node, "20000", 
                stdin=asyncio.subprocess.PIPE, 
                stdout=asyncio.subprocess.PIPE
        )
        command = "ip-addr\n"
        connection.stdin.write(command.encode())
        output = await connection.stdout.readline()
        output = output.decode("utf-8", errors='ignore')
        while "-- 2" not in output:
            try:
                output = await asyncio.wait_for(asyncio.shield(connection.stdout.readline()), timeout=0.2)
                output = output.decode("utf-8", errors='ignore')
            except Exception as e:
                print(e)
                print("Timeout retry fetch address on", node)
                connection.kill()
                break
        
        if "-- 2" in output:
            addr = output.split()[1]
            node_id_to_global_address[node] = addr
        connection.kill()


async def retry_fetch_addresses_riot(nodes):
    global node_id_to_global_address
    global site
    for node in nodes:
        print("node:", node)
        node = node.split(".")[0]
        print("Opening netcat command to the node:", node)
        connection = await asyncio.create_subprocess_exec(
                "nc", node, "20000", 
                stdin=asyncio.subprocess.PIPE, 
                stdout=asyncio.subprocess.PIPE
        )
        command = "ifconfig\n"
        connection.stdin.write(command.encode())
        output = await connection.stdout.readline()
        output = output.decode("utf-8", errors='ignore')
        while "scope: global" not in output:
            try:
                output = await asyncio.wait_for(asyncio.shield(connection.stdout.readline()), timeout=0.2)
                output = output.decode("utf-8", errors='ignore')
            except Exception as e:
                print(e)
                print("Timeout retry fetch address on", node)
                connection.kill()
                break
        
        if "scope: global" in output:
            addr = output.split()[2].split('/')[0]
            node_id_to_global_address[node] = addr
        connection.kill()

'''
TASK 2: RUN PING
'''

'''
TASK 2.1: RUN INITIAL PING
'''

def read_ping(line, dest_node, dest_addr):
    global ping_measurements
    global site
    if f"Received ping reply from {dest_addr}" in line:
        splitted = line.split(";")
        key = f"{splitted[1]}.{site}.iot-lab.info"
        rtt = splitted[-1].split()[-2]
        ping_measurements[(key, dest_node)] = rtt
        return True


async def run_ping_round():
    global ping_measurements
    global all_nodes_to_addresses
    print("In run ping round")
    aggregator = await asyncio.create_subprocess_exec(
                "serial_aggregator", 
                stdin=asyncio.subprocess.PIPE, 
                stdout=asyncio.subprocess.PIPE
                )
            
    destinations_ids = list(all_nodes_to_addresses.keys())
    start=time.time()
    try:
        for dest in destinations_ids:
            print(f"Awaiting run ping to ping {dest}")
            await run_ping(aggregator, dest, all_nodes_to_addresses[dest])
    except Exception as e:
        traceback.format_exc()
        print(e)
        write_addresses()
        aggregator.kill()
        return False
    end=time.time()
    print(f"Took {end-start} secs to finish run ping round.")

async def run_ping(aggregator, dest_node, dest_addr):
    print("In run ping")
    output_list=[]
    command = f"ping {dest_addr}\n"
    aggregator.stdin.write(command.encode())
    output = await aggregator.stdout.readline()
    output = output.decode("utf-8", errors='ignore')
    read_ifconfig(output)
    output_list.append(output)
    num_successful_measurements = 0
    while True:
        try:
            output_inner = await asyncio.wait_for(asyncio.shield(aggregator.stdout.readline()), timeout=0.5)
            output_inner = output_inner.decode("utf-8", errors='ignore')
            if read_ping(output_inner, dest_node, dest_addr):
                num_successful_measurements += 1
            print(output_inner)
            output_list.append(output_inner)

        except Exception as e:
            traceback.format_exc()
            print("In exception")
            print(e)
            break

    print(output_list)

'''
TASK 2.2: RETRY PING
'''

def retry_ping_round(loop, os):
    global missing_measurements
    source_list = list(missing_measurements.keys())
    start = time.time() 
    k=0
    while k < len(source_list):
        count=0
        probe_tasks = []
        for j in range(k, min(len(source_list), k+20)):
            count+=1
            source = source_list[j]
            dests = missing_measurements[source]
            if os == "riot":
                probe_tasks.append(asyncio.ensure_future(run_retry_ping_riot(source, dests)))
            elif os == "contiki":
                probe_tasks.append(asyncio.ensure_future(run_retry_ping_contiki(source, dests)))
        loop.run_until_complete(asyncio.gather(*probe_tasks))
        k+=count
    end = time.time()
    print(f"Took {end-start} secs to finish retry ping round")
    
    
async def run_retry_ping_contiki(source, dests):
    global all_nodes_to_addresses
    global ping_measurements
    node = source.split('.')[0]
    if "node-" in node:
        node = node[5:]
    print(f"Running retry ping on {node} with {len(dests)} dests.")
    connection = await asyncio.create_subprocess_exec(
                "nc", node, "20000", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    start = time.time()
    for dest_node in dests:

        dest_addr = all_nodes_to_addresses[dest_node]
        command = f"ping {dest_addr}\n"     
        max_retry = 2
        retry = 0
        while True:
            if retry >= max_retry:
                print(f"Max retry reached for {node} to {dest_node}")
                break
            connection.stdin.write(command.encode())
            output = await connection.stdout.readline()
            start=time.time()
            output = output.decode("utf-8")
            continue_reading=True
            while continue_reading:#"Received ping reply" not in output: 
                try:
                    if "Received ping reply" in output:
                        break

                    elif 'timeout' in output:
                        print(f"Timeout for node: {node}")
                        break

                    elif time.time()-start > 10:
                        print(f"It took more than 5 secs to read output from node: {node}!")
                        break

                    output = await connection.stdout.readline()#await asyncio.wait_for(asyncio.shield(connection.stdout.readline()), timeout=1)
                    output = output.decode("utf-8", errors='ignore')
                except:
                    traceback.format_exc()
                    print(f"Timeout reached for {node}")
                    print("ping measurements:", ping_measurements)
                    continue_reading=False
                    

            if "Received ping reply" in output:

                rtt = output.split()[-2]
                #print("RTT:", rtt)
                ping_measurements[(source, dest_node)] = rtt
                break
            retry += 1

    end = time.time()
    print(f"Took {end-start} secs to finish retry ping round for {source}")
    try:
        connection.kill()
    except:
        print("Couldnt kill the process!")



async def run_retry_ping_riot(source, dests):
    global all_nodes_to_addresses
    global ping_measurements
    node = source.split('.')[0]
    if "node-" in node:
        node = node[5:]
    print(f"Running retry ping on {node} with {len(dests)} dests.")
    connection = await asyncio.create_subprocess_exec(
                "nc", node, "20000", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    start = time.time()
    try:


        for dest_node in dests:

            dest_addr = all_nodes_to_addresses[dest_node]
            command = f"ping {dest_addr}\n"     
            max_retry = 2
            retry = 0
            while True:
                if retry >= max_retry:
                    print(f"Max retry reached for {node} to {dest_node}")
                    break
                connection.stdin.write(command.encode())
                output = await connection.stdout.readline()
                start=time.time()
                output = output.decode("utf-8")
                continue_reading=True
                #out_list=[output]
                while continue_reading:#"Received ping reply" not in output: 
                    try:

                        if "min/avg/max" in output:
                            break

                        elif '0 packets received' in output:
                            print(f"Node: {node} received 0 packets!")
                            break

                        elif time.time()-start > 5:
                            print(f"It took more than 5 secs to read output from node: {node}!")
                            #print("out_list:", out_list)
                            #raise Exception("Timeout!!")
                            break

                        output = await asyncio.wait_for(asyncio.shield(connection.stdout.readline()), timeout=5)
                        output = output.decode("utf-8", errors='ignore')
                        #out_list.append(output)
                    except:
                        traceback.format_exc()
                        print(f"Timeout reached for {node}")
                        #print("ping measurements:", ping_measurements)
                        #print("out_list:", out_list)
                        continue_reading=False
                        

                if "min/avg/max" in output:
                    rtt = output.split()[3].split('/')[1]
                    ping_measurements[(source, dest_node)] = rtt
                    break
                retry += 1
    except Exception as e:
        traceback.format_exc()

    finally:
        end = time.time()
        print(f"Took {end-start} secs to finish retry ping round for {source}")
        connection.kill()

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
    else:
        file_path = './m3/nodes.txt'
        if os.path.isfile(file_path):
            nodes = read_nodes(file_path)
        else:
            print(file_path, "does not exist!!")
            return

    loop = asyncio.get_event_loop()

    #Fetch Addresses
    # if "fetch_addresses" in method:
    #     initial_fetch_address = asyncio.ensure_future(fetch_addresses())
    #     loop.run_until_complete(asyncio.gather(initial_fetch_address))
    #     write_addresses()
    #     print("SUCCESS")
        
    #Retry Fetch Addresses
    if "retry_fetch_addresses"  in method:
        if nodes == None:
            print("No nodes have been given as config parameters.")
            return    

        retry_fetch_address=None
        if "contiki" in method:
            retry_fetch_address = asyncio.ensure_future(retry_fetch_addresses_contiki(nodes))

        elif "riot" in method:
            retry_fetch_address = asyncio.ensure_future(retry_fetch_addresses_riot(nodes))

        else:
            print("M3 OS not provided!")
            return
        loop.run_until_complete(asyncio.gather(retry_fetch_address))
        write_addresses()
        print("SUCCESS")
        
    #Run Ping
    # elif method == "run_ping":
    #     read_all_addresses()
    #     initial_ping = asyncio.ensure_future(run_ping_round())
    #     loop.run_until_complete(asyncio.gather(initial_ping))
    #     write_ping_measurements()
    #     print("SUCCESS")

    #Retry Ping
    elif "retry_ping"  in method:

        read_all_addresses()
        read_missing_measurements()
        try:
            if "riot" in method:
                retry_ping_round(loop, "riot")

            elif "contiki" in method:
                retry_ping_round(loop, "contiki")

            else:
                print("M3 OS not provided!")
                return
        except Exception as e:
            print(e)
            write_ping_measurements()
            print("ERROR")
        
        write_ping_measurements()
        print("SUCCESS")

    else:
        raise Exception("Method did not match anything")
    

if __name__ == "__main__":
    main()
