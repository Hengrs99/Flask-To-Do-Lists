from website import create_app

#APP SETUP
app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # run the web server