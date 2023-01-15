from flask import Flask,redirect,url_for

# WSGI application
app = Flask(__name__)

@app.route('/')
def welcome():
    return "test page new"

@app.route('/newpage')
def newwelcome():
    return "test page newwelcome"

# Building Url Dynamically with Variable Rules And URL Building

@app.route('/success/<int:score>')
def success(score):
    return "<html><body><h1>The Reult is passed and score is {}</h1></body></html>".format(str(score))


@app.route('/fail/<int:score>')
def fail(score):
    return "The Person has failed and the marks is "+ str(score)

# based on result value, url will redirect to success or fail page
@app.route('/results/<int:marks>')
def results(marks):
    result=""
    if marks<50:
        result='fail'
    else:
        result='success'
    return redirect(url_for(result,score=marks))

if __name__ == '__main__':
    app.run(debug=True)




