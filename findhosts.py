import requests,json,argparse,ipaddress
def extract_hostnames_from_ip(ip):
    url = "https://api.securitytrails.com/v1/ips/nearby/"
    headers = {"APIKEY": "YOUR_KEY"}
    response = requests.get(url+ip, headers=headers, verify=False)
    response_json = json.loads(response.content)
    res={}
    try: 
      for block in response_json["blocks"]:
         if ip in block["ip"]:
          if len(block["hostnames"])>1:
           res[ip]=block["hostnames"]
    except KeyError as e:
        print("Error with  ip",ip)
    return(res)
def extract_hostnames_from_cidr(cidr):
    ip_list = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
    res={}
    for ip in ip_list:
       r1=extract_hostnames_from_ip(ip)
       res[ip]=r1[ip]
    return(res)
def write_to_file(res,name):
    with open(name, "w", encoding="UTF-8") as fp:
        for ip in res:
            if len(res["ip"])<1:
              fp.write("hostname :- ",str(res["ip"][0]))
            else:
              fp.write("hostnames :- ",'.'.join(map(str, res["ip"])))
            fp.write("\nip :- ",str(ip)+'\n')
parser = argparse.ArgumentParser()
parser.add_argument("-o", help = "outputfile")
parser.add_argument("-cidr",help = "Takes cidr")
parser.add_argument("-ip",help = "Takes ip")
args=parser.parse_args()  
if args.ip:
    a1=extract_hostnames_from_ip(args.ip)
    print(a1)
    if args.o:
        write_to_file(a1,args.o)
elif args.cidr:
    a1=extract_hostnames_from_cidr(args.cidr)
    print(a1)
    if args.o:
        write_to_file(a1,args.o)
