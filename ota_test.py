from ota import OTAUpdater
# from wifi_config import SSID, PASSWORD

SSID = 'GC_Star24'
PASSWORD = 'Misty911!'

firmware_url = "https://raw.githubusercontent.com/wilki48/test_ota/main/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test_file.py")

ota_updater.download_and_install_update_if_available()