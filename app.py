#------------------------------------------------------------------------------#
# Imports
#------------------------------------------------------------------------------#
from flask import Flask, render_template, jsonify, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
import string
import random
import datetime
import pprint


#------------------------------------------------------------------------------#
# App Config.
#------------------------------------------------------------------------------#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



#------------------------------------------------------------------------------#
# Snippet Model
#------------------------------------------------------------------------------#
class Snippet(db.Model):
    #__tablename__ = 'Snippets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(100000))
    key = db.Column(db.String(10))
    lang = db.Column(db.String(120))
    expires = db.Column(db.DateTime())
    
    def __init__(self, title, content, lang):

        key = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        expires = datetime.datetime.now()

        self.title = title
        self.content = content
        self.lang = lang
        self.key = key
        self.expires = expires

    def __repr__(self):
        return '<Snippet %r>' % self.title



#------------------------------------------------------------------------------#
# Routes
#------------------------------------------------------------------------------#
@app.route('/')
def home():
    return render_template('pages/create.html')

@app.route('/terms')
def terms():
    return 'Terms page'

@app.route('/about')
def about():
    return 'About page'

@app.route('/snippets/<int:snippet_id>', methods=['GET'])
def show_snippet(snippet_id):
    snippet = Snippet.query.get(snippet_id)
    pprint.pprint(Snippet.query.filter(id == snippet_id).first())
    if snippet is None:
        abort(404)

    return render_template('pages/view-snippet.html', snippet=snippet)

@app.route('/<string:key>', methods=['GET'])
def show_snippet_for_key(key):
    snippet = Snippet.query.filter_by(key=key).first()
    if snippet is None:
        abort(404)

    return render_template('pages/view.html', snippet=snippet)

@app.route('/api/v1.0/snippets/<int:snippet_id>', methods=['GET'])
def get_snippet(snippet_id):
    snippet = [snippet for snippet in snippets if snippet['id'] == snippet_id]
    if len(snippet) == 0:
        abort(404)
    return jsonify({'snippet': snippet[0]})

@app.route('/api/v1.0/snippets', methods=['POST'])
def create_snippet():
    if not request.json or not 'title' in request.json:
        abort(400)

    # snippets.append(snippet)
    snippet = Snippet(request.json['title'], request.json.get('content', ""), request.json.get('lang', ""))
    db.session.add(snippet)
    db.session.commit()
    return jsonify({'key': snippet.key, 'lang': snippet.lang}), 201



#----------------------------------------------------------------------------#
# App Start
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.debug = True
    app.run()