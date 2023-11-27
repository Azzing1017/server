from flask import Flask # flask.py 안에 Flask class 로드
from flask import request # 요청 관련 클래스 ~
from flask import render_template # html 로드하는 클래스 ~
from werkzeug.utils import secure_filename # 파일이름, 경로에 대한 기본적인 보안

# flask server 보안 규칙
# 1. html 문서들은 render_template으로 로드 시
# 반드시 templates 폴더 내에 존재해야 한다
# 2. 모든 경로에 대해 접근 불가
# 단, static 경로만 접근 가능

import os

# static/imgs 폴더가 없으면 만들어라
if not os.path.exists('static/imgs'):
    os.makedirs('static/imgs')

# 내장 변수 생성자 __name__ 를 매개변수로 Flask class를 생성
# 생성된 인스턴스를 app에 저장!
app = Flask(__name__)

@ app.route('/') # Ipv4:port + '/' 경로에 접속 시 호출되는 함수 정의!! 
def index(): # 하나의 경로에는 하나의 함수가 반드시 있어야한다!
    # return 쓸 수있는 결과는, 타입은 html
    # 1. 태그를 직접
    # 2. 라이브러리 활용 render_template 이용
    
    # return '<h1>건중스 페이지</h1>'
    return '''
        <style>
            form{
             transform: scale(4);
             transform-origin: top left;
              }
        </style>
        <form action="/detect" method="post" enctype="multipart/form-data" >
            <input type="file" name="file"></br>
            <input type="submit" name="전송">
        </form>
        '''

@ app.route('/detect', methods=['GET','POST']) # root 경로에서 넣어 온 이미지를 받아오는 페이지
def detect():
    ## request 관련 페이지들은
    # route 설정 시 반드시 전송방식을 정의해야 한다.
    # 받아오는 코드

    # GET -> request.args['Key값']
    # POST -> request.form['Key값']
    # file -> requiest.files['Key값']

    f = request.files['file']
    filename = secure_filename(f.filename)
    img_path = 'static/imgs/' + filename
    f.save(img_path) # 들여쓰기 한칸 되있으니까 자동완성안되네?

    i = ImageDetect() # 꼭 대문자로 시작해서 class 소문자면 함수
    result = i.detect_img(img_path)
    cnf = result[0][4]
    nc = result[0][5]
    label = i.data[nc]
    output = '<h1>{}일 확률이 {:.2f}%입니다.</h1>'.format(label, cnf*100) # {:.2f} 소수점 2번째자리까지 출력
    
    # return '전송 선공!!'
    return output

    # file관련 경로, 이름들은 보안을 지켜주자
    # file 같은 경우는 경로들이 다보이기에 다른 것들 경로를 숨겨주기 위해 라이브러리 로드

# 내가 직접 실행(run)시 내장 변수 __name__이 __main__으로 변한다.
if __name__ == '__main__':
    # app.run()
    # app.run() 안에 들어갈 수 잇는게 여러가지 있다.
    # app.run(host = '127.0.0.0', ) 
    # app.run(host = '211.228.36.254', )  # 내 ip로하면 접근할 수 있는 컴퓨터가있으면 막접속가능
    # app.run(host = 'localhost', ) # 이렇게하면 나만 접근가능
    app.run(port=5033) # flask는 왠만하면 5000번대