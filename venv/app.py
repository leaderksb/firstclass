from flask import Flask, make_response, render_template, request, jsonify,session,redirect
import pymysql
from pymysql.cursors import DictCursor
import os
import json
import re

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='tokki6013*',
    db='firstclass',
    charset='utf8mb4'
)

app = Flask(__name__)
# 세션 사용에 필요한 SECRET_KEY 설정
app.secret_key = 'hello123'
# app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/sentmessagelist')
def read_sentmessagelist():
    return render_template('sentmessagelist.html')
@app.route('/sentmessage')
def read_sentmessage():
    return render_template('sentmessage.html')

@app.route('/main', methods=['GET', 'POST'])
def read_main():
    print(session.get('id') != None)
    if(session.get('id')!= None) :
        return render_template('main.html')
    else:
        return render_template('login.html')

@app.route('/mainapi', methods=['GET'])
def search():
    global conn

    letterImg = request.args.get('letterImg')

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM nickname, email, id FROM information WHERE id = %s;"

            user_id = request.get_json('id')

            cursor.execute(sql,(user_id,))

            result = cursor.fetchone()

            if result :
                # todo 작성하는 곳으로 이동
                return render_template()
            else:
                return "사용자가 존재하지 않습니다."
    except Exception as e:
        print(f"에러 발생: {e}")
        return "해당 사용자의 프로필을 찾을 수 없습니다."
    #finally:
        # MySQL 연결 종료
        # 자동호출

def CheckLogin(id):
    # if session['logged_in'] == True and session['id'] == id:
    if session.get('logged_in') == True and session.get('id') == id:
        return True
    else:
        return False

from flask import make_response

@app.route('/mypage', methods=['GET'])
def read_profile():
    global conn

    # 세션에서 'id'를 가져오기
    user_id = session.get('id')

    if not user_id:
        return redirect('./login')

    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 작성
            sql = "SELECT nickname, email, proimg, id FROM information WHERE id = %s;"

            # SQL 쿠키 실행
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

# @app.route('/mypage', methods=['GET'])
# def read_profile():
#     global conn
#     # 예를 들어, URL에서 전달되는 사용자 아이디를 가져오기
#     user_id = request.args.get('id')

#     if CheckLogin(user_id) == False:
#         return redirect('./login')

#     try:
#         with conn.cursor() as cursor:
#             # SQL 쿼리 작성
#             sql = "SELECT nickname, email, proimg, id FROM information WHERE id = %s;"

#             # SQL 쿼리 실행
#             cursor.execute(sql, (user_id,))

#             # 결과 가져오기
#             result = cursor.fetchone()

    #         if result:
    #             # 프로필 정보를 HTML에 전달하거나 다른 처리를 수행할 수 있음
    #             return render_template('mypage.html', profile=result)
    #         else:
    #             return "해당 사용자의 프로필을 찾을 수 없습니다."
    # except Exception as e:
    #     print(f"에러 발생: {e}")
    #     return "해당 사용자의 프로필을 찾을 수 없습니다."
    #finally:
        # MySQL 연결 종료
        # 자동호출

@app.route('/editProfile',methods=['GET'])
def read_editprofile():
    global conn
    # 예를 들어, URL에서 전달되는 사용자 아이디를 가져오기
    user_id = request.args.get('id')

    if CheckLogin(user_id) == False:
        return redirect('./login')
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 작성
            sql = "SELECT nickname, email, proimg,id FROM information WHERE id = %s;"

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
    #finally:
        # MySQL 연결 종료
        # 자동호출

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

    global conn

    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 작성
            sql = "UPDATE information SET pw = %s, nickname = %s, email = %s, proimg = %s WHERE id = %s ;"

            # SQL 쿼리 실행
            cursor.execute(sql, (password,nickname,email,proimg,id))

            # 업데이트는 커밋 필요
            conn.commit()
            output_query = "SELECT * FROM information WHERE id = %s"
            cursor.execute(output_query,(id,))
            output = cursor.fetchall()

            return jsonify(output)

    except Exception as e:
        print(f"에러 발생: {e}")
        return "수정 에러"
    #finally:
        # MySQL 연결 종료
        # 자동호출

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
    global conn

    try:
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
            with conn.cursor() as cursor:
                # 사용자가 업로드한 이미지 가져오기
                file = request.files['proimg']
                if file and file.filename != '':
                    extension = os.path.splitext(file.filename)[1]
                    f_name = id + extension
                    # directory 경로
                    upload_folder = 'venv/static/images'
                    # directory 가 없다면 생성
                    os.makedirs(upload_folder, exist_ok=True)
                    # Windows에서는 별도로 쓰기 권한을 추가해야 함
                    try:
                        os.chmod(upload_folder, 0o777)
                    except Exception as e:
                        print(f"Failed to set write permissions: {e}")
                    # 파일 저장
                    file.save(os.path.join(upload_folder, f_name))
                    proimg = '../static/images/'+f_name
                else:
                    proimg = '../static/images/default_image.jpg'
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
                conn.commit()
                return 'signupOK'
    except Exception as e:
        print(f"error occured: {e}")
        return "회원가입 에러"
    #finally:
        # MySQL 연결 종료
        # 자동호출
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global conn

    try:
        if request.method == 'POST':
            userInfo = request.form
            id = userInfo['id']
            pw = userInfo['pw']
            with conn.cursor() as cursor:
                sql = "SELECT * FROM information WHERE id = %s AND pw = %s"
                cursor.execute(sql, (id, pw))
                accout = cursor.fetchone()
                if accout:
                    session['logged_in'] = True
                    session['id'] = id
                    return 'loginOK'
                else:
                    return 'ID 또는 비밀번호가 일치하지 않습니다'
    except Exception as e:
        print(f"error occured: {e}")
        return "로그인 에러"
    #finally:
        # MySQL 연결 종료
        # 자동호출
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    return jsonify({'result': 'success'})

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:  # 세션에 로그인 상태 정보가 있는지 확인
        return 'Dashboard - 사용자 ID: ' + session['id']
    else:
        return '로그인이 필요합니다'

