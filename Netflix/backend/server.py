# ============================================ 
# IMPORTACIONES 
# ============================================ 
from flask import Flask, jsonify, request   # Framework web 
from flask_cors import CORS                 # Cross-Origin Resource Sharing 
import psycopg2                             # Driver de PostgreSQL 
from psycopg2.extras import RealDictCursor  # Retorna resultados como diccionarios 
import os                                   # Variables de entorno 
import socket                               # Obtener hostname del contenedor 
# ============================================ 
# CONFIGURACIÓN DE LA APLICACIÓN 
# ============================================ 
app = Flask(__name__) 
# Habilitar CORS para todas las rutas (permite peticiones desde el frontend) 
CORS(app) 
 
# Configuración de la base de datos desde variables de entorno 
DB_CONFIG = { 
    'host': os.getenv('DB_HOST', 'db-master'),  # Nombre del contenedor de la BD 
    'port': os.getenv('DB_PORT', '5432'),       # Puerto de PostgreSQL 
    'database': os.getenv('DB_NAME', 'netflix_db'), 
    'user': os.getenv('DB_USER', 'postgres'), 
    'password': os.getenv('DB_PASSWORD', 'postgres123') 
} 
 
# Obtener el ID del servidor (nombre del contenedor) 
SERVER_ID = socket.gethostname() 
 
# ============================================ 
# FUNCIÓN: Conexión a la Base de Datos 
# ============================================ 
def get_db_connection(): 
    """ 
    Establece y retorna una conexión a PostgreSQL. 
    RealDictCursor hace que los resultados sean diccionarios en lugar de tuplas. 
    """ 
    try: 
        conn = psycopg2.connect( 
            **DB_CONFIG,  # ** desempaqueta el diccionario como parámetros 
            cursor_factory=RealDictCursor 
        ) 
        return conn 
    except Exception as e: 
        print(f" Error conectando a la base de datos: {e}") 
        return None 
 
# ============================================ 
# ENDPOINT: Health Check 
# ============================================ 
@app.route('/health', methods=['GET']) 
def health_check(): 
    """ 
    Endpoint de salud para que el load balancer verifique 
    que el servidor está funcionando correctamente. 
    """ 
    return jsonify({ 
        'status': 'healthy', 
        'server_id': SERVER_ID, 
        'message': 'Servidor funcionando correctamente' 
    }), 200 
 
# ============================================ 
# ENDPOINT: Obtener todo el contenido 
# ============================================ 
@app.route('/api/content', methods=['GET']) 
def get_content(): 
    """ 
    Obtiene lista de todo el contenido (películas/series). 
    Parámetros opcionales en query string: 
    - genre: filtrar por género 
    - limit: número máximo de resultados (default: 50) 
    """ 
    conn = get_db_connection() 
    if not conn: 
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500 
     
    try: 
        cursor = conn.cursor() 
         
        # Obtener parámetros de la URL 
        genre = request.args.get('genre')  # ?genre=Drama 
        limit = request.args.get('limit', 50)  # ?limit=10 
         
        # Construir query SQL dinámicamente 
        query = "SELECT * FROM content" 
        params = [] 
         
        # Agregar filtro por género si se especifica 
        if genre: 
            query += " WHERE genre = %s" 
            params.append(genre) 
         
        # Agregar ordenamiento y límite 
        query += " ORDER BY created_at DESC LIMIT %s" 
        params.append(limit) 
         
        # Ejecutar la consulta 
        cursor.execute(query, params) 
        content = cursor.fetchall()  # fetchall() obtiene todos los resultados 
         
        # Cerrar cursor y conexión 
        cursor.close() 
        conn.close() 
         
        # Retornar respuesta JSON 
        return jsonify({ 
            'server_id': SERVER_ID,  # Identifica qué servidor respondió 
            'content': content, 
            'count': len(content) 
        }), 200 
         
    except Exception as e: 
        return jsonify({'error': str(e)}), 500 
 
# ============================================ 
# ENDPOINT: Obtener contenido por ID 
# ============================================ 
@app.route('/api/content/<int:content_id>', methods=['GET']) 
def get_content_by_id(content_id): 
    """ 
    Obtiene un contenido específico por su ID. 
    Ejemplo: /api/content/1 
    """ 
    conn = get_db_connection() 
    if not conn: 
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500 
     
    try: 
        cursor = conn.cursor() 
        # %s es un placeholder que previene SQL injection 
        cursor.execute("SELECT * FROM content WHERE id = %s", (content_id,)) 
        content = cursor.fetchone()  # fetchone() obtiene un solo resultado 
         
        cursor.close() 
        conn.close() 
         
        if content: 
            return jsonify({ 
                'server_id': SERVER_ID, 
                'content': content 
            }), 200 
        else: 
            return jsonify({'error': 'Contenido no encontrado'}), 404 
             
    except Exception as e: 
        return jsonify({'error': str(e)}), 500 
 
