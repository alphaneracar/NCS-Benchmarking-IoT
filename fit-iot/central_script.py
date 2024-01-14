from datetime import datetime
import json
import os
import sys
import time
import logging
from src.linux_coordinator import LinuxCoordinator
from src.m3_coordinator import M3Coordinator
import invoke
import enoslib as en

en.init_logging(level=logging.INFO)
en.check()
'''
This is the central code responsible for creating the necessary things for each site.
'''

node_to_ip = {'grenoble':'2001:660:5307:30ff::5', 'lille':'2001:660:4403:47f::4', 'paris':'2001:660:330f:a27f::4', 'saclay':'2001:660:3207:4bf::17', 'strasbourg':'2a07:2e40:fffe:df::5'}


sites = ["grenoble", "saclay", "paris", "strasbourg"]


def create_experiment_dir(experiment_id, sites):

    invoke.run(f"mkdir ./experiment_data/{experiment_id}")

    invoke.run(f"mkdir ./experiment_data/{experiment_id}/intermediate")
    invoke.run(f"mkdir ./experiment_data/{experiment_id}/results")

    for site in sites:
        invoke.run(f"mkdir ./experiment_data/{experiment_id}/intermediate/{site}")
        for sub in ["m3", "linux_1", "linux_2"]:
            invoke.run(f"mkdir ./experiment_data/{experiment_id}/intermediate/{site}/{sub}")
    print(f"Created the experiment directory with id: {experiment_id}") 


'''
All of the results will come here and combined in this class. This class is only class that will 
use enoslib.
'''

