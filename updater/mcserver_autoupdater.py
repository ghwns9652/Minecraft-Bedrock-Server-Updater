# Automatically compare installed version of Minecrafter server to latest version 
import requests
import logging
from bs4 import BeautifulSoup
import subprocess
import os
import sys
import datetime

# Write down your absolute path of Minecraft Bedrock Server Updater
# Example : 
#   minecraft_directory = '/home/ubuntu/Minecraft-Bedrock-Server-Updater'
# Do not write '/' at the end of the path!
minecraft_directory = '/path/to/updater'

URL = "https://www.minecraft.net/en-us/download/server/bedrock/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

try:
 page = requests.get(URL, headers=HEADERS, timeout=5)
except requests.exceptions.Timeout:
  logging.error("timeout raised, recovering")

soup = BeautifulSoup(page.content, "html.parser")

a_tag_res = []
for a_tags in soup.findAll('a', attrs={"aria-label":"Download Minecraft Dedicated Server software for Ubuntu (Linux)"}):
  a_tag_res.append(a_tags['href'])

download_link=a_tag_res[0]

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

