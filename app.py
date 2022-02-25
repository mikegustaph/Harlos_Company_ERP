from erp import create_app, initialize_db


application = create_app()

if __name__ == "__main__":
    initialize_db(application, config=True)
    application.run(debug=True)