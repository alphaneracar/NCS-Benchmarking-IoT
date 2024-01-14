import json
import os
from src.site_coordinator import SiteCoordinator
import ipaddress
import invoke.exceptions

ipv6_prefixes = {'grenoble': '2001:660:5307:3100::/64', 'lille': '2001:660:4403:0480::/64', 'saclay': '2001:660:3207:04c0::/64', 'strasbourg': '2a07:2e40:fffe:00e0::/64', 'paris': '2001:660:330f:a286::/64'}


def increment_ip_addr(addr, counter):
    addr = addr.split(':')
    addr = ':'.join(addr[:4])+':0000:0000:0000:0000'
    addr1 = ipaddress.IPv6Address(addr)
    while counter > 0:
        addr1 += int(ipaddress.IPv6Address('0000:0000:0000:0001:0000:0000:0000:0000'))
        counter -= 1
    return(str(addr1)+'1/64')

class M3Coordinator(SiteCoordinator):

    def __init__(
        self,
        site,
        experiment_id,
        border_routers: dict,
        nodes,
        os_input
        ):
        super().__init__(
            site,
            experiment_id,
            nodes,
            'm3',
            os_input
        )
        self.border_routers=border_routers
        self.ipv6_prefix=ipv6_prefixes[site]
        self.os=os_input
        

    def set_up(self):
        print(f'{self.site_prefix}Got work to do..')
        self.init_border_routers()
    
    def init_border_routers(self):
        print(f'{self.site_prefix}Starting the br screen sessions..')
        conn = self.init_connection()
        for key, value in self.border_routers.items():
            node = value[0].split('.')[0]
            if 'node-' in node:
                node = node[5:]
            print(f'{self.site_prefix}Starting iteration for br {key}, on {node}')
            port_num = 20000
            port_num = str(port_num + int(key))
            command = None
            if value[-1] == 'contiki':
                print(f'{self.site_prefix}Starting tun screen for br {key}, and {node}')
                command = f"screen -L -Logfile ./tunslip{key}.output -dmS tun{key} sudo tunslip6.py -v2 -L -a {node} -p 20000 {increment_ip_addr(self.ipv6_prefix, int(key))}"
            
            elif value[-1] == 'riot':
                print(f'{self.site_prefix}Starting tap screen for br {key}, and {node}')
                command = f"screen -L -Logfile ./tunslip{key}.output -dmS tap{key} sudo ethos_uhcpd.py {node} tap{key} {increment_ip_addr(self.ipv6_prefix, int(key))}"
            
            conn.run(
                command, 
                disown=True
                )

    def rerun_stopped_br_processes(self):
        screen_name = "tap" if self.os=="riot" else "tun"
        stopped_brs=[]
        conn = self.init_connection()
        grep_result=""
        grep_str = ""
        try:
            conn.run(f"screen -wipe", hide = True)
        except invoke.exceptions.UnexpectedExit as e:
            print(e)
        try:
            grep_result = conn.run(f"screen -ls", hide = True)
            grep_str = grep_result.stdout.strip(" \t\n\r")
        except invoke.exceptions.UnexpectedExit as e:
            print(e)
        #grep_result = conn.run(f"screen -ls", hide = True)
        #grep_str = grep_result.stdout.strip(" \t\n\r")
        if grep_str=="":
            for k in self.border_routers.keys():
                self.start_border_router(k)
            return
        for k in self.border_routers.keys():

            if f"{screen_name}{k}" not in grep_str:
                stopped_brs.append(k)
                print(f"{screen_name}{k} not alive!")
    
        if len(stopped_brs) == 0:
            print(f'{self.site_prefix}Nothing to restart, returning!')
            return
        else:
            for k in stopped_brs:
                self.start_border_router(k)

    def start_border_router(self, num):
        print(f'{self.site_prefix}Starting the br screen sessions..')
        conn = self.init_connection()
        key = str(num)
        value = self.border_routers[num]
        
        node = value[0].split('.')[0]
        if 'node-' in node:
            node = node[5:]
        print(f'{self.site_prefix}Starting iteration for br {key}, on {node}')
        # port_num = 20000
        # port_num = str(port_num + int(key))
        command = None
        if value[-1] == 'contiki':
            print(f'{self.site_prefix}Starting tun screen for br {key}, and {node}')
            command = f"screen -L -Logfile ./tunslip{key}.output -dmS tun{key} sudo tunslip6.py -v2 -L -a {node} -p 20000 {increment_ip_addr(self.ipv6_prefix, int(key))}"
        
        elif value[-1] == 'riot':
            print(f'{self.site_prefix}Starting tap screen for br {key}, and {node}')
            command = f"screen -L -Logfile ./tunslip{key}.output -dmS tap{key} sudo ethos_uhcpd.py {node} tap{key} {increment_ip_addr(self.ipv6_prefix, int(key)-1)}"
        
        conn.run(
            command, 
            disown=True
            )

    def digest_new_addresses(self):
        self.get_addresses()
        results = self.read_addresses()
        print(f'{self.site_prefix}{len(results.keys())} adresses received!')
        for k, v in results.items():
            if v != 'NA':
                key = f"{k}.{self.site}.iot-lab.info"
                self.global_addresses_to_nodes[v] = key
                self.nodes_to_global_addresses[key] = v
                self.awaiting_nodes_to_global_addresses.pop(key)

    def kill_border_routers(self):
        for key in self.border_routers.keys():
            self.kill_br_screen(key)
    
    def kill_br_screen(self, index):
        print(f'{self.site_prefix}Killing tunslip{index} at {self.border_routers[index]}')
        
        conn = self.init_connection()

        screen_name = "tap" if self.os=="riot" else "tun"

        conn.run(f"screen -S {screen_name}{index} -X quit")


    #TODO: Write a separate method for writing br details and call that from this method 
    # along with the kill_border_routers 
    def finish(self):
        print(f"\n{self.site_prefix}Finishing the experiment..\n")

        print(f"\n{self.site_prefix}Killing border routers..\n")
        self.kill_border_routers()

        print(f"\n{self.site_prefix}Writing border routers..\n")

        base_dir = f"experiment_data/{self.experiment_id}/results"
        br_results_dir = os.path.join(base_dir, self.site)
        os.makedirs(br_results_dir, exist_ok=True)

        with open(f"{base_dir}/{self.site}/brs.json", "w") as file:
            json.dump(self.border_routers, file)

        print(f"\n{self.site_prefix}Collecting tap output files..\n")
        conn = self.init_connection()
        for k, v in self.border_routers.items():
            self.write_border_router(base_dir, k, v, conn)
        
        conn.close()

    '''
    -------------------- READ/WRITE --------------------
    '''

    def write_border_router(self, prefix, k, v, conn):
        #TODO: delete the files after reading
        print(f"{self.site_prefix}Writing the details of br on {v}..")
        conn.get(
            f"/senslab/users/eracar/tunslip{k}.output",
            f"{prefix}/{self.site}/"
        )

