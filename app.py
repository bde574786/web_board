from flask import Flask, render_template, jsonify, request, redirect, session, url_for
import pymysql

app = Flask(__name__)
app.secret_key = '1234'

def initialize_table():
    conn = make_handle()
    try:
        with conn.cursor() as cursor:
            create_post_table_query = """
                    CREATE TABLE IF NOT EXISTS POST(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) not null,
                        writer VARCHAR(255) not null,
                        content TEXT not null,
                        secret_key varchar(255),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
            
            create_user_table_query = """
                    CREATE TABLE IF NOT EXISTS USER(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id varchar(255) not null,
                        username varchar(255) not null,
                        phone_number varchar(255) not null,
                        password varchar(255) not null,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
            """
                
            cursor.execute(create_post_table_query)
            cursor.execute(create_user_table_query)
    except:
        return "error"

def make_handle():
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'asd123',
        db = 'web_db',
    )
    
    return conn

@app.route('/')
def index_redirect():
    return redirect('/index')


@app.route('/index')
def index():
    conn = make_handle()
    try:
        with conn.cursor() as cursor:
            query =  """
                SELECT 
                    id, 
                    title, 
                    writer,
                    secret_key,
                    DATE_FORMAT(created_at, '%Y-%m-%d')
                FROM
                    post
                ORDER BY created_at DESC
            """
            
            
            cursor.execute(query)
            result = cursor.fetchall()
            
            return render_template('index.html', posts=result)
    
    except:
        return "error"


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/write_post', methods=["POST"])
def write_post():
    data = request.json
    conn = make_handle()
    
    title = data['title']
    writer = data['writer']
    secret_key = data['secretKey']
    content = data['content']
    
    if(secret_key):
        query = f"""
                INSERT INTO 
                    POST(title, writer, secret_key, content)
                VALUES('{title}', '{writer}', '{secret_key}', '{content}');
            """
    else:
        query = f"""
                INSERT INTO 
                    POST(title, writer, content)
                VALUES('{title}', '{writer}', '{content}');
            """
    
    print(query)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            return "success"        
    
    except:
        return "error"


@app.route('/view_post/<int:id>')
def view_post(id):
    conn = make_handle()
    
    try:
        with conn.cursor() as cursor:
            query = f"""
                SELECT 
                    id, 
                    title, 
                    writer, 
                    content, 
                    DATE_FORMAT(created_at, '%Y-%m-%d')
                FROM post
                WHERE id = {id}
            """
            
            cursor.execute(query)
            result = cursor.fetchone()

        return render_template('view.html', post=result)

    except:
        return "error"


@app.route('/get_post_data/<int:id>')
def get_post_data(id):
    conn = make_handle()
    
    try:
        with conn.cursor() as cursor:
            query = f"""
                SELECT
                    id,
                    title,
                    writer,
                    content
                FROM post
                WHERE id={id}
            """
            
            cursor.execute(query)
            result = cursor.fetchone()

        return render_template('edit.html', post=result)
            
    except:
        pass


@app.route('/edit_post/<int:id>', methods=['POST'])
def edit_post(id):
    data = request.json
    conn = make_handle()
    
    try:
        with conn.cursor() as cursor:
            query = f"""
                UPDATE post
                SET title ='{data['title']}', writer = '{data['writer']}', content = '{data['content']}'
                WHERE id = {id}
            """
            
            cursor.execute(query)
            conn.commit()
            
        return "success"
    except:
        return "error"


@app.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    conn = make_handle()
    
    try:
        with conn.cursor() as cursor:
            query = f"""
                DELETE FROM post
                WHERE id = {id}
            """

            cursor.execute(query)
            conn.commit()
        return "success"
    except:
        return "error"

@app.route('/verify_post', methods=['POST'])
def verify_post():
    conn = make_handle()
    data = request.json
    id = data['id']
    secret_key = data['secretKey']
    
    try:
        with conn.cursor() as cursor:
            query = f"""
                SELECT id, secret_key
                FROM post
                WHERE id = '{id}' and secret_key = '{secret_key}'
            """
            cursor.execute(query)
            if(cursor.fetchone()):
                return "success"
            else:
                return "error"
    except Exception as e:
        print(e)

@app.route('/search', methods=['GET'])
def search_data():
    conn = make_handle()
    
    option = request.args.get('option')
    user_input = request.args.get('userInput')
    
    query = """
                SELECT 
                    id
                FROM
                    post 
            """
    
    try:
        with conn.cursor() as cursor:
            if option == 'all':
                query += f"WHERE title LIKE '%{user_input}%' OR content LIKE '%{user_input}%'"
            elif option == 'title':
                query += f"WHERE title LIKE '%{user_input}%'"
            elif option == 'content':
                query += f"WHERE content LIKE '%{user_input}%'"
        
            cursor.execute(query)
            result = cursor.fetchall()

        return jsonify(result)
    except:
        return "error"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user_login', methods=['POST'])
def user_login():
    conn = make_handle()
    data = request.json
    
    user_id = data['userId']
    password = data['password']
    
    query = f"""
        SELECT user_id, password
        FROM user
        WHERE user_id = '{user_id}' AND password = '{password}'
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            if(cursor.fetchone()):
                session['user_id'] = user_id
                return 'success'
            else:
                return 'error'
    except Exception as e:
        print(e)
        return 'error'


@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    conn = make_handle()
    data = request.json
    
    user_id = data['userId']
    username = data['username']
    phone_number = data['phoneNumber']
    password = data['password']
    
    query = f"""
        INSERT INTO user(user_id, username, phone_number, password)
        values('{user_id}', '{username}', '{phone_number}', '{password}')
    """
    
    user_id_check_query = f"""
        SELECT user_id
        FROM user
        WHERE user_id = '{user_id}'
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(user_id_check_query)
            if(cursor.fetchone()):
                return 'duplicate_id'
            else:
                cursor.execute(query)
                conn.commit()
                return 'success'
            
    except:
        return 'error'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/find_id')
def find_id():
    return render_template('find_id.html')

@app.route('/get_id', methods=['POST'])
def get_id():
    data = request.json
    name = data['name']
    phone_number = data['phoneNumber']
    
    conn = make_handle()
    
    query = f"""
        SELECT user_id
        FROM USER
        WHERE username = '{name}' and phone_number = '{phone_number}'
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return jsonify(result)
    except Exception as e:
        print(e)
        pass
    
    return "success"


@app.route('/find_password')
def find_password():
    return render_template('find_password.html')


@app.route('/get_password', methods=['POST'])
def get_password():
    data = request.json
    user_id = data['id']
    name = data['name']
    phone_number = data['phoneNumber']
    
    conn = make_handle()
    
    query = f"""
        SELECT password
        FROM USER
        WHERE user_id = '{user_id}' and username = '{name}' and phone_number = '{phone_number}'
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return jsonify(result)
    except Exception as e:
        print(e)
        pass
    
    return "success"

@app.errorhandler(400)
def error_400(e):
    return render_template('error_400.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('error_404.html')

@app.errorhandler(500)
def error_500(e):
    return render_template('error_500.html')


if __name__ == '__main__':
    initialize_table()
    app.run()