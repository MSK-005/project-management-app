from src import create_app

# Entering 'python .\main.py' runs the app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)