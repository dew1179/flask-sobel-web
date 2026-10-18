from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'potato123secret'
# 本地sqlite数据库，无需安装MySQL，开箱即用
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///potato.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 上传图片保存路径
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)


# 数据库模型：土豆生长数据表
class PotatoRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.String(30))
    temperature = db.Column(db.Float)
    height = db.Column(db.Float)
    remark = db.Column(db.String(200))
    img_name = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)


# 首页路由
@app.route('/')
def index():
    records = PotatoRecord.query.all()
    return render_template('potato.html', records=records)


# 提交数据+上传图片接口
@app.route('/add', methods=['POST'])
def add_record():
    date = request.form.get('record_date')
    temp = request.form.get('temperature')
    height = request.form.get('height')
    remark = request.form.get('remark')
    file = request.files['img']

    img_filename = None
    if file and file.filename != '':
        img_filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))

    new_data = PotatoRecord(
        record_date=date,
        temperature=float(temp),
        height=float(height),
        remark=remark,
        img_name=img_filename
    )
    db.session.add(new_data)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 自动生成数据库文件
    app.run(debug=True)
