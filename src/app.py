from flask import Flask, render_template, jsonify
import randomcamp
app = Flask(__name__)


@app.route('/getalbum')
def get_album():
    random_album_iframe, album_info = randomcamp.get_random_album() 
    data = { "album_iframe" : random_album_iframe,
             "album_info" : album_info}
    return  jsonify(data)

@app.route('/')
def main_page():
    return render_template("base.html")

if __name__ == '__main__':
          app.run(host="0.0.0.0",debug=True)
