#-*- coding:utf-8 -*_
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# docker-compose.yml 파일에 따라 Dockerfile build 후 생성된 컨테이너에서 os.envrion() 함수로 mongodb에 설정된 ip주소를 확인
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

@app.route('/')
def todo():
	_items = db.tododb.find()
	items = [item for item in _items]
	return render_template('todo.html', items=items)
   
# templeates/todo.html 파일에서 form에 입력 시 new() 메소드 실행 
@app.route('/new',methods=['POST'])
def new():
	item_doc = {
		'name': request.form['name'],
		'description': request.form['description']
	}
# item_doc dictionary를 mongodb에 insert
	db.tododb.insert_one(item_doc)
# redirect로 재전송
# url_for() 메소드로 todo() method를 실행    
        return redirect(url_for('todo'))

if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)


