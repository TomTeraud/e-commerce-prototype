import os
class Config():
    
    """Configuration class for Flask application."""
    BUCKET_NAME = os.environ.get('GOOGLE_STORAGE_BUCKET')    
    THUMBNAIL_BUCKET_NAME = os.environ.get('THUMBNAIL_BUCKET_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SELECTED_PRECE_ID = 0
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])
    
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'

    POSTS_PER_PAGE = 8

    
class Savienojums():

    """Configuration class for database connection."""
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    unix_socket_path = os.environ.get('INSTANCE_UNIX_SOCKET')

    db_uri= "postgresql://{}:{}@/{}?host={}".format(
        db_user, 
        db_pass, 
        db_name, 
        unix_socket_path
        )
    SQLALCHEMY_DATABASE_URI = db_uri
