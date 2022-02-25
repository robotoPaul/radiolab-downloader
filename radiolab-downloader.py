import requests
import bs4
import os

url_main = "https://www.wnycstudios.org"
url_episodes = "podcasts/radiolab/podcasts"     # Use podcasts/radiolab/radio-shows for only the radio shows

empty_kill_threshold = 10                       # How many pages with no episodes have to occur before stopping the program

start_page = 1
end_page = 1000

title_has_to_include = []                       # Only download episodes that contain any of these strings         example: ["bilbo","hobbyte"]
title_does_not_contain = []                     # Exclude episodes that contain any of these strings              example: ["gandalf","gray"]

path = "B:\Radiolab"                            # example: C:\Music\Radiolab

def get_url_content(url):
    return requests.get(url).text

def get_episode_urls(url_main, url_episodes):
    content = get_url_content(url_main + "/" + url_episodes)
    soup = bs4.BeautifulSoup(content, "html.parser")
    urls = []
    for episode in soup.findAll('h1', {'class': 'episode-tease__title'}):
        title = episode.find('a').text
        rel_url = episode.find('a').get('href')
        abs_url = url_main + rel_url
        urls.append((title,abs_url))
    return urls

def download_episode(episode):
    title = episode[0]
    url = episode[1]
    content = get_url_content(url)
    soup = bs4.BeautifulSoup(content, "html.parser")
    download_object = soup.find('a', {'class': 'download-link'})
    if(download_object != None):
        download_url = download_object.get('href')
        file = requests.get(download_url)
        if(path == ""):
            open(title + ".mp3", 'wb').write(file.content)
        else:
            open(path + "\\" + title + ".mp3", 'wb').write(file.content)
    return

def check_existing_episode(title):
    if(path == ""):
        return os.path.exists(os.getcwd() + '\\' + title + ".mp3")
    else:
        print(path + '\\' + title + ".mp3")
        return os.path.exists(path + '\\' + title + ".mp3")

def main():
    episodes = []
    empty_pages = 0
    

    for i in range(start_page, end_page):
        skip = False
        print("Page " + str(i))
        episodes = get_episode_urls(url_main, url_episodes + "/" + str(i))

        if(episodes == []):
            empty_pages += 1

        if(empty_kill_threshold<=empty_pages):
            print("Empty pages threshold reached")
            break

        for episode in episodes:
            title = episode[0]
            for string in title_has_to_include:
                if string not in title:
                    skip = True
                else:
                    print(string+"    "+title)
            for string in title_does_not_contain:
                if string in title:
                    skip = True
            
            if(skip):
                continue

            if(check_existing_episode(title)):
                print("Skipping existing episode " + title)
                continue

            print("Downloading episode '" + title + "'")
            try:
                download_episode(episode)
                print("Successfully downloaded episode '" + title + "'")
            except Exception:
                print("Couldn't download episode '" + title + "'")
    print("Finished Downloading!")



        
    
if __name__ == "__main__":
    main()
