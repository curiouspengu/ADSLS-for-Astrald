from collections import deque
import random
from time import sleep
import webbrowser
import subprocess

import datetime
import requests

DEBUG_MODE = False
CURRENT_VERSION = "ADSLS-v1.3"

def fetch_links():
    api_url = 'http://curiouspengu.pythonanywhere.com/link_relay/get_links/'    
    response = requests.get(api_url)
    links = response.json().get('links', [])
    return links


def check_for_updates():
    url = f"https://api.github.com/repos/curiouspengu/ADSLS-for-Astrald/releases"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        releases = response.json()
        if releases:
            latest_release = releases[0]["tag_name"]
        else:
            return "No releases found"
    else:
        return
    
    if (not CURRENT_VERSION == latest_release):
        print("You can update! Update here:\nhttps://github.com/curiouspengu/ADSLS-for-Astrald/releases\n")
        print(f"Your version: {CURRENT_VERSION}")
        print(f"Latest version: {latest_release}")
        print("Wait 5 seconds.")
        sleep(5)
        input("Press enter to continue... ")

def main():
    sniped_tables = []
    for table in ["glitch", "jester", "mari"]:
        print(f"Would you like to snipe {table} links?")
        ans = input("Y/N: ")
        print()
        if ans.lower() == "y":
            sniped_tables.append(table + "_config.json")


    if DEBUG_MODE == False:
        print("""Just to let you know that you can donate here:
https://www.roblox.com/games/5080477735/Donations-to-Curious-Pengu#!/store

I'm not forcing you to donate, but at the end of the day most of Radiant Team's products will be completely free, so donations of any size and shape are greatly appreciated.
""")
        sleep(10)
        print("RUNNING | CLOSE THIS WINDOW TO EXIT | KEEP THIS WINDOW OPEN")
    sp()

    previous_links = deque()
    while True:
        links = fetch_links()
        
        if DEBUG_MODE == True:
            print(links)
        
        for link in links:
            if not link["table"] in sniped_tables:
                if DEBUG_MODE == True:
                    print("REJECTED DUE TO NOT SNIPING")
                continue
            if link["id"] in previous_links:
                if DEBUG_MODE == True:
                    print("REJECTED DUE TO DUPLICATE")
                continue
            else:
                previous_links.append(link["id"])
            
            timestamp = datetime.datetime.strptime(link["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
            duration = datetime.datetime.now(datetime.timezone.utc) - timestamp
            duration_in_s = duration.total_seconds()
            if divmod(duration_in_s, 3600)[0] < 1:
                if divmod(duration_in_s, 60)[0] < 4:
                    if "https://www.roblox.com/games/15532962292/Sols-RNG-Eon1-1?privateServerLinkCode=" in link["url"]:
                        join_ps_link(link["url"])
                        sleep(200)
                elif DEBUG_MODE == True:
                    print("REJECTED DUE TO TIME")
            elif DEBUG_MODE == True:
                print("REJECTED DUE TO TIME")
            while len(previous_links) > 50:
                previous_links.popleft()
        
        if DEBUG_MODE == True:
            sleep(2)

def sp():
    num = random.randint(1, 5)
    if DEBUG_MODE == True:
        print(f"RANDOM_NUMBER_PROMO: {num}")
    if num == 3:
        webbrowser.open("https://www.roblox.com/games/5080477735/Donations-to-Curious-Pengu#!/store")

def join_ps_link(link):
    server_code = link.split(r"LinkCode=")[-1]
    final_link = f"roblox://placeID=15532962292^&linkCode={server_code}"
    subprocess.Popen(["start", final_link], shell=True)
    

if __name__ == "__main__":
    check_for_updates()
    main()
