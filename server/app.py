from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.pop('page_views', None)  # Remove the 'page_views' key from the session
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize the 'page_views' key in the session if it doesn't exist
    session['page_views'] = session.get('page_views', 0)

    # Increment the 'page_views' count for each request
    session['page_views'] += 1

    # Check if the user has viewed more than 3 pages
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Fetch the article data (you need to implement this part)
    article = Article.query.get(id)

    if not article:
        return jsonify({'message': 'Article not found'}), 404  # Handle article not found

    # Serialize the article data
    article_data = {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author': article.author,  # Include author data if needed
    }

    # Return the article data as JSON
    return jsonify(article_data)

if __name__ == '__main__':
    app.run(port=5557)
