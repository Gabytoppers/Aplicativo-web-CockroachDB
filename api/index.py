from app import app  

# Define el handler para Vercel
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
