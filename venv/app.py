from flask import Flask, render_template, request, jsonify
import pymysql

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


@app.route('/login')
def login():
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    
    return render_template('logout.html')

# @app.route('/memo', methods=['POST'])
# def post_article():
#     # 1. 클라이언트로부터 데이터를 받기
#    url_receive = request.form['url_give']
#    comment_receive = request.form['comment_give']

#    # 2. meta tag를 스크래핑하기
#    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#    data = requests.get(url_receive, headers=headers)
#    soup = BeautifulSoup(data.text, 'html.parser')
#    print(soup)  # HTML을 받아온 것을 확인할 수 있다.
   
#    og_image = soup.select_one('meta[property="og:image"]')
#    og_title = soup.select_one('meta[property="og:title"]')
#    og_description = soup.select_one('meta[property="og:description"]')

#    url_title = og_title['content']
#    url_description = og_description['content']
#    url_image = og_image['content']

#    article = {'url': url_receive, 'title': url_title, 'desc': url_description, 'image': url_image, 'comment': comment_receive}

#    # 3. mongoDB에 데이터를 넣기
#    db.articles.insert_one(article)

#    return jsonify({'result': 'success'})

# @app.route('/memo', methods=['GET'])
# def read_articles():
#     # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
#     result = list(db.articles.find({}, {'_id': 0}))
#     return jsonify({'result': 'success', 'articles': result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)