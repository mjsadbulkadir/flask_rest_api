from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from dotenv import find_dotenvs


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    author = db.Column(db.String(50))
    
    def __init__(self,title,description, author):
        self.title = title
        self.description = description
        self.author = author
        
class PostSchema(ma.Schema):
    class Meta:
        fields = ("title", "author", "description")
        
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
    
@app.route('/post', methods = ['POST'])
def add_post():
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']

    my_post = Post(title, description,author)
    db.session.add(my_post)
    db.session.commit()

    return post_schema.jsonify(my_post)

@app.route('/get', methods = ['GET'])
def get_post():
 all_posts = Post.query.all()
 result = posts_schema.dump(all_posts)
 
 return jsonify(result)

@app.route('/post_details/<id>/', methods = ['GET'])
def post_details(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)


@app.route('/post_updates/<id>/', methods = ['PUT'])
def post_update(id):
    post = Post.query.get(id)
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    
    post.title = title
    post.description = description
    post.author = author
    
    # db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post)
    
    # return post_schema.jsonify(post)

@app.route('/post_delete/<id>/', methods = ['DELETE'])
def post_delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    # print(post)
    return post_schema.jsonify(post)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
     app.run(debug=True ,port=8000,use_reloader=False)
    