class CentralCoordinator():

    def __init__(
        self,
        experiment_conf
        ):
        self.experiment_conf=experiment_conf
        self.sites=sites
        self.absolute_path=os.getcwd() 

    def initialize_experiment(self):
        self.conf = en.IotlabConf.from_dictionary(self.experiment_conf)
        self.p = en.Iotlab(self.conf)
        self.roles, self.networks = self.p.init()        
        
    def update_site_config(self, key, site_config):
        if "br" in key:
            return
        print(f"Adding {key} to the site_config.")
        site = key.split('_')[1]
        if "m3" in key:
            if "m3_"+site not in site_config.keys():
                site_config["m3_"+site] = {"brs":{}, "nodes": []}
            br_num = key.split('_')[-1]
            print("key:", self.roles["br_"+site+"_"+br_num])
            print(self.roles["br_"+site+"_"+br_num])
            os_input = None

            if "gnrc" in self.roles["br_"+site+"_"+br_num][0].image:
                os_input = "riot"

            else:
                os_input = "contiki"

            site_config["m3_"+site]["brs"][br_num] = (self.roles["br_"+site+"_"+br_num][0].address, os_input)
            nodes = []
            for n in self.roles[key]:
                nodes.append(n.address)
            site_config["m3_"+site]["nodes"] += nodes

        elif "a8" in key:
            num = key.split('_')[-1]
            if "linux_"+site+'_'+num not in site_config.keys():
                site_config["linux_"+site+'_'+num] = []
            nodes = []
            for n in self.roles[key]:
                nodes.append(n.address)
            site_config["linux_"+site+'_'+num] += nodes

        elif "rpi" in key:
            num = key.split('_')[-1]
            if "linux_"+site+'_'+num not in site_config.keys():
                site_config["linux_"+site+'_'+num] = []
            nodes = []
            for n in self.roles[key]:
                nodes.append(n.address)
            site_config["linux_"+site+'_'+num] += nodes

    def create_site_coordinators(self):
        print(f'Creating the site coordinators...')
        site_config=dict()
        self.site_coordinators=dict()
        for k in self.roles.keys():
            self.update_site_config(k, site_config)
            
        for scr, n in site_config.items():
            coord = None
            if "m3" in scr:
                site = scr.split("_")[1]
                coord = M3Coordinator(site, self.experiment_id, n["brs"], n["nodes"], n["brs"]['0'][-1])
            elif "linux" in scr:
                site = scr.split("_")[1]
                num = scr.split("_")[-1] 
                coord = LinuxCoordinator(site, self.experiment_id, n, num)
            self.site_coordinators[scr] = coord

        print(f"Site coordinators are created:", self.site_coordinators)
    

    def set_up_sites(self):
        print("In set_up_sites")
        self.create_site_coordinators()
        for k, v in self.site_coordinators.items():
            print("\n\n--------------------------------------\n\n")
            print("Setting up ", k)
            v.set_up()

    def set_up_experiment(self, experiment_id):
        print("In set_up_experiment")
        self.experiment_id = experiment_id
        print(os.getcwd())
        print(f"{self.absolute_path}/experiment_data")
        if os.path.isdir(f"./experiment_data/{experiment_id}"):
            print(f"Directory with experiment id: {experiment_id} already exists")
            return
        create_experiment_dir(experiment_id, self.sites)
        

    def send_site_scripts(self, input_sites=None):
        dest_sites=sites
        if input_sites != None:
            dest_sites=input_sites
        print("Sending ping_experiments directory to all sites..")
        for s in dest_sites:
            invoke.run(
                f"scp -r {self.absolute_path}/src/ping_experiments eracar@{s}.iot-lab.info:~",
                hide=True
            )

    def check_if_addresses_are_ready(self):
        is_ready=True
        for k, v in self.site_coordinators.items():
            is_ready = is_ready and v.check_finished_fetch_addresses()
        return is_ready

    def check_if_measurements_are_ready(self):
        is_ready=True
        for k, v in self.site_coordinators.items():
            is_ready = is_ready and v.check_finished_ping_round()
        return is_ready
        
    def collect_all_addresses(self):
        print(f"Collecting addresses from {len(self.site_coordinators.keys())} number of coordinators")
        self.all_addresses=node_to_ip
        for k, v in self.site_coordinators.items():
            print("Collecting address from:", k)
            self.all_addresses.update(v.nodes_to_global_addresses)
            print("all addresses:", self.all_addresses)

    def propagate_all_addresses(self):
        print(f"Propagating all_addresses to {len(self.site_coordinators.keys())} number of coordinators")
        for k, v in self.site_coordinators.items():
            print(f"Propagating all_addresses to {k}..")
            v.all_nodes_to_addresses = self.all_addresses

    def collect_all_measurements(self):
        print(f"Collecting measurements from {len(self.site_coordinators.keys())} number of coordinators")
        self.all_measurements=dict()
        for k, v in self.site_coordinators.items():
            print(f"Collecting {len(v.ping_measurements.keys())} from {k}")
            self.all_measurements.update(v.ping_measurements)

    def finish_experiment(self):
        print("Finishing the experiment from site script..")
        for s in self.site_coordinators.values():
            s.finish()



    ''' ----------------------- READ/WRITE ----------------------- '''

    def write_addresses(self):
        timestamp = time.time()
        date_object = datetime.fromtimestamp(timestamp)
        formatted_time = date_object.strftime('%Y-%m-%d_%H:%M')
        file_name = f"all_nodes_to_addresses"
        print(f"Writing all addresses to {file_name}")
        with open(f"./experiment_data/{self.experiment_id}/results/{file_name}.json", 'w') as file:
            json.dump(self.all_addresses, file) 
        file_name = f"all_addresses_{formatted_time}"
        print(f"Writing all addresses to {file_name}")
        with open(f"./experiment_data/{self.experiment_id}/results/{file_name}.json", 'w') as file:
            json.dump(self.all_addresses, file) 
      

    # def write_all_nodes(self):
    #     print("Writing all_addresses to results..")
    #     with open(f"{self.absolute_path}/experiment_data/{self.experiment_id}/results/all_addresses.json", "w") as file:
    #         json.dump(self.all_addresses, file, indent=4)

    def write_all_measurements(self):
        timestamp = time.time()
        date_object = datetime.fromtimestamp(timestamp)
        formatted_time = date_object.strftime('%Y-%m-%d_%H:%M')
        file_name = f"ping_measurements_{formatted_time}"
        print(f"Writing all measurements to {file_name}")
        converted_dict = {str(key): value for key, value in self.all_measurements.items()}
        with open(f"./experiment_data/{self.experiment_id}/results/{file_name}.json", 'w') as file:
            json.dump(converted_dict, file)        
      
    # def write_border_routers(self):

    #     for k in self.site_coordinators.keys():
    #         if "m3" in k:
    #             print("Writing the border routers for", k)
    #             self.site_coordinators[k]

    #     pass

    def write_experiment_conf(self):
        with open(f"./experiment_data/{self.experiment_id}/results/experiment_config.json", 'w') as file:
            json.dump(self.experiment_conf, file)

