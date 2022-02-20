import scan

import flask

app = flask.Flask(__name__, static_url_path='/')

@app.route('/')
def home():
    if flask.request.args.get('host'):
        arg = flask.request.args.get
        result = scan.run(arg('host'), arg('port'), arg('threads'), float(arg('timeout'))/1000)
        return flask.render_template('result.html', results=result)

    return flask.render_template('index.html')

app.run(debug=True)