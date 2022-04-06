import requests as rq
from random import randint, choice
from bs4 import BeautifulSoup as bs

BASE_URL = "https://bandcamp.com/artist_index?page="
IFRAME_START = '<iframe style="border: 0; width: 350px; height: 670px;" src="https://bandcamp.com/EmbeddedPlayer/v=2/'
IFRAME_END = '/size=large/bgcol=333333/linkcol=ffffff/tracklist=true/transparent=true/" seamless></iframe>'

def rq_txt(url):
    return rq.get(url).text


def has_data_item_id(tag):
    return tag.has_attr('data-item-id')

def get_max_page(tree):
    return tree.find_all('a', class_="pagenum round4")[-1].text

def pick_artist(tree):
    max_page = get_max_page(tree)
    random_page = randint(1, int(max_page))

    if random_page != 1:
        tree = bs(rq_txt(BASE_URL+str(random_page)), "lxml")

    artist = choice(tree.find('ul', class_="item_list").contents)
    artist_link = artist.a.get('href')
    return artist_link+"/music"

def pick_album(tree, artist_link):
    album = choice(tree.find_all(has_data_item_id))
    album_link = album.a.get("href")
    if album_link[0] != "h":
        album_link = artist_link + album_link
    ntree = bs(rq_txt(album_link), "lxml")
    return ntree.find("meta", attrs={"property":"og:video:secure_url"})


def get_album_iframe(artist_link):
    tree = bs(rq_txt(artist_link), "lxml")
    
    ntree = tree.find("meta", attrs={"property":"og:video:secure_url"})
    if ntree == None:
        ntree = pick_album(tree, artist_link[:-6])
    album_id = ntree.get('content').split('/')[5]
    return IFRAME_START + album_id + IFRAME_END


        

def get_random_album():
    tree = bs(rq_txt(BASE_URL), "lxml")

    artist_link = pick_artist(tree)

    iframe = get_album_iframe(artist_link)
    print(iframe)
if __name__ == "__main__":
    get_random_album()
