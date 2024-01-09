from flask import Flask, render_template, request, jsonify
import pymysql

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

@app.route('/editProfile',methods=['POST'])
def editprofile():
    print(request.get_json("data"))
    return request.get_json("data")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)