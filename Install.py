import launch
import sys

#platform specific installs
if sys.platform.startswith('win'): # Windows installs
    print("CPU Temp Installer: Windows Detected")
    if not launch.is_installed("wmi"):
        print("CPU Temp: WMI not found \n OS: Windows Detected \n Action: Attempting WMI install using pip")
        launch.run_pip("install wmi") 
elif sys.platform.startswith('linux'): # Linux installs
    print("CPU Temp Installer: Linux Detected")
elif sys.platform.startswith('darwin'): # Mac installs
    print("CPU Temp Installer: MacOS Detected")
else:
    print("CPU Temp Installer: Unknown OS")