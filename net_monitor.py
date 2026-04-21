import os
import csv
from datetime import datetime
import requests
import time
import threading
from dotenv import load_dotenv
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException,NetmikoTimeoutException

load_dotenv()
url = os.environ.get("SLACK_WEBHOOK_URL")
def slack_alert(alert):
     payload={"text":alert}
     return requests.post(url, json=payload)

def monitor(device):
        try:   
            connection = ConnectHandler(**device)
            connection.enable()
            raw_name=connection.find_prompt()
            hostname=raw_name.strip("#").strip(">")
            int_brief=connection.send_command("sh ip int br")
            int_list=int_brief.strip().splitlines()
            for interface in int_list:
                interface=interface.strip().split()
                if "Interface" not in interface and interface[1]!= "unassigned" and interface[4]!="up":
                    int_alert= (f"ALERT! {hostname} Interface {interface[0]} is down")
                    print(int_alert)
                    slack_alert(int_alert)
                elif interface[1]!= "unassigned" and interface[4]=="up":
                    print(f"{hostname} - Interface{interface[0]} is healthy")
            bgp_sum=connection.send_command("sh bg sum")
            bgp_list=bgp_sum.strip().splitlines()
            for session in bgp_list:
                session=session.strip().split()
                if len(session)==10 and "BGP" not in session and "memory" not in session and "AS" not in session and not session[9].isnumeric():
                    bgp_alert=(f"ALERT! {hostname} BGP session with {session[0]} is not Established")
                    print(bgp_alert)
                    slack_alert(bgp_alert)
                elif len(session)==10 and "BGP" not in session and "memory" not in session and "AS" not in session  and session[9].isnumeric():
                    print(f"{hostname}- BGP Session with {session[0]} is healthy") 
              

            connection.disconnect()
        except NetmikoTimeoutException:
                print(f"{device['host']} timed out.")
        except NetmikoAuthenticationException:
                print(f"{device['host']} could not be reached due to authentication failure.")
        except Exception as e:
                print(f"Unexpected error on {device['host']}: {e}")

while True:
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H:%M:%S")
    print(f"{timestamp}: Polling the devices...")
    threads=list()
    with open ("inventory.csv") as f:
        reader=csv.DictReader(f)
        for device in reader:
            th=threading.Thread(target=monitor,args=(device, ))
            threads.append(th)
            th.start()


     
    for th in threads:
        th.join()
    time.sleep(60)


