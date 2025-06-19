# Automatically compare installed version of Minecrafter server to latest version 
import requests
import logging
import subprocess
import os
import sys
import datetime

# Write down your absolute path of Minecraft Bedrock Server Updater
# Example : 
#   minecraft_directory = '/home/ubuntu/Minecraft-Bedrock-Server-Updater'
# Do not write '/' at the end of the path!
minecraft_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URL = "https://www.minecraft.net/en-us/download/server/bedrock/"
BACKUP_URL = "https://raw.githubusercontent.com/ghwns9652/Minecraft-Bedrock-Server-Updater/main/backup_download_link.txt"
DOWNLOAD_LINKS_URL = "https://net-secondary.web.minecraft-services.net/api/v1.0/download/links"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

try:
    response = requests.get(DOWNLOAD_LINKS_URL, headers=HEADERS, timeout=5)
    response_json = response.json()
    
    all_links = response_json['result']['links']
    download_link = None
    
    # Find the serverBedrockLinux download link
    for link in all_links:
        if link['downloadType'] == 'serverBedrockLinux':
            download_link = link['downloadUrl']
            break
    
    if download_link is None:
        raise Exception("serverBedrockLinux download link not found")

except requests.exceptions.Timeout:
    logging.error("timeout raised, recovering")
    response = requests.get(BACKUP_URL, headers=HEADERS, timeout=5)

    download_link=response.text

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
    subprocess.run(['wget', '--user-agent', HEADERS['User-Agent'], '-P', minecraft_directory+'/updater', '-c', download_link])
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
    subprocess.run(['wget', '--user-agent', HEADERS['User-Agent'], '-P', minecraft_directory+'/updater', '-c', download_link])
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

