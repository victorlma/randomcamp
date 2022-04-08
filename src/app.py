from flask import Flask, render_template
import randomcamp
app = Flask(__name__)

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def main_page(path):
    random_album_iframe, album_info = randomcamp.get_random_album() 
    return render_template("base.html", iframe = random_album_iframe, info = album_info)

if __name__ == '__main__':
          app.run(host="0.0.0.0",debug=True)
