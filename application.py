from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # return '<h1> On home page </h1>'
    return render_template('landingpage.html')

if __name__ == '__main__':
    app.run(debug=True)
