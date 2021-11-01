from website import create_app # default run  __init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    
    

