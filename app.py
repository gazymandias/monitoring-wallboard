from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

app = Flask(__name__)

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    task = db.Column(db.String(80), unique=False, nullable=False)
    process = db.Column(db.String(80), unique=False, nullable=True)
    numerator = db.Column(db.Integer, unique=False, nullable=False)
    denominator = db.Column(db.Integer, unique=False, nullable=False)
    started_at = db.Column(db.String(80), unique=False, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, name, status, task, process, numerator, denominator, started_at):
        self.name = name
        self.status = status
        self.task = task
        self.process = process
        self.numerator = numerator
        self.denominator = denominator
        self.started_at = started_at

db.create_all()


@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in db.session.query(Item).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)


@app.route('/items', methods=['POST'])
def create_item():
    body = request.get_json()
    db.session.add(Item(body['name'], body['status'], body['task'], body['process'],
                        body['numerator'], body['denominator'], body['started_at']))
    db.session.commit()
    return "item created"


@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    body = request.get_json()
    db.session.query(Item).filter_by(id=id).update(
        dict(name=body['name'], status=body['status'], task=body['task'], process=body['process'],
             numerator=body['numerator'], denominator=body['denominator'], started_at=body['started_at'],
             updated_at=func.now()))
    db.session.commit()
    return "item updated"


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(Item).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"


@app.route('/home')
def wallboard_home():
    try:
        import collections
        items = []
        for item in db.session.query(Item).all():
            del item.__dict__['_sa_instance_state']
            items.append(item.__dict__)
        my_lists = collections.defaultdict(list)
        for item in items:
            my_lists["robot"].append(item["name"])
            my_lists["status"].append(item["status"])
            my_lists["task"].append(item["task"])
            my_lists["process"].append(item["process"])
            my_lists["numerator"].append(item["numerator"])
            my_lists["denominator"].append(item["denominator"])
            my_lists["progress"].append(round(item["numerator"] / item["denominator"] * 100, 2))
            my_lists["started_at"].append(item["started_at"])
            my_lists["updated_at"].append(item["updated_at"].strftime("%H:%M:%S"))
        item_count = max(item["id"] for item in items)
        return render_template('wallboard.html', item_count=item_count, robots=my_lists["robot"],
                               status=my_lists["status"], task=my_lists["task"], process=my_lists["process"],
                               progress=my_lists["progress"], numerator=my_lists["numerator"],
                               denominator=my_lists["denominator"], start=my_lists["started_at"],
                               updated_at=my_lists["updated_at"])
    except Exception:
        return render_template('error.html')
