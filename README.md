# CPU temperature protection
### Original GPU Temp Protection Repository
This extension was forked from w-e-w's GPU Temperature Protection extension which can be found here 
https://github.com/w-e-w/stable-diffusion-webui-GPU-temperature-protection 

### Disclaimer
This repository is currently in development and may be unstable or non functional for many users. It is not advisable to use this repository in it's current state. Use at your own risk

### Pause image generation when GPU temperature exceeds threshold
this extension uses nvidia-smi to monitor GPU temperature at the end of each step, if temperature exceeds threshold pause image generation until criteria are met.

## Requirements
Only tested on systems with an Intel CPU

## Installation
Install using extensions tab `Install from URL` by manually copying the repository URL
```
https://github.com/thecubist/stable-diffusion-webui-CPU-temperature-protection-Windows.git
```
# writing beyond this point is from the original repository and will be updated once extension is updated
## Setting
Settings can be found at `Setting` > `GPU Temperature`

- `GPU temperature monitor minimum interval`
    - checking temperature too often will reduce image generation performance
    - set to `0` well effectively disable this extension
    - to completely disable extension disable the file extension tab
- `GPU sleep temperature`
    - generation will pause if GPU core temperature exceeds this temperature
- `GPU wake temperature`
    - generation will continue to pause until temperature has drops below this temperature 
    - setting a higher value than `GPU sleep temperature`will effectively disable this
- `Sleep Time`
    - seconds to sleep before checking temperature again
- `Max sleep Time` 
    - max number of seconds that it's allowed to pause
    - generation will continue disregarding `GPU wake temperature` after the allotted time has passed
    - set to `0` disable this limit allowing it to pause indefinitely
- `Print GPU Core temperature while sleeping in terminal`
    - print the GPU core temperature reading from nvidia-smi to console when generation is paused
    - providing information

## Notes
- Temperature unit Celsius, Time unit seconds
- To be honest I don't recommend anyone using this extension, if your GPU is having temperature issues and don't have the means to improve the cooling, then recommend using software like MSI afterburner to undervolt or further power limit or thermal limit the GPU.
