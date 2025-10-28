from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True will auto-reload the server when you save files
    app.run(debug=True)