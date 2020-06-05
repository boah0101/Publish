from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# HTML을 주는 부분


@app.route('/')
def home():
    return render_template('Boah_Shoppingmall.html')

# API 역할을 하는 부분


@app.route('/post', methods=['POST'])
def write_order_info():
    name_receive = request.form['name_give']
    qty_receive = request.form['qty_give']
    add_receive = request.form['add_give']
    phone_receive = request.form['phone_give']

    order_info = {
        'name': name_receive,
        'qty': qty_receive,
        'add': add_receive,
        'phone': phone_receive
    }
    db.order_info_list.insert_one(order_info)

    return jsonify({'result': 'success', 'msg': 'POST됨'})


@app.route('/get', methods=['GET'])
def read_order_info():
    order_info_list = list(db.order_info_list.find({}, {'_id': 0}))

    return jsonify({'result': 'success', 'msg': list(db.order_info_list.find({}, {'_id': 0}))})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
