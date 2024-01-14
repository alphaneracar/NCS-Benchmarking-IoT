import ast
import os
import invoke
from fabric import Connection
from abc import ABC, abstractmethod
import json

class SiteCoordinator(ABC):

    def __init__(
        self,
        site,
        experiment_id,
        nodes,
        device_type,
        os_prefix=None,
        num=None):
        
        self.site=site
        self.nodes=nodes
        self.experiment_id=experiment_id
        self.device_type=device_type
        self.num=num
        self.site_prefix=self.device_type+"-"+site+": "


        self.remote_dir=self.device_type 
        if self.num != None:
            self.remote_dir=self.device_type+"_"+num
        
        self.os_prefix = "_"+os_prefix if os_prefix!= None else ""

        self.nodes_to_global_addresses=dict()
        self.global_addresses_to_nodes=dict()

        self.all_nodes_to_addresses=dict()

        self.ping_measurements=dict()

        #These must be initialized for every key to keep track of missing measurements.
        self.awaiting_nodes_to_global_addresses=dict()
        self.awaiting_ping_measurements=dict()


    '''This will be overriden on m3 nodes'''
    def set_up(self):
        print(f"{self.site_prefix}Nothing to do")

    '''This will be overriden on m3 nodes'''
    def finish(self):
        print(f"{self.site_prefix}Nothing to do")

    def check_finished_ping_round(self) -> bool:
        number_of_missing_measurements = len(self.awaiting_ping_measurements.keys())
        if number_of_missing_measurements == 0:
            print(f'{self.site_prefix}There are {number_of_missing_measurements} number of retry ping hosts.')
            return True
        else:
            print(f'{self.site_prefix}All measurements are fetched!')
            return False

    def check_finished_fetch_addresses(self) -> bool:
        number_of_missing_addresses = len(self.awaiting_nodes_to_global_addresses.keys())
        if number_of_missing_addresses == 0:
            print(f'{self.site_prefix}There are {number_of_missing_addresses} number of retry fetch address hosts.')
            return True
        else:
            print(f'{self.site_prefix}All addresses are fetched!')
            return False

    '''
    ------------------------------------------- REFRESH PING -------------------------------------------
    '''


    def refresh_ping_measurement(self):
        print(f'{self.site_prefix}Resetting the ping measurements to initial state.')
        self.initialize_awaiting_ping_measurements_dict()
        self.ping_measurements={}


    '''
    ------------------------------------------- CONNECTION HANDLERS -------------------------------------------
    '''
    def init_connection(self):
        print(f'{self.site_prefix}Openning connection to {self.site}')
        connection = Connection(
                f"eracar@{self.site}.iot-lab.info"
        )
        return connection
        

    def close_connection(self, connection: Connection):
        connection.close()

    '''
    ------------------------------------------- FETCH ADDRESS RUN -------------------------------------------
    '''
    def initialize_awaiting_address_dict(self):
        print(f'{self.site_prefix}Initializing the awaiting_addresses dictionary.')
        for n in self.nodes:
            self.awaiting_nodes_to_global_addresses[n] = None


    def digest_new_addresses(self):
        self.get_addresses()
        results = self.read_addresses()
        print(f'{self.site_prefix}{len(results.keys())} adresses received!')
        for k, v in results.items():
            if v != 'NA':
                self.global_addresses_to_nodes[v] = k
                self.nodes_to_global_addresses[k] = v
                self.awaiting_nodes_to_global_addresses.pop(k)
        
        

    def calculate_missing_addresses(self) -> list:
        print(f'{self.site_prefix}Calculating the missing addresses..')
        return list(self.awaiting_nodes_to_global_addresses.keys())

    '''---- INITIAL FETCH ADDRESS ----'''

    def run_fetch_addresses(self):
        print(f'{self.site_prefix}Starting initial fetch address run.')
        self.delete_addresses_site()
        self.delete_addresses_local()
        self.send_nodes()
        conn = self.init_connection()
        print(f'{self.site_prefix}Running fetch addresses on site.')
        conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py fetch_addresses_{self.num} {self.site}"
        )
        self.get_addresses()
        #self.digest_new_addresses()

    '''---- RETRY FETCH ADDRESS ----'''

    def retry_fetch_addresses(self):
        if len(self.awaiting_nodes_to_global_addresses.keys()) == 0:
            print(f'{self.site_prefix}All addresses are compelete, nothing to rerun.')
            return
        print(f'{self.site_prefix}Starting retry fetch address run.')
        self.send_nodes()
        conn = self.init_connection()
        missing_addresses = list(self.awaiting_nodes_to_global_addresses.keys())
        conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py retry_fetch_addresses{self.os_prefix} {self.site} '{str(missing_addresses)}'"
        )
        self.get_addresses()
        #self.digest_new_addresses()


    def async_retry_fetch_addresses(self):
        if len(self.awaiting_nodes_to_global_addresses.keys()) == 0:
            print(f'{self.site_prefix}All addresses are compelete, nothing to rerun.')
            return
        print(f'{self.site_prefix}Starting retry fetch address run.')
        self.send_nodes()
        conn = self.init_connection()
        missing_addresses = list(self.awaiting_nodes_to_global_addresses.keys())
        return conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py retry_fetch_addresses{self.os_prefix}_{self.num} {self.site} '{str(missing_addresses)}'",
            asynchronous=True
        )
        #self.get_addresses()
        #self.digest_new_addresses()

    def read_async_retry_fetch_addresses(self, promise):
        print(f'{self.site_prefix}Joining the promise..')
        promise.join()


    '''
    ------------------------------------------- PING RUN -------------------------------------------
    '''

    def initialize_awaiting_ping_measurements_dict(self):
        print(f'{self.site_prefix}Initializing the awaiting_ping_measurements dictionary.')
        for n in self.nodes:
            for a in self.all_nodes_to_addresses.keys():
                self.awaiting_ping_measurements[(n, a)] = None

        if self.device_type=='linux':
            for a in self.all_nodes_to_addresses.keys():
                self.awaiting_ping_measurements[(self.site, a)] = None

        self.delete_all_addresses_site()
        self.put_all_addresses()

    def digest_new_measurements(self):
        self.get_ping_results()
        results = self.read_ping_results()
        print(f'{self.site_prefix}{len(results.keys())} measurements received!')
        for k, v in results.items():
            if v != 'NA':
                self.ping_measurements[k] = v
                self.awaiting_ping_measurements.pop(k)
        
        self.delete_ping_results_site()
        self.delete_ping_results_local()

    
    '''---- INITIAL PING ----'''

    def run_ping_measurement(self):
        print(f'{self.site_prefix}Starting the initial ping round.')
        self.send_nodes()
        conn = self.init_connection()
        conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py run_ping{self.os_prefix}_{self.num} {self.site}"
        )

    def async_run_ping_measurement(self):
        print(f'{self.site_prefix}Starting the initial ping round.')
        self.send_nodes()
        conn = self.init_connection()
        return conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py run_ping{self.os_prefix}_{self.num} {self.site}", 
            asynchronous=True
        )

    def read_async_run_ping_measurement(self, promise):
        print(f'{self.site_prefix}Joining the promise..')
        promise.join()
        


    '''---- RETRY PING ----'''

    def calculate_missing_measurements_dict(self) -> dict:
        print(f'{self.site_prefix}Calculating the missing measurements..')
        missing_measurements=dict()
        for a in self.awaiting_ping_measurements.keys():
            if a[0] not in missing_measurements.keys():
                missing_measurements[a[0]] = []
                missing_measurements[a[0]].append(a[1])
            else:
                missing_measurements[a[0]].append(a[1])

        return missing_measurements
    
    def retry_ping_measurement(self):
        if len(self.awaiting_ping_measurements.keys()) == 0:
            print(f'{self.site_prefix}All ping measurements are complete, nothing to rerun.')
            return
        
        print(f'{self.site_prefix}Starting the retry ping round.')
        self.send_missing_measurements()
        conn = self.init_connection()
        conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py retry_ping{self.os_prefix}_{self.num} {self.site}"
        )

    def async_retry_ping_measurement(self):
        if len(self.awaiting_ping_measurements.keys()) == 0:
            print(f'{self.site_prefix}All ping measurements are complete, nothing to rerun.')
            return
        
        print(f'{self.site_prefix}Starting the retry ping round.')
        self.send_missing_measurements()
        conn = self.init_connection()
        return conn.run(
            f"cd ~/ping_experiments && python3 {self.device_type}_site.py retry_ping{self.os_prefix}_{self.num} {self.site}", 
            asynchronous=True
        )

    def read_async_retry_ping_measurement(self, promise):
        print(f'{self.site_prefix}Joining the promise..')
        promise.join()

    '''
    ------------------------------------------- SEND/GET -------------------------------------------
    
    This part here is the endpoint between the scripts running on sites and the scripts running local.

    The methods in endpoint always try to delete the files before transferring. 
    '''

    #TODO: SHould they also delete files before executing a command on site or will you rely on the overwriting of the files?

    def send_nodes(self):
        print(f'{self.site_prefix}Sending the nodes.txt.')
        self.delete_nodes_local()
        self.delete_nodes_site()
        self.write_nodes()
        self.put_nodes()


    def send_missing_measurements(self):
        print(f'{self.site_prefix}Sending the missing measurements.json.')
        missing_measurements = self.calculate_missing_measurements_dict()
        self.delete_missing_measurements_site()
        self.delete_missing_measurements_local()
        self.write_missing_measurements(missing_measurements)
        self.put_missing_measurements()


    '''
    ------------------------------------------- GET/PUT AND READ/WRITE -------------------------------------------
    
    This part can be thought of lower layer communication protocol handlers.
    '''

    '''---- PING ----'''

    def get_ping_results(self):
        print(f'{self.site_prefix}Getting the ping results.')
        conn = self.init_connection()
        print(os.getcwd())
        print("remote path:", f"~/ping_experiments/{self.remote_dir}/ping_measurements.json")
        conn.get(
            f"./ping_experiments/{self.remote_dir}/ping_measurements.json", 
            f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/"
        )
        self.close_connection(conn)

    def read_ping_results(self):
        print(f'{self.site_prefix}Reading the ping results.')
        with open(f'./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/ping_measurements.json', 'r') as file:
            data = json.load(file)
        return {ast.literal_eval(key): value for key, value in data.items()}

    def delete_ping_results_local(self):
        print(f'{self.site_prefix}Deleting the local fetched ping measurements.')
        self.run_command(
            f'rm -rf ./experiment_data/{self.experiment_id}/{self.site}/{self.remote_dir}/ping_measurements.json', 
            conn=None,
            hide=True
        )
        # invoke.run(
        #     f'rm -rf ./experiment_data/{self.experiment_id}/{self.site}/{self.device_type}/ping_measurements.json', 
        #     hide=True
        # )

    def delete_ping_results_site(self):
        print(f'{self.site_prefix}Deleting the fetched ping measurements on site.')
        conn = self.init_connection()
        self.run_command(
            f'rm -rf ~/ping_experiments/{self.remote_dir}/ping_measurements.json',
            conn=conn,
            hide="err")
        # conn.run(
        #     f'rm -rf ~/ping_experiments/{self.device_type}/ping_measurements.json',
        #     hide="err")
        self.close_connection(conn)

    def write_missing_measurements(self, missing_measurements):
        print(f'{self.site_prefix}Writing missing measurements on local.')
        with open(f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/missing_measurements.json", "w") as file:
            json.dump(missing_measurements, file, indent=4)

    def delete_missing_measurements_local(self):
        print(f'{self.site_prefix}Deleting missing measurements on local.')
        self.run_command(
            f'rm -rf ./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/missing_measurements.json', 
            conn=None,
            hide=True
        )
        # invoke.run(
        #     f'rm -rf ./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.device_type}/missing_measurements.json', 
        #     hide=True
        # )

    def delete_missing_measurements_site(self):
        print(f'{self.site_prefix}Deleting the missing ping measurements on site.')
        conn = self.init_connection()
        self.run_command(
            f'rm -rf ~/ping_experiments/{self.remote_dir}/missing_measurements.json',
            conn=conn,
            hide="err")
        # conn.run(
        #     f'rm -rf ~/ping_experiments/{self.device_type}/missing_measurements.json',
        #     hide="err")
        self.close_connection(conn)

    def put_missing_measurements(self):
        print(f'{self.site_prefix}Putting the missing_measurements.json to site.')
        conn = self.init_connection()
        conn.put(
            f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/missing_measurements.json",
            f"/senslab/users/eracar/ping_experiments/{self.remote_dir}"
        )
        conn.close()

    '''---- SITE ADDRESS ----'''

    def get_addresses(self):
        conn = self.init_connection()
        print("Getting from: ", f"ping_experiments/{self.remote_dir}/node_ids_to_addresses.json")
        print(conn.host)
        conn.get(
            f"/senslab/users/eracar/ping_experiments/{self.remote_dir}/node_ids_to_addresses.json", 
            f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/node_ids_to_addresses.json"
        )
        self.close_connection(conn)

    def read_addresses(self):
        with open(f'./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/node_ids_to_addresses.json', 'r') as file:
            return json.load(file)

    def delete_addresses_local(self):
        print(f'{self.site_prefix}Deleting the local addresses.')
        self.run_command(
            f'rm -rf ./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/node_ids_to_addresses.json', 
            conn=None,
            hide=True
        )
        # invoke.run(
        #     f'rm -rf ./experiment_data/{self.experiment_id}/{self.site}/node_ids_to_addresses.json', 
        #     hide=True
        # )

    def delete_addresses_site(self):
        print(f'{self.site_prefix}Deleting the fetched addresses on site.')
        conn = self.init_connection()
        self.run_command(
            f'rm -rf ./ping_experiments/{self.remote_dir}/node_ids_to_addresses.json', 
            conn=conn,
            hide="err"
        )
        # conn.run(
        #     f'rm -rf ./ping_experiments/{self.device_type}/node_ids_to_addresses.json', 
        #     hide="err"
        # )
        self.close_connection(conn)

    '''---- ALL ADDRESSES ----'''

    def delete_all_addresses_site(self):
        print(f'{self.site_prefix}Deleting the fetched addresses on site.')
        conn = self.init_connection()
        self.run_command(
            f'rm -rf ./ping_experiments/{self.remote_dir}/all_nodes_to_addresses.json', 
            conn=conn,
            hide="err"
        )
        self.close_connection(conn) 

    def put_all_addresses(self):
        print(f'{self.site_prefix}Putting the all_nodes_to_addresses.json to site.')
        conn = self.init_connection()
        conn.put(
            f"./experiment_data/{self.experiment_id}/results/all_nodes_to_addresses.json",
            f"ping_experiments/all_nodes_to_addresses.json"
        )
        conn.close()

    '''---- NODES ----'''

    def write_nodes(self):
        print(f'{self.site_prefix}Writing nodes to local.')
        with open(f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/nodes.txt", "w") as file:
            for n in self.nodes:
                file.write("%s\n" % n)

    def put_nodes(self):
        print(f'{self.site_prefix}Putting nodes on {self.site}.')
        conn = self.init_connection()
        conn.put(
            f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/nodes.txt",
            f"./ping_experiments/{self.remote_dir}/"
        )
        self.close_connection(conn)

    def delete_nodes_local(self):
        print(f'{self.site_prefix}Deleting the local nodes.txt.')
        #print(os.getcwd())
        self.run_command(
            f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.remote_dir}/nodes.txt", 
            None,
            'err'
        )
        # invoke.run(
        #     f"./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.device_type}/nodes.txt", 
        #     hide='err'
        # )

    def delete_nodes_site(self):
        print(f'{self.site_prefix}Deleting the nodes.txt addresses on {self.site}.')
        conn = self.init_connection()
        self.run_command(
            f'rm -rf ./ping_experiments/{self.remote_dir}/nodes.txt', 
            conn=conn, 
            hide="err"
            )
        #conn.run(f'rm -rf ./ping_experiments/{self.device_type}/nodes.txt', hide="err")
        self.close_connection(conn)


    def run_command(self, command, conn=None, hide=False):

        try:
            if conn != None:
                conn.run(
                    command,
                    hide=hide
                )
            else:
                invoke.run(
                    command,
                    hide=hide
                )

        except invoke.exceptions.UnexpectedExit as u:
            print(u)

    #NOTE: This won't be necessary because missing addresses will be given as parameter.

    # def write_missing_addresses(self, missing_measurements):
    #     print(f'{self.site_prefix}Writing missing measurements on local.')
    #     with open(f"~/experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.device_type}/missing_measurements.json", "w") as file:
    #         json.dump(missing_measurements, file, indent=4)

    # def delete_missing_addresses_local(self):
    #     print(f'{self.site_prefix}Deleting missing measurements on local.')
    #     invoke.run(
    #         f'rm -rf ./experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.device_type}/missing_measurements.json', 
    #         hide=True
    #     )

    # def delete_missing_addresses_site(self):
    #     print(f'{self.site_prefix}Deleting the missing ping measurements on site.')
    #     conn = self.init_connection()
    #     conn.run(f'rm -rf ./ping_experiments/{self.device_type}/missing_measurements.json')
    #     self.close_connection(conn)

    # def put_missing_addresses(self):
    #     print(f'{self.site_prefix}Putting the missing_measurements.json to site.')
    #     conn = self.init_connection()
    #     conn.put(
    #         f"~/experiment_data/{self.experiment_id}/intermediate/{self.site}/{self.device_type}/missing_measurements.json",
    #         f"./ping_experiments/{self.device_type}"
    #     )

    