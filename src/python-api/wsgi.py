from app import app  # Import the Flask app from your main app file

if __name__ == "__main__":
    app.run()  # This is for local testing, but in production we will use a WSGI server
