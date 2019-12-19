from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # return '<h1> On home page </h1>'
    return render_template('landingpage.html')

@app.route('/random')
def random():
    # return '<h1> On home page </h1>'
    return render_template('random.html')


if __name__ == '__main__':
    app.run(debug=True)
