# virtual-smart-remote
This project combines GNU Radio and PyQt to control an off-the-shelf smart outlet set. GUI widget replaces handheld remote to control any home appliance, lights, etc. from a distance. 

This code was used as part of a training session to demonstrate analysis and imitation of basic RF communication. An SDR transciever was used to capture, deconstruct, and resynthesize simple OOK patterns around 434MHz. See section below for product details.  
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/28e304ad-4e0e-42ba-970e-706c8a65c282" width=320>
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/160d0bb5-d26e-4fdf-958d-2dbc5dde47ca" width=320>
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/618129fc-4a9a-443d-a65f-a490dac8b342" width=320>


## Target Device
**ETEKCITY Remote Outlet Switch**  
"ZAP 3LX"  
https://etekcity.com/products/remote-outlet-zap-3lx-s  
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/64705fff-3e21-4ccb-acf3-b344422e2ae5" width=200>
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/b7e7bb1c-ae0c-4a32-ad84-89d23841b25e" width=200>


## Requirements
* Python (version 3.x)
* GNU Radio (version 3.7 or later)
* GNU Radio-compatible SDR transmitter (HackRF One, BladeRF, LimeSDR, etc.)
  
## Running the application
1. Clone repository
2. With radio plugged in, run:  `sudo python3 zapctl.py`  
(*Note: Buttons 3 & 4 have not been implemented...feel free to add these for RF hacking practice!*)
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/949c52c4-6c1c-4317-bd09-0043fa8673fb" width=400>
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/9dedf649-5366-44cd-8c40-7ed77d5e6a49" width=200>
<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/322e4d86-ffb5-4c0d-8bd2-2c2b54045622" width=200>

<img src="https://github.com/jrabinowitz2/virtual-smart-remote/assets/45504513/3da80844-789c-428c-a23f-d9cff2c7d69a" >





