from flask import Flask, render_template, jsonify, request, redirect
import pymysql

app = Flask(__name__)

def initialize_table():
    conn = make_handle()
    try:
        with conn.cursor() as cursor:
            create_post_table_query = """
                    CREATE TABLE IF NOT EXISTS POST(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255),
                        writer VARCHAR(255),
                        content TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
            
            create_user_table_query = """
                
            """
                
            cursor.execute(create_post_table_query)
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
            cursor = conn.cursor()
            
            query =  """
                SELECT 
                    id, 
                    title, 
                    writer, 
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
    
    try:
        with conn.cursor() as cursor:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO 
                    POST(title, writer, content)
                VALUES('{data['title']}', '{data['writer']}', '{data['content']}');
            """

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
            cursor = conn.cursor()
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
            cursor = conn.cursor()
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
            cursor = conn.cursor()
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
            cursor = conn.cursor()
            query = f"""
                DELETE FROM post
                WHERE id = {id}
            """

            cursor.execute(query)
            conn.commit()
        return "success"
    except:
        return "error"


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
            cursor = conn.cursor()
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

@app.route('/join')
def join():
    return render_template('join.html')

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