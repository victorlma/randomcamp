import requests as rq
from random import randint, choice
from bs4 import BeautifulSoup as bs

BASE_URL = "https://bandcamp.com/artist_index?page="
IFRAME_START = '<iframe style="border: 0;" src="https://bandcamp.com/EmbeddedPlayer/v=2/'
IFRAME_END = '/size=large/bgcol=333333/linkcol=ffffff/minimal=true/tracklist=false/transparent=true/" seamless></iframe>'

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
    return ntree, ntree.find("meta", attrs={"property":"og:video:secure_url"})


def get_album_info(tree):
    album_info = ''
    names = tree.find('div', id="name-section")
    about = tree.find('div', class_="tralbumData tralbum-about")
    cred = tree.find('div', class_="tralbumData tralbum-credits")

    if names:
        album_info += str(names)
    if about:
        album_info += str(about)
    if cred:
        album_info += str(cred)

    return album_info

def get_album_iframe_and_info(artist_link):
    tree = bs(rq_txt(artist_link), "lxml")
    
    ntree_album = tree.find("meta", attrs={"property":"og:video:secure_url"})
    ntree = tree
    if ntree_album == None:
        ntree, ntree_album = pick_album(tree, artist_link[:-6])
    
    album_info = get_album_info(ntree)
    album_id = ntree_album.get('content').split('/')[5]
    return IFRAME_START + album_id + IFRAME_END, album_info


        

def get_random_album():
    tree = bs(rq_txt(BASE_URL), "lxml")

    artist_link = pick_artist(tree)

    iframe, info = get_album_iframe_and_info(artist_link)
    return iframe, info

if __name__ == "__main__":
    get_random_album()
