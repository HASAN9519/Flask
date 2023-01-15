from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

# jinja2 templates
'''
{%...%} for staements conditions, for loop
{{  }} expressions for print
{# .... #} for comment
'''

@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/success/<int:score>')
def success(score):
    return render_template('result1.html',result=score)

# HTTP GET And POST
# values of all name fields from input is passed to submit

@app.route('/submit',methods=['POST','GET'])
def submit():
    total_score=0
    if request.method=='POST':

        science = float(request.form['science'])
        maths = float(request.form['maths'])
        c = float(request.form['c'])
        data_science = float(request.form['datascience'])
        total_score = (science+maths+c+data_science)/4

    return redirect(url_for('success',score=total_score))  # redirecting to success

if __name__=='__main__':
    app.run(debug=True)