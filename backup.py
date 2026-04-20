import csv
from datetime import datetime
import threading
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

thread_list=[]

def backup(device):
            try:
                connection = ConnectHandler(**device)
                connection.enable()
                hostname = connection.find_prompt().strip("#").strip(">")
                output = connection.send_command("sh run")
                now = datetime.now()
                timestamp = now.strftime("%d%m%Y_%H%M%S")
                filename = (f"backup_{hostname}_{timestamp}.txt")
                with open (filename,"w") as file:
                    file.write(output)
                    
                    
                print(f"Backup saved! {filename}")
                
                connection.disconnect()
            except NetmikoTimeoutException:
                print(f"{device['host']} timed out.")
            except NetmikoAuthenticationException:
                print(f"{device['host']} could not be reached due to authentication failure.")
            except Exception as e:
                print(f"Unexpected error on {device['host']}: {e}")


with open ("inventory.csv") as f:
    reader = csv.DictReader(f)
    for device in reader:
         th=threading.Thread(target=backup, args=(device, ))
         thread_list.append(th)

for th in thread_list:
     th.start()

for th in thread_list:
     th.join()


         
            