'''
# MySQL 데이터베이스에 연결
conn = pymysql.connect(host='localhost',
            
                             user='root',
                             password='tokki6013*',
                             db='firstclass',
                             charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        # SQL 쿼리 작성
        sql = "desc information"
        # SQL 쿼리 실행
        cursor.execute(sql)
        # 모든 결과 가져오기
        result = cursor.fetchall()
        print(result)
except Exception as e:
    print(f"An error occurred: {e}")

    # with conn.cursor() as cursor:
    #     # SQL 쿼리 작성
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     # SQL 쿼리 실행
    #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # 데이터베이스에 변경 사항 반영
    # conn.commit()
finally:
    # MySQL 연결 종료
    # 자동호출
    conn.close()
'''

# @app.route('/letterImgSelect', methods=['GET'])
# def letterImgSelect():
#     send_id = request.args.get('send_id')
#     receive_id = request.args.get('receive_id')

#     print()
#     print('send_id >', send_id)
#     print('receive_id >', receive_id)
#     print()

#     return render_template('letterImgSelect.html', send_id=send_id, receive_id=receive_id)


@app.route('/letterImgSelect', methods=['GET'])
def letterImgSelect():
    global conn

    send_id = request.args.get('send_id')
    receive_id = request.args.get('receive_id')

    print()
    print('send_id >', send_id)
    print('receive_id >', receive_id)
    print()
    
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # 딕셔너리 타입으로 가져오기
            # send_id 검증
            sql = "select * from information where id = %s;"
            cursor.execute(sql, (send_id,))
            send_data = cursor.fetchone()

            # receive_id 검증
            sql = "select * from information where id = %s;"
            cursor.execute(sql, (receive_id,))
            receive_data = cursor.fetchone()
            
            # send_id와 receive_id가 모두 유효한 경우
            if send_data and receive_data:
                return render_template('letterImgSelect.html', send_id=send_id, receive_id=receive_id)
            else:
                return {"result": "fail"}, 400
    except Exception as e:
        print('Error:', e)
        return {"result": "fail"}, 500

@app.route('/letterWrite', methods=['GET'])
def letterWrite():
    send_id = request.args.get('send_id')
    receive_id = request.args.get('receive_id')
    letterImg = request.args.get('letterImg')

    return render_template('letterWrite.html', send_id=send_id, receive_id=receive_id, letterImg=letterImg)

# 상대방에게 첫 복주머니 보내기
@app.route('/letterWriteNew', methods=['POST'])
def letterImgReceive(): ########################################
    global conn

    send_id = request.form['send_id']
    receive_id = request.form['receive_id']
    letterImg = request.form['letterImg']
    writeTitle = request.form['writeTitle']
    writeContent = request.form['writeContent']

    print('letterImg >', letterImg)
    print('writeTitle >', writeTitle)
    print('writeContent >', writeContent)
    print()

    try:
        with conn.cursor() as cursor:
            sql = "insert into luckybag (send_id, receive_id, letterimg, title, content, readchk) values (%s, %s, %s, %s, %s, %s);"
            # SQL 쿼리 실행
            cursor.execute(sql, (send_id, receive_id, letterImg, writeTitle, writeContent, 'False'))
            # DB에 반영
            conn.commit()
            # MySQL 연결 종료
            # 자동호출
    except Exception as e:
        print('Error:', e)
        return jsonify(result='fail')

    # 성공적으로 DB에 저장한 경우 성공 메시지를 클라이언트에 전달
    return jsonify(result='success')

# 상대방에게 보낸 복주머니 수정
@app.route('/letterWriteRe', methods=['POST'])
def letterWriteRe():
    global conn

    num = request.form['num']
    writeTitle = request.form['writeTitle']
    writeContent = request.form['writeContent']

    print('num >', num)
    print('writeTitle >', writeTitle)
    print('writeContent >', writeContent)
    print()

    try:
        with conn.cursor() as cursor:
            sql = "update luckybag set title = %s, content = %s, letterdate = NOW() WHERE num = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (writeTitle, writeContent, num))
            # DB에 반영
            conn.commit()
            # MySQL 연결 종료
            # 자동호출
    except Exception as e:
        print('Error:', e)
        return jsonify(result='fail')

    # 성공적으로 DB에 저장한 경우 성공 메시지를 클라이언트에 전달
    return jsonify(result='success')

