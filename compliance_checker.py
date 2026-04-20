import csv
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
import threading

def compliance(device):
        try:
            connection=ConnectHandler(**device)
            connection.enable()
            hostname=connection.find_prompt().strip("#").strip(">")
            clock_status=connection.send_command("show run | section clock")
            if "summer-time AEDT recurring 1 Sun Oct 2:00 1 Sun Apr 3:00" not in clock_status:
                dst_conf=[
                    "clock summer-time AEDT recurring 1 Sun Oct 2:00 1 Sun Apr 3:00"

                ]
                connection.send_config_set(dst_conf)
                print(f"Daylight Savings Time rule added to {hostname}")
            input_status=connection.send_command("sh run | include transport")
            if "telnet" in input_status:
                telnet_dis=[
                    "line vty 0 4",
                    "transport input ssh"
                ]
                connection.send_config_set(telnet_dis)
                print(f"Telnet disabled on {hostname}")
            banner_status=connection.send_command("sh run | section banner")
            if "Unauthorized access prohibited!" not in banner_status:
                banner_set=[
                    "banner motd # Unauthorized access prohibited! #"
                ]
                connection.send_config_set(banner_set)               
                print(f"Banner added to {hostname}")
            timestamp_status=connection.send_command("sh run | include timestamps log")
            if "no service timestamps log" in timestamp_status:
                timestamp_set=[
                    "service timestamps log"
                ]
                connection.send_config_set(timestamp_set)
                print(f"Timestamped log messages enabled on {hostname}")
            else:
                print(f"Router {hostname} is compliant")

            connection.save_config()
            connection.disconnect()
        except NetmikoTimeoutException:
            print(f"{device['host']} timed out.")
        except NetmikoAuthenticationException:
            print(f"{device['host']} could not be reached due to authentication failure.")
        except Exception as e:
            print(f"Unexpected error on {device['host']}: {e}")

threads=[]



with open ("inventory.csv") as f:
    reader = csv.DictReader(f)
    for device in reader:
        th=threading.Thread(target=compliance,args=(device, ))
        threads.append(th)

for th in threads:
    th.start()
for th in threads:
    th.join()

