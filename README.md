# RandomCamp


Come and get a random Bandcamp album!


![Preview](https://user-images.githubusercontent.com/100252586/162129060-3f19be39-1d5b-4866-85fb-816b0c18b7e7.png)

## How It Works?

It uses BeautifulSoup to do the scrapping in the Bandcamp Artist Index,
pulling a random artist from it.
The script then gets a random album from the artist along with some info
about it. 

Finally it displays both the embedded album and the info in a web template
renderer with Flask.