##################################################
# 나에게 온 복주머니 리스트 - 전체
@app.route('/letterReceiveList', methods=['GET'])
def letterReceiveList():
    global conn

    # 만약에 로그인 id가 있으면 그걸 luckybag 테이블에서 receive_id로 검색
    receive_id = 'user1'

    print('receive_id >', receive_id)
    print()

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # 딕셔너리 타입으로 가져오기
            sql = "select * from luckybag where receive_id = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (receive_id,))  # 변환 불가능한 튜플로 받아오는 방법
            data = cursor.fetchall()  # 모든 행을 가져옴
            # 자동호출
            # cursor.close()
            # conn.close()
            return render_template('letterReceiveList.html', data=data)
    except Exception as e:
        print('Error:', e)
        return render_template('letterReceiveList.html')

# 나에게 온 복주머니 - 해당 글
@app.route('/letterReceive/<num>', methods=['GET'])
def letterReceive(num):
    global conn

    # 만약에 로그인 id가 있으면 그걸 luckybag 테이블에서 receive_id로 검색
    receive_id = 'user1'

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # 딕셔너리 타입으로 가져오기
            sql = "select * from luckybag where num = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (num,))  # 변환 불가능한 튜플로 받아오는 방법
            data = cursor.fetchone()  # 해당 행을 가져옴
            # 자동호출
            # cursor.close()
            # conn.close()
            print('record >', data)
            print()
            return render_template('letterReceive.html', record=data)
    except Exception as e:
        print('Error:', e)
        return render_template('letterReceive.html')

# 상대방에게 보낸 복주머니 삭제
@app.route('/letterReceiveDelete', methods=['POST'])
def letterReceiveDelete():
    global conn

    num = request.form['num']

    print('num >', num)
    print()

    try:
        with conn.cursor() as cursor:
            sql = "delete from luckybag WHERE num = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (num,))
            # DB에 반영
            conn.commit()
            # MySQL 연결 종료
            # 자동호출
    except Exception as e:
        print('Error:', e)
        return jsonify(result='fail')

    # 성공적으로 DB에 저장한 경우 성공 메시지를 클라이언트에 전달
    return jsonify(result='success')
##################################################

##################################################
# 내가 보낸 복주머니 리스트 - 전체
@app.route('/letterSendList', methods=['GET'])
def letterSendList():
    global conn

    # 만약에 로그인 id가 있으면 그걸 luckybag 테이블에서 send_id로 검색
    send_id = 'user2'

    print('send_id >', send_id)
    print()

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # 딕셔너리 타입으로 가져오기
            sql = "select * from luckybag where send_id = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (send_id,))  # 변환 불가능한 튜플로 받아오는 방법
            data = cursor.fetchall()  # 모든 행을 가져옴
            # 자동호출
            # cursor.close()
            # conn.close()
            return render_template('letterSendList.html', data=data)
    except Exception as e:
        print('Error:', e)
        return render_template('letterSendList.html')

# 내가 보낸 복주머니 - 해당 글
@app.route('/letterSend/<num>', methods=['GET'])
def letterSend(num):
    global conn

    # 만약에 로그인 id가 있으면 그걸 luckybag 테이블에서 send_id로 검색
    send_id = 'user1'

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # 딕셔너리 타입으로 가져오기
            sql = "select * from luckybag where num = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (num,))  # 변환 불가능한 튜플로 받아오는 방법
            data = cursor.fetchone()  # 해당 행을 가져옴
            # 자동호출
            # cursor.close()
            # conn.close()
            print('record >', data)
            print()
            return render_template('letterSend.html', record=data)
    except Exception as e:
        print('Error:', e)
        return render_template('letterSend.html')

# 내가 받은 복주머니 삭제
@app.route('/letterSendDelete', methods=['POST'])
def letterSendDelete():
    global conn

    num = request.form['num']

    print('num >', num)
    print()

    try:
        with conn.cursor() as cursor:
            sql = "delete from luckybag WHERE num = %s;"
            # SQL 쿼리 실행
            cursor.execute(sql, (num,))
            # DB에 반영
            conn.commit()
            # MySQL 연결 종료
            # 자동호출
    except Exception as e:
        print('Error:', e)
        return jsonify(result='fail')

    # 성공적으로 DB에 저장한 경우 성공 메시지를 클라이언트에 전달
    return jsonify(result='success')
##################################################

# 현재 로그인한 사용자 입장에서 안 읽은 복주머니 개수 반환
@app.route('/luckybagReadFalseCnt', methods=['GET'])
def getLuckybagCount():
    global conn

    receive_id = session.get('id')

    try:
        with conn.cursor() as cursor:
            sql = "select count(*) from luckybag where receive_id = '" + receive_id + "' and readchk = 'False';"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result is not None:
                count = result[0]
            else:
                count = 0

            return jsonify(result='success', count=count)

    except Exception as e:
        print('Error:', e)
        return jsonify(result='fail')
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)