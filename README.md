Multi-Threaded Network Automation Suite

Overview

A Python-based automation framework designed to manage Cisco IOU devices in a GNS3 environment. This suite handles the three pillars of network operations: Backup, Monitoring, and Compliance.

Core Features

    Backup Engine: Automatically captures and timestamps running configurations for version control.

    Real-time Monitor: Polling system that detects interface failures and BGP neighbor drops, sending instant alerts to Slack.

    Compliance Remediation: A "self-healing" script that enforces network standards (Disabling Telnet, enabling timestamps on log messages, adding MOTD banners, and ensuring AEDT time synchronization).

Tech Stack

    Language: Python 3.x

    External Dependencies: Netmiko (SSH), Requests (Webhooks), Dotenv.

    Environment: Ubuntu 22.04 VM, GNS3, Cisco IOU.

### **Lab Environment Setup (GNS3)**
To run these scripts, you need a functional network topology. This project was built and tested using:
* **GNS3:** Network simulation software.
* **Cisco IOU (IOS on Unix):** L3 images (Cisco IOS Software, Linux Software (I86BI_LINUX-L3-ADVENTERPRISEK9-M)).
* **Nodes:** 5 Routers (Router1 through ROuter5).
* **Connectivity:** * All routers must be reachable via SSH from the host running the scripts (Ubuntu VM).
    * A **NAT Cloud** was used in GNS3 to provide the Ubuntu VM access to the IOU management interfaces.


Topology

<img width="771" height="455" alt="Topology" src="https://github.com/user-attachments/assets/001c2efb-2804-4645-8274-3e1045074dff" />



How to Use

    Clone the repo.

    Populate example_inventory.csv with your device details.
    
    Rename .env.example to .env and add your Slack Webhook URL.

    Run the Python scripts
    For Monitoring: python3 monitor.py
    For Backups: python3 backup.py
    For Compliance: python3 compliance.py
