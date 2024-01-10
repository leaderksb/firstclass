from flask import Flask, render_template, request, jsonify, session
import pymysql
import os

# MySQL 데이터베이스에 연결
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='hello123',
                             db='firstclass',
                             charset='utf8mb4')

try:
    with connection.cursor() as cursor:
        # SQL 쿼리 작성
        sql = "desc information"
        # SQL 쿼리 실행
        cursor.execute(sql)
        # 모든 결과 가져오기
        result = cursor.fetchall()
        print(result)
except Exception as e:
    print(f"An error occurred: {e}")


    # with connection.cursor() as cursor:
    #     # SQL 쿼리 작성
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     # SQL 쿼리 실행
    #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # 데이터베이스에 변경 사항 반영
    # connection.commit()
finally:
    # MySQL 연결 종료
    connection.close()

db = pymysql.connect(
    host='localhost',
    user='root',
    password='hello123',
    db='firstclass',
    charset='utf8mb4'
)


app = Flask(__name__)
# 세션 사용에 필요한 SECRET_KEY 설정 
app.secret_key = 'hello123'
# app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userInfo = request.form
        id = userInfo['id']
        pw = userInfo['pw']
        nickname = userInfo['nickname']
        email = userInfo['email']
        proimg = userInfo['proimg']
        
        cursor = db.cursor()
        
        if not (id and pw and nickname and email):
            return '모두 입력해주세요'
        else:
            sql = "SELECT * FROM information WHERE id = %s"
            cursor.execute(sql, (id,))
            account = cursor.fetchone()
            if account:
                return '이미 존재하는 id 입니다'
            
            sql = "SELECT * FROM information WHERE email = %s"
            cursor.execute(sql, (email,))
            account = cursor.fetchone()
            if account:
                return '이미 가입한 이메일입니다'
            
            sql = "INSERT INTO information(id, pw, nickname, email, proimg) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, pw, nickname, email, proimg))
            
            db.commit()
            cursor.close()
            return '회원가입 완료!'
            
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userInfo = request.form
        
        id = userInfo['id']
        pw = userInfo['pw']
        
        cursor = db.cursor()
        
        sql = "SELECT * FROM information WHERE id = %s AND pw = %s"
        cursor.execute(sql, (id, pw))
        accout = cursor.fetchone()
        
        if accout:
            session['logged_in'] = True
            session['id'] = id
            return '로그인 성공!'
        else:
            return 'ID 또는 비밀번호가 일치하지 않습니다'
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    return '로그아웃되었습니다'

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:  # 세션에 로그인 상태 정보가 있는지 확인
        return 'Dashboard - 사용자 ID: ' + session['id']
    else:
        return '로그인이 필요합니다'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)