# ============================================ 
# ENDPOINT: Historial de usuario 
# ============================================ 
@app.route('/api/users/<int:user_id>/history', methods=['GET']) 
def get_user_history(user_id): 
    """ 
    Obtiene el historial de visualización de un usuario. 
    Ejemplo: /api/users/1/history 
    """ 
    conn = get_db_connection() 
    if not conn: 
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500 
     
    try: 
        cursor = conn.cursor() 
        # JOIN combina datos de dos tablas relacionadas 
        query = """ 
            SELECT  
                wh.id, 
                wh.watched_at, 
                wh.progress, 
                c.title, 
                c.thumbnail_url, 
                c.duration, 
                c.genre 
            FROM watch_history wh 
            JOIN content c ON wh.content_id = c.id 
            WHERE wh.user_id = %s 
            ORDER BY wh.watched_at DESC 
        """ 
        cursor.execute(query, (user_id,)) 
        history = cursor.fetchall() 
         
        cursor.close() 
        conn.close() 
         
        return jsonify({ 
            'server_id': SERVER_ID, 
            'history': history, 
            'count': len(history) 
        }), 200 
         
    except Exception as e: 
        return jsonify({'error': str(e)}), 500 
 
# ============================================ 
# ENDPOINT: Registrar visualización 
# ============================================ 
@app.route('/api/watch', methods=['POST']) 
def add_watch_record(): 
    """ 
    Registra que un usuario ha visto un contenido. 
    Body esperado (JSON): 
    { 
        "user_id": 1, 
        "content_id": 2, 
        "progress": 300 
    } 
    """ 
    conn = get_db_connection() 
    if not conn: 
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500 
     
    try: 
        # Obtener datos del body de la petición 
        data = request.get_json() 
        user_id = data.get('user_id') 
        content_id = data.get('content_id') 
        progress = data.get('progress', 0) 
         
        # Validar que existan los datos necesarios 
        if not user_id or not content_id: 
            return jsonify({'error': 'user_id y content_id son requeridos'}), 400 
         
        cursor = conn.cursor() 
        # INSERT agrega un nuevo registro 
        # RETURNING retorna el ID del registro insertado 
        query = """ 
            INSERT INTO watch_history (user_id, content_id, progress) 
            VALUES (%s, %s, %s) 
            RETURNING id 
        """ 
        cursor.execute(query, (user_id, content_id, progress)) 
        new_id = cursor.fetchone()['id'] 
         
        # commit() confirma los cambios en la base de datos 
        conn.commit() 
        cursor.close() 
        conn.close() 
         
        return jsonify({ 
            'server_id': SERVER_ID, 
            'message': 'Registro creado exitosamente', 
            'id': new_id 
        }), 201  # 201 = Created 
         
    except Exception as e: 
        # rollback() deshace cambios si hay error 
        conn.rollback() 
        return jsonify({'error': str(e)}), 500 
 
# ============================================ 
# ENDPOINT: Buscar contenido 
# ============================================ 
@app.route('/api/search', methods=['GET']) 
def search_content(): 
    """ 
    Busca contenido por título o descripción. 
    Parámetro: q (query string) 
    Ejemplo: /api/search?q=stranger 
    """ 
    conn = get_db_connection() 
    if not conn: 
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500 
     
    try: 
        search_term = request.args.get('q', '') 
         
        if not search_term: 
            return jsonify({'error': 'Parámetro de búsqueda "q" es requerido'}), 400 
         
        cursor = conn.cursor() 
        # ILIKE es case-insensitive en PostgreSQL (no distingue mayúsculas/minúsculas) 
        # % es wildcard (comodín) que significa "cualquier texto" 
        query = """ 
            SELECT * FROM content  
            WHERE title ILIKE %s OR description ILIKE %s 
            ORDER BY release_year DESC 
        """ 
        search_pattern = f"%{search_term}%" 
        cursor.execute(query, (search_pattern, search_pattern)) 
        results = cursor.fetchall() 
         
        cursor.close() 
        conn.close() 
         
        return jsonify({ 
            'server_id': SERVER_ID, 
            'results': results, 
            'count': len(results), 
            'search_term': search_term 
        }), 200 
         
    except Exception as e: 
        return jsonify({'error': str(e)}), 500
    
# ============================================ 
# PUNTO DE ENTRADA DE LA APLICACIÓN 
# ============================================ 
if __name__ == '__main__': 
    # host='0.0.0.0' permite conexiones desde cualquier IP 
    # port=5000 es el puerto donde escucha el servidor 
    # debug=False en producción (True muestra errores detallados) 
    app.run(host='0.0.0.0', port=5000, debug=False)