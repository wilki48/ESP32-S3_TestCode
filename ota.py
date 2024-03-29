import network
import urequests
import os
import json
import machine
from time import sleep 

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them.
    Branch must be names main in github"""
    def __init__(self, ssid, password, repo_url, filename):
        self.filename = filename
        self.versionFilename = filename.replace('.py', '_version.json')
        self.ssid = ssid
        self.password = password
        self.repo_url = repo_url

        # self.version_url = repo_url + 'main/version.json'                 # Replacement of the version mechanism by Github's oid
        self.version_url = self.process_version_url(repo_url, filename)     # Process the new version url
        self.firmware_url = repo_url + filename                             # Removal of the 'main' branch to allow different sources
        print(f'self.firmware_url: {self.firmware_url}')
        # get the current version (stored in version.json)
        print(f'*** versionFilename: {self.versionFilename}')
        if self.versionFilename in os.listdir():
            print(f'Found {self.versionFilename} file')
            with open(self.versionFilename) as f:
                self.current_version = json.load(f)['version']
            print(f"Current file version is '{self.current_version}'")

        else:
            print('Creating version.json file')
            self.current_version = "0"
            # save the current version
            with open(self.versionFilename, 'w') as f:
                json.dump({'version': self.current_version}, f)
            
    def process_version_url(self, repo_url, filename):
        """ Convert the file's url to its assoicatied version based on Github's oid management."""

        # Necessary URL manipulations
        version_url = repo_url.replace("raw.githubusercontent.com", "github.com")  # Change the domain
        #print('version url 1: ', version_url)
        version_url = version_url.replace("/", "§", 4)                             # Temporary change for upcoming replace
        #print('version url 2: ', version_url)
        version_url = version_url.replace("/", "/latest-commit/", 1)               # Replacing for latest commit
        #print('version url 3: ', version_url)
        version_url = version_url.replace("§", "/", 4)                             # Rollback Temporary change
        #print('version url 4: ', version_url)
        version_url = version_url + filename                                       # Add the targeted filename
        
        print('version url: ', version_url)
        
        return version_url

    def connect_wifi(self):
        """ Connect to Wi-Fi."""

        sta_if = network.WLAN(network.STA_IF)
        if sta_if.isconnected():
            print('Already connected to wifi...')
            return
        
        print('connecting...')
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        
    def fetch_latest_code(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        response = urequests.get(self.firmware_url)
        if response.status_code == 200:    
            # Save the fetched code to memory
            self.latest_code = response.text
            return True
        
        elif response.status_code == 404:
            print('Firmware not found.')
            return False

    def update_no_reset(self):
        """ Update the code without resetting the device."""

        print('Udate no reset')
        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            result = f.write(self.latest_code)
        
        # update the version in memory
        self.current_version = self.latest_version

        # save the current version
        with open(self.versionFilename, 'w') as f:
            json.dump({'version': self.current_version}, f)
        
        # free up some memory
        self.latest_code = None

        # Overwrite the old code.
        print(f'filename: {self.filename}')
        os.rename('latest_code.py', self.filename)
        
    def update_and_reset(self):
        """ Update the code and reset the device."""

        print('Updating and reset device...')
        print(f'filename: {self.filename}')
        # Overwrite the old code.
        #os.rename('latest_code.py', self.filename)

        # Restart the device to run the new code.
        #print("Restarting device after update and reset...")
        #sleep(0.25)
        #machine.reset()  # Reset the device to run the new code.
        
    def check_for_updates(self):
        """ Check if updates are available."""
        
        print('def check_for_updates(self):')
        # Connect to Wi-Fi
        self.connect_wifi()

        headers = {"accept": "application/json"} 
        response = urequests.get(self.version_url, headers=headers)
        
        data = json.loads(response.text)
       
        self.latest_version = data['oid']                   # Access directly the id managed by GitHub
        print(f'latest version is: {self.latest_version}')
        
        # compare versions
        newer_version_available = True if self.current_version != self.latest_version else False
        print(f'Newer version available: {newer_version_available}')
         
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        if self.check_for_updates():
            if self.fetch_latest_code():
                self.update_no_reset()
                #self.update_and_reset()
                return True
        else:
            print('No new updates available.')
            return False
