import ipaddress
import requests
import json
from tqdm import tqdm
import argparse
 
# Initialize parser

def extract_hostnames_from_cidr(cidr, customer_list=None):
    url = "https://api.securitytrails.com/v1/ips/nearby/"
    headers = {"APIKEY": "YOUR_KEY"}

    ip_list = [url + ip for ip in (str(ip) for ip in ipaddress.IPv4Network(cidr))]
    
    hostnames = set()
    ports = set()
    customers = set()
    for ip in tqdm(ip_list):
        response = requests.request("GET", ip, headers=headers, verify=False)
        response_json = json.loads(response.content)
        try: 
            for block in response_json["blocks"]:
                hostnames.update(block["hostnames"])
                ports.update(block["ports"])
        except KeyError as e:
            print(ip)

    if customer_list:
        for each in hostnames:
            if each in customer_list:
                customers.update(each)
        return hostnames, customers, ports
    return hostnames, ports

def write_to_file(object_list, name):
    with open(name, "w", encoding="UTF-8") as fp:
        for each in object_list:
            fp.write(str(each))
            fp.write("\n")          
parser = argparse.ArgumentParser()
parser.add_argument("-o", help = "outputfile")
parser.add_argument("-cidr",help = "Takes cidr")
parser.add_argument("-ip",help = "Takes ip")
parser.add_argument("-i",help = "Takes input file")
args=parser.parse_args()    
