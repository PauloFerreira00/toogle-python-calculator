from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "db.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)


# Toogle model
class Toogle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    toogle = db.Column(db.String(100), unique=True)

    def __init__(self, toogle):
        self.toogle = toogle


# Toogle schema
class ToogleSchema(Schema):
    id = fields.Int()
    toogle = fields.Str()


# Init schema
toogle_schema = ToogleSchema()


# Create toogle
@app.route('/toogles', methods=['POST'])
def add():
    toogle = request.json['toogle']

    new_toogle = Toogle(toogle)
    db.session.add(new_toogle)
    db.session.commit()

    return toogle_schema.dump(new_toogle)


@app.route('/toogles/<id>', methods=['DELETE'])
def delete(id):
    toogle = Toogle.query.get(id)
    db.session.delete(toogle)
    db.session.commit()

    return toogle_schema.dump(toogle)


@app.route('/toogles', methods=['GET'])
def all():
    toogle_schema = ToogleSchema(many=True)

    toogles = Toogle.query.all()
    result = toogle_schema.dump(toogles)
    print(result)
    return jsonify(result)


# Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
