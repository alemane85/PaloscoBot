from flask import Flask,render_template
import webbrowser

app = Flask(__name__)
url="http://127.0.0.1:5000/backend"
webbrowser.open(url,new=2)
# Defining the home page of our site
@app.route("/backend")  # this sets the route to this page
def home():
	return render_template("base.html")

if __name__ == "__main__":
    app.run()
