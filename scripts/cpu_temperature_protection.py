import gradio as gr
import time
import pythoncom
from modules.sd_samplers_kdiffusion import KDiffusionSampler
from modules import scripts, shared
import launch
import sys 
# OS specific imports
try:
    import wmi #WMI used for windows support
except Exception as e:
    if sys.platform.startswith('win'):
        print("CPU Temp Error: WMI not found on Windows platform, please restart SD to auto install WMI")

#settings for the UI
shared.options_templates.update(shared.options_section(('CPU_temperature_protection', "CPU Temperature"), {
    "cpu_temps_sleep_enable": shared.OptionInfo(True, "Enable CPU temperature protection"),
    "cpu_temps_sleep_print": shared.OptionInfo(True, "Print CPU Core temperature while sleeping in terminal"),
    "cpu_temps_sleep_minimum_interval": shared.OptionInfo(5.0, "CPU temperature monitor minimum interval", gr.Number).info("won't check the temperature again until this amount of seconds have passed"),
    "cpu_temps_sleep_sleep_time": shared.OptionInfo(1.0, "Sleep Time", gr.Number).info("seconds to pause before checking temperature again"),
    "cpu_temps_sleep_max_sleep_time": shared.OptionInfo(10.0, "Max sleep Time", gr.Number).info("max number of seconds that it's allowed to pause, 0=unlimited"),
    "cpu_temps_sleep_sleep_temp": shared.OptionInfo(75.0, "CPU sleep temperature", gr.Slider, {"minimum": 0, "maximum": 125}).info("generation will pause if CPU core temperature exceeds this temperature"),
    "cpu_temps_sleep_wake_temp": shared.OptionInfo(75.0, "CPU wake temperature", gr.Slider, {"minimum": 0, "maximum": 125}).info("generation will pause until CPU core temperature drops below this temperature"),
}))
    
class CPUTemperatureProtection(scripts.Script):
    def title(self):
        return "CPU temperature protection"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def process(self, p, *args):
        if shared.opts.cpu_temps_sleep_enable:
            setattr(KDiffusionSampler, "callback_state", CPUTemperatureProtection.cpu_temperature_protection_decorator(KDiffusionSampler.callback_state))

    def get_cpu_package_temperature():
    # ----------------------- windows mode --------------------------
        try: #catch errors caused by WMI or OHM not running
            
            pythoncom.CoInitialize()  # Start thread
            temperature_infos = wmi.WMI(namespace="root\\OpenHardwareMonitor").Sensor()  # Holds all temperature info
            for sensor in temperature_infos: #search for CPU package sensor
                if sensor.SensorType == "Temperature" and sensor.Name == "CPU Package":
                    return float(sensor.Value)
        except Exception as e:
            print(f'[Error getting CPU package temperature]: {e}') # add different prints based on commonly thrown errors
        finally:
            pythoncom.CoUninitialize()  # Close thread
    # ---------------------------------------------------------------
        return 0

    @staticmethod
    def cpu_temperature_protection():
        if shared.opts.cpu_temps_sleep_enable:
            call_time = time.time()
            if call_time - CPUTemperatureProtection.last_call_time > shared.opts.cpu_temps_sleep_minimum_interval:
                cpu_core_temp = CPUTemperatureProtection.get_cpu_package_temperature()
                if cpu_core_temp > shared.opts.cpu_temps_sleep_sleep_temp:

                    if shared.opts.cpu_temps_sleep_print:
                        print(f'\n\nCPU Temperature: {cpu_core_temp}°C')

                    time.sleep(shared.opts.cpu_temps_sleep_sleep_time)
                    cpu_core_temp = CPUTemperatureProtection.get_cpu_package_temperature()
                    while cpu_core_temp > shared.opts.cpu_temps_sleep_wake_temp and (not shared.opts.cpu_temps_sleep_max_sleep_time or shared.opts.cpu_temps_sleep_max_sleep_time > time.time() - call_time) and shared.opts.cpu_temps_sleep_enable:
                        if shared.opts.cpu_temps_sleep_print:
                            print(f'CPU Temperature: {cpu_core_temp}°C')

                        time.sleep(shared.opts.cpu_temps_sleep_sleep_time)
                        cpu_core_temp = CPUTemperatureProtection.get_cpu_package_temperature()

                    CPUTemperatureProtection.last_call_time = time.time()
                else:
                    CPUTemperatureProtection.last_call_time = call_time

    @staticmethod
    def cpu_temperature_protection_decorator(fun):
        def wrapper(*args, **kwargs):
            result = fun(*args, **kwargs)
            CPUTemperatureProtection.cpu_temperature_protection()
            return result
        return wrapper

    last_call_time = time.time()
