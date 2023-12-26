from app import create_app  # Import the application factory function

app = create_app()  # Create the Flask application instance


if __name__ == '__main__':
    app.run(debug=True, port=5001)
