from flask import Flask, render_template, request, jsonify,session
import pymysql
import os
import json
import re

db = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
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

@app.route('/mypage', methods=['GET'])
def read_profile():
    # MySQL 데이터베이스에 연결
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='firstclass',
                             charset='utf8mb4')

    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = "SELECT nickname, email, proimg, id FROM information WHERE id = %s;"

            # 예를 들어, URL에서 전달되는 사용자 아이디를 가져오기
            user_id = request.args.get('id')

            # SQL 쿼리 실행
            cursor.execute(sql, (user_id,))

            # 결과 가져오기
            result = cursor.fetchone()

            if result:
                # 프로필 정보를 HTML에 전달하거나 다른 처리를 수행할 수 있음
                return render_template('mypage.html', profile=result)
            else:
                return "해당 사용자의 프로필을 찾을 수 없습니다."
    except Exception as e:
        print(f"에러 발생: {e}")
        return "해당 사용자의 프로필을 찾을 수 없습니다."
    finally:
        # MySQL 연결 종료
        connection.close()

@app.route('/editProfile',methods=['GET'])
def read_editprofile():
    # MySQL 데이터베이스에 연결
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='firstclass',
                             charset='utf8mb4')

    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = "SELECT nickname, email, proimg,id FROM information WHERE id = %s;"

            # 예를 들어, URL에서 전달되는 사용자 아이디를 가져오기
            user_id = request.args.get('id')

            # SQL 쿼리 실행
            cursor.execute(sql, (user_id,))

            # 결과 가져오기
            result = cursor.fetchone()

        if result:
                # 프로필 정보를 HTML에 전달하거나 다른 처리를 수행할 수 있음
            return render_template('editProfile.html', profile=result)
        else:
            return "해당 사용자의 프로필을 찾을 수 없습니다."
    except Exception as e:
        print(f"에러 발생: {e}")
        return "해당 사용자의 프로필을 찾을 수 없습니다."
    finally:
        # MySQL 연결 종료
        connection.close()

@app.route('/editProfile',methods=['PUT'])
def editprofile():
    file = request.files['file']
    data = json.loads(request.form['data'])
    id = data.get("id")
    password = data.get("password")
    nickname = data.get("nickname")
    email = data.get("email")

    def validate_password(password):
        if len(password) < 8:
            return False
        elif re.search('[0-9]',password) is None:
            return False
        elif re.search('[A-Z]',password) is None:
            return False
        elif re.search('[a-z]',password) is None:
            return False
        else:
            return True
    if not validate_password(password):
            return "비밀번호는 8자 이상에 숫자, 소문자, 대문자를 포함해주세요"

    extention = os.path.splitext(file.filename)[1]
    f_name = id + extention
    # 저장할 디렉토리 경로
    upload_folder = 'venv/static/images/'

    # 디렉토리가 없으면 생성
    os.makedirs(upload_folder, exist_ok=True)
    # Windows에서는 별도로 쓰기 권한을 추가해야 함
    try:
        os.chmod(upload_folder, 0o777)
    except Exception as e:
        print(f"Failed to set write permissions: {e}")
    # 파일 저장
    file.save(os.path.join(upload_folder, f_name))

    proimg = '../static/images/'+f_name

    # MySQL 데이터베이스에 연결
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='firstclass',
                             charset='utf8mb4')

    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = "UPDATE information SET pw = %s, nickname = %s, email = %s, proimg = %s WHERE id = %s ;"

            # SQL 쿼리 실행
            cursor.execute(sql, (password,nickname,email,proimg,id))

            # 업데이트는 커밋 필요
            connection.commit()
            output_query = "SELECT * FROM information WHERE id = %s"
            cursor.execute(output_query,(id,))
            output = cursor.fetchall()

            return jsonify(output) ;

    except Exception as e:
        print(f"에러 발생: {e}")
        return "수정 에러"
    finally:
        # MySQL 연결 종료
        connection.close()


def validate_password(password):
    if len(password) < 8:
        return False
    elif re.search('[0-9]',password) is None:
        return False
    elif re.search('[A-Z]',password) is None:
        return False
    elif re.search('[a-z]',password) is None:
        return False
    else:
        return True

def validate_email(email):
    if re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email) is None:
        return False
    else:
        return True

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userInfo = request.form
        id = userInfo['id']
        pw = userInfo['pw']
        nickname = userInfo['nickname']
        email = userInfo['email']
        # proimg = userInfo['proimg']

        # 유효성 검사 실시
        if not validate_email(email):
            return "이메일 형식이 잘못됐습니다"
        if not validate_password(pw):
            return "비밀번호는 8자 이상에 숫자, 소문자, 대문자를 포함해주세요"

        cursor = db.cursor()

        # 사용자가 업로드한 이미지 가져오기
        file = request.files.get('proimg')

        # 이미지를 업로드 하지 않았다면 기본 사진 보여주기
        if file:
            proimg = file.read()
        else:
            with open('/Users/juminkim/Desktop/firstclass/venv/static/default_image.jpg', 'rb') as f:
                proimg = f.read()

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
    app.run('0.0.0.0', port=5000, debug=True)