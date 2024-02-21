from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)

def initialize_table():
    conn = make_handle()
    try:
        with conn.cursor() as cursor:
            create_table_query = """
                    CREATE TABLE IF NOT EXISTS POST(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255),
                        writer VARCHAR(255),
                        content TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """
            cursor.execute(create_table_query)
    except Exception as e:
        print(f"Error : {e}")

def make_handle():
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'asd123',
        db = 'web_db',
    )
    
    return conn


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
                    DATE_FORMAT(updated_at, '%Y-%m-%d') as date
                FROM
                    post
                ORDER BY updated_at DESC;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            return render_template('index.html', posts=result)
    
    except Exception as e:
        print(f"Error: {e}")
    
    return 'Hello, World!'


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
                INSERT INTO POST(title, writer, content)
                VALUES('%s', '%s', '%s');
            """ % (data['title'], data['writer'], data['content'])

            cursor.execute(query)
            conn.commit()
            
            return "success"        
    
    except Exception as e:
        print(f"Error: {e}")
        return "error"

if __name__ == '__main__':
    initialize_table()
    app.run()