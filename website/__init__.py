from flask import Flask

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = 'Here can you give a secret key' # secret key for the webb appilaction
    
    from .auth import auth
    
    app.register_blueprint(auth,  url_prefix='/') # / means no prefix
    
    return app
    
    
  
    
    
