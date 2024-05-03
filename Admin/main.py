from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = '7s3p3uBZ'

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'Passw0rd':
            session['admin_logged_in'] = True
            return redirect('/admin/index')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/admin/index')
def admin_index():
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return render_template('index.html')
    else:
        return redirect('/admin/login')

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

if __name__ == '__main__':
    app.run(debug=True)
