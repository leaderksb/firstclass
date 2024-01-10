from flask import Flask, render_template, request, jsonify
import pymysql
import os
import json
import re

app = Flask(__name__)

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
        
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)