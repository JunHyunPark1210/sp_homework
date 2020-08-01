from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    # 1. 클라이언트로부터 데이터를 받기
    ordname = request.form['name']
    ordcount = request.form['count']
    ordaddr= request.form['addr']
    ordphone = request.form['phone']

    # DB에 삽입할 review 만들기
    order = {'name': ordname, 'count': ordcount, 'addr': ordaddr, 'phone': ordphone}
    # reviews에 review 저장하기
    db.orders.insert_one(order)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    orders = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)