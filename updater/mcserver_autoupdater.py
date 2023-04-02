# Automatically compare installed version of Minecrafter server to latest version 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import subprocess
import os
import sys
import datetime

# Write down your absolute path of Minecraft Bedrock Server Updater
# Example : 
#   minecraft_directory = '/home/ubuntu/Minecraft-Bedrock-Server-Updater'
# Do not write '/' at the end of the path!
minecraft_directory = '/path/to/updater'

url = 'https://www.minecraft.net/en-us/download/server/bedrock'

options = Options()
options.add_argument('-headless')

browser = webdriver.Firefox(options=options)
browser.get(url)

# Find the element with the specified aria-label
element = browser.find_element(By.XPATH, '//*[@aria-label="Download Minecraft Dedicated Server software for Ubuntu (Linux)"]')

# Extract the href attribute
download_link = element.get_attribute('href')

print("Download link:", download_link)

download_link_file = minecraft_directory+'/updater/download_link.txt'
if not os.path.isfile(download_link_file):
    with open(download_link_file, 'w') as file:
        file.write('hello minecraft!')

with open(download_link_file, 'r') as file:
    prev_download_link = file.read();

logfile = minecraft_directory+'/updater/update.log'

running_files = os.listdir(minecraft_directory+'/running')
if len(running_files) == 0:
    # Download server binary
    subprocess.run(['wget', '-P', minecraft_directory+'/updater', download_link])
    # Save the download link to a text file
    with open(download_link_file, 'w') as file:
        file.write(download_link)
    # Migrate current server to newest version (preserves server settings & world data)
    subprocess.run(['bash', minecraft_directory+'/updater/migrate.sh', minecraft_directory])
    # run MC server
    subprocess.run(['bash', minecraft_directory+'/updater/startserver.sh', minecraft_directory])
    with open(logfile, 'a') as file:
        timenow = "["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"]"
        new_version = "v"+download_link[download_link.find('bedrock')+15:download_link.find('.zip')]
        msg = timenow+" minecraft server is installed "+"("+new_version+")\n"
        print(msg)
        file.write(msg)

elif download_link != prev_download_link:
    # Download server binary
    subprocess.run(['wget', '-P', minecraft_directory+'/updater', download_link])
    # Save the download link to a text file
    with open(download_link_file, 'w') as file:
        file.write(download_link)
    # Stop MC server safely
    subprocess.run(['bash', minecraft_directory+'/updater/stopserver.sh'])
    # Migrate current server to newest version (preserves server settings & world data)
    subprocess.run(['bash', minecraft_directory+'/updater/migrate.sh', minecraft_directory])
    # run MC server
    subprocess.run(['bash', minecraft_directory+'/updater/startserver.sh', minecraft_directory])
    with open(logfile, 'a') as file:
        timenow = "["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"]"
        if prev_download_link == 'hello minecraft!':
            prev_version = 'unknown'
        else :
            prev_version = "v"+prev_download_link[prev_download_link.find('bedrock')+15:prev_download_link.find('.zip')]
        new_version = "v"+download_link[download_link.find('bedrock')+15:download_link.find('.zip')]
        msg = timenow+" minecraft server is updated "+"("+prev_version+" -> "+new_version+")\n"
        print(msg)
        file.write(msg)
else:
    with open(logfile, 'a') as file:
        timenow = "["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"]"
        msg = timenow+" minecraft server is already newest version. nothing to update.\n"
        print(msg)
        file.write(msg)

browser.quit()

