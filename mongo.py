from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'mongotask'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mongotask'

mongo = PyMongo(app)

CORS(app)

@app.route('/api/tasks/<id>', methods=['GET'] )
@app.route('/api/tasks', defaults={'id': '0'},methods=['GET'])
def get_all_tasks(id='0'):
    tasks = mongo.db.tasks
    result = []
    print(id)
    if(id == '0'):
    
        for field in tasks.find():
            result.append({'_id': str(field['_id']), 'title': field['title']})    
    else:
        tasks = mongo.db.tasks #Todo: Find how to get one task by Id
        new_task = tasks.find_one({'_id': ObjectId(id)})
        if(new_task is not None):
            result.append(new_task)
        else:   
            result.append({"message":"Object Not found"})
    
    return jsonify({'result' : result})


@app.route('/api/task', methods=['POST'])
def add_task():
    tasks = mongo.db.tasks 
    title = request.get_json()['title']

    task_id = tasks.insert({'title': title})
    new_task = tasks.find_one({'_id':task_id})

    result = {'title' : new_task['title']}

    return jsonify({'result' : result})

@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    tasks = mongo.db.tasks 
    title = request.get_json()['title']

    tasks.find_one_and_update({'_id':ObjectId(id)}, {"$set": {"title": title}}, upsert=False)
    new_task = tasks.find_one({'_id': ObjectId(id)})

    result = {'title' : new_task['title']}

    return jsonify({"result": result})

@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    tasks = mongo.db.tasks 

    response = tasks.delete_one({'_id': ObjectId(id)})

    if response.deleted_count == 1:
        result = {'message' : 'record deleted'}
    else: 
        result = {'message' : 'no record found'}
    
    return jsonify({'result' : result})

if __name__ == '__main__':
    app.run(debug=True)