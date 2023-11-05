# virtual-smart-remote
This project combines GNU Radio and PyQt to control an off-the-shelf smart outlet set. GUI widget replaces handheld remote to control any home appliance, lights, etc. from a distance. 

This code was used as part of a training session to demonstrate analysis and imitation of basic RF communication. An SDR transciever was used to capture, deconstruct, and resynthesize simple OOK patterns around 434MHz. See section below for product details.

## Target Device
ETEKCITY Remote Outlet Switch  
"ZAP 3LX"  
https://etekcity.com/products/remote-outlet-zap-3lx-s

## Requirements
* python
* GNU Radio (3.7 or later)
* GNU Radio-compatible SDR transmitter
  
## Running the application
1. Clone repository
2. Run with: `sudo python zapctl.py` 
