# Flask_Elice

## 설치 및 실행

**1. 의존성 다운**

```bash
pip3 install -r requirements.txt # virtualenv 사용 권장
```

**2. DB 및 기본 설정**

- app/constants.py 수정 (db 설정에 맞춰 변경)
- app/__init__.py 수정 (app.config['SERVER_NAME'] 및 app.config['DEBUG'] 변경)
- 다음 명령어 입력

```bash
python3 manage.py db init
python3 manage.py db migrate
```

**3. 서버 실행**

```bash
python3 manage.py run
```


## API 명세

### 회원 관련 API

### `POST` signup

```html
POST /user/signup
```

- Request Example

```json
{
    "fullname": "Kim Byeong Cheol",
    "email": "klm03025@gmail.com",
    "password": "test1234"
}
```

- Response
    - 200: Signup Success
    - 409: Signup Failed
    - 500: Internal Server Error.

### `POST` login

```json
POST /user/login
```

- Request Example

```json
{
    "email": "klm03025@gmail.com",
    "password": "test1234"
}
```

- Response
    - 200: Login Success
    - 404: User Not Found
    - 409: Login Failed
    - 500: Internal Server Error

### `GET` logout

```json
GET /user/logout
```

- Response
    - 200: Login Success
    - 404: Not Logged in
    - 500: Internal Server Error

### `GET` info

```json
GET /user/info
```

- Response
    - 200: Success
    - 500: Internal Server Error

```json
{
    "status": "Loggedin",
    "fullname": "Kim Byeong Cheol",
    "email": "klm03025@gmail.com"
}
```

-----------------------------------


### 게시판 관련 API

### `POST` create

```json
POST /board/create
```

- Request Example

```json
{
	"name" : "자유게시판"
}
```

- 로그인이 선행 되어야 함.
- Response
    - 200: Success
    - 404: User Not Found
    - 409: Created Failed
    - 500: Internal Server Error

### `GET` read

```json
GET /board/{board_name}
```

- Response
    - 200: Success
    - 404: Board Not Found
    - 500: Internal Server Error

```json
{
    "message" : "Read Success",
    "name" : "자유게시판",
    "article" : [
			...
    ]
}
```

### `DELETE` delete

```json
DELETE /board/{board_name}/delete
```

- 로그인이 선행되어야 하며, 본인이 만든 게시판만 삭제할 수 있음.
- 게시판에 글이 1개 이상 존재할 경우 삭제할 수 없음.
- Response:
    - 200: Success
    - 404: Board Not Found
    - 409: Not Enough Permission, Board Has Articles
    - 500: Internal Server Error

### `POST` update

```json
POST /board/{board_name}/update
```

- Request Example

```json
{
    "name": "비밀게시판"
}
```

- 로그인이 선행되어야 하며, 본인이 만든 게시판만 수정할 수 있음.
- Response:
    - 200: Success
    - 404: Board Not Found
    - 409: Not Enough Permission
    - 500: Internal Server Error


------------------------------------


### 게시물 관련 정보

### `POST` create

```json
POST /board/{board_name}/create
```

- Request Example

```json
{
    "title": "배가 고파요",
    "content": "말 나온 겸 오늘 야식이나 시켜먹으려고 하는데, 뭘 시켜야 잘 시켰다고 소문이 날까요?"
}
```

- 로그인이 선행되어야 함.
- Response:
    - 200: Success
    - 404: Board Not Found
    - 409: Not Enough Permission
    - 500: Internal Server Error

### `GET` read

```json
GET /board/{board_name}/{article_id}
```

- Response:
    - 200: Success
    - 404: Article Not Found
    - 500: Internal Server Error

### `DELETE` delete

```json
DELETE /board/{board_name}/{article_id}/delete
```

- 로그인이 선행되어야 하며, 본인의 글이 아니면 삭제할 수 없음.
- Response:
    - 200: Success
    - 404: Article Not Found
    - 409: Not Enough Permission
    - 500: Internal Server Error

### `POST` update

```json
POST /board/{board_name}/{article_id}/update
```

- 로그인이 선행되어야 하며, 본인의 글이 아니면 수정할 수 없음.
- Response:
    - 200: Success
    - 404: Article Not Found
    - 409: Not Enough Permission
    - 500: Internal Server Error
