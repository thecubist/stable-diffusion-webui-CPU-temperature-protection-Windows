# CPU temperature protection
### Original CPU Temp Protection Repository
This extension was forked from w-e-w's CPU Temperature Protection extension which can be found here 
https://github.com/w-e-w/stable-diffusion-webui-GPU-temperature-protection 

### Disclaimer
This repository is currently in development and may be unstable or non functional for many users. The project has only been tested on a machine equiped with an Intel CPU. 

Use at your own risk

### Pause image generation when CPU temperature exceeds threshold
this extension uses nvidia-smi to monitor CPU temperature at the end of each step, if temperature exceeds threshold pause image generation until criteria are met.

## Requirements
### Open Hardware Monitor
Open Hardware Monitor (OHM) is used to access the temperature sensors for the CPU and must be running in the background for this extension to function. You can get Open Hardware Monitor from 
https://openhardwaremonitor.org/
### WMI
The WMI is used to access information within OHM and must be installed in the stable diffusion virtual environment in order to function. This extension supports auto installing WMI. If WMI does not auto install you can manually install this dependency by navigating to the stable diffusion folder and running the commands
```
venv/scripts/activate
```
to activate the virtual environment so pip targets the correct location 
```
pip install wmi
```
to install WMI 

## Installation
Install using extensions tab `Install from URL` by manually copying the repository URL
```
https://github.com/thecubist/stable-diffusion-webui-CPU-temperature-protection-Windows.git
```
![image](https://github.com/thecubist/stable-diffusion-webui-CPU-temperature-protection-Windows/assets/36249159/c77838ba-eee6-42d6-9a06-ba5d03d6bf38)

# writing beyond this point is from the original repository and will be updated once extension is updated
## Setting
Settings can be found at `Setting` > `CPU Temperature`

- `CPU temperature monitor minimum interval`
    - checking temperature too often will reduce image generation performance
    - set to `0` well effectively disable this extension
    - to completely disable extension disable the file extension tab
- `CPU sleep temperature`
    - generation will pause if CPU core temperature exceeds this temperature
- `CPU wake temperature`
    - generation will continue to pause until temperature has drops below this temperature 
    - setting a higher value than `CPU sleep temperature`will effectively disable this
- `Sleep Time`
    - seconds to sleep before checking temperature again
- `Max sleep Time` 
    - max number of seconds that it's allowed to pause
    - generation will continue disregarding `CPU wake temperature` after the allotted time has passed
    - set to `0` disable this limit allowing it to pause indefinitely
- `Print CPU Core temperature while sleeping in terminal`
    - print the CPU core temperature reading from nvidia-smi to console when generation is paused
    - providing information

## Notes
- Temperature unit Celsius, Time unit seconds
- Be advised, repeatedly lowering and raising the temperature of a CPU in quick succession can in some situations lower the lifespan of the CPU. This extension is not a replacement for effective CPU cooling and should be used with caution
