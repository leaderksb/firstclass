from flask import Flask, jsonify, render_template, request, redirect
import pymysql
from pymysql.cursors import DictCursor

'''
# MySQL 데이터베이스에 연결
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='tokki6013*',
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
    # 자동호출
    connection.close()
''' 

app = Flask(__name__)

# MySQL 데이터베이스에 연결
conn = pymysql.connect(host='localhost',
                            user='root',
                            password='tokki6013*',
                            db='firstclass',
                            charset='utf8mb4')

@app.route('/letterImgSelect', methods=['GET'])
def letterImgSelect():

    return render_template('letterImgSelect.html')

@app.route('/letterWrite', methods=['GET'])
def letterWrite():
    letterImg = request.args.get('letterImg')

    return render_template('letterWrite.html', letterImg=letterImg)

# 상대방에게 첫 복주머니 보내기
@app.route('/letterWriteNew', methods=['POST'])
def letterImgReceive(): ########################################
    global conn

    send_id = request.form['send_id']
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
            cursor.execute(sql, (send_id, 'user1', letterImg, writeTitle, writeContent, 'False'))
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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)