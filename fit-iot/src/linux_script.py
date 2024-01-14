import asyncio
import sys

'''
This is stored in ~/shared directory on each site, and will only executed from the sites. 
'''

async def run_ping(destinations):
    results = dict()
    tasks = [asyncio.create_subprocess_exec(
                'ping', '-c', '2', d,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            for d in destinations]

    completed_tasks = await asyncio.gather(*tasks)
    
    for d, task in zip(destinations, completed_tasks):
        stdout, stderr = await task.communicate()
        if stdout:
            results[d] = read_ping_result(stdout.decode())
        elif stderr: 
            results[d] = f"ERR: {stderr.decode()}"
            
    print(results)

def parse_address_list(input_str):
    # Remove brackets and split the string by commas
    addresses = input_str.strip("[]").split(',')
    # Strip whitespace and return the list
    return [address.strip() for address in addresses]

def read_ping_result(res):
    if "0 received" in res:
        return "NA"
    splitted = res.split('\n')
    for s in splitted:
        if "min/avg/max/mdev" in s:
            return s.split()[3].split('/')[1]

if __name__ == "__main__":
    dest_addresses = sys.argv[1]
    dest_address_list = parse_address_list(dest_addresses)
    asyncio.run(run_ping(dest_address_list))


