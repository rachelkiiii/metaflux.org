from flask import request, session, redirect, url_for, make_response
from app import app
from processing import do_addition, get_mode, process_data

# disable debug for production
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "aoejfakcjefwejanavvnakdaeofwvoiejqporafda"

#def clear_session():
#    session['last_action'] = None
    # using session.clear() nulls everything, including the session itself, so you have to check for session AND session['key'] or pop(None) individual session keys
    # session.clear()

# Check credentials, modify session, etc.
#@app.before_request
#def before_request():
#    if 'session_start' not in session:
#        session['session_start'] = datetime.datetime.now()
#    session['last_action'] = datetime.datetime.now()

@app.route('/')
@app.route('/index')
def index():
    return '''
        <html>
        <body style="background-color:black;">
        <h1>hello world</h1>
        </body>
        </html>
    '''

@app.route('/testadd', methods=['GET', 'POST'])
def adder_page():
    errors = ""
    if request.method == 'POST':
        number1 = None
        number2 = None
        try:
            number1 = float(request.form["number1"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        try:
            number2 = float(request.form["number2"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        if number1 is not None and number2 is not None:
            result = do_addition(number1, number2)
            return '''
                <html>
                    <body>
                        <p>The result is {result}</p>
                        <p><a href="/testadd">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)
    return '''
        <html>
            <body>
                {errors}
                <p>Enter your numbers:</p>
                <form method="post" action="/testadd">
                    <p><input name="number1" /></p>
                    <p><input name="number2" /></p>
                    <p><input type="submit" value="Do calculation" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

@app.route('/testmode', methods=['GET', 'POST'])
def mode_page():
    if "inputs" not in session:
        session["inputs"] = []

    errors = ""
    if request.method == 'POST':
        try:
            session["inputs"].append(float(request.form["number"]))
            session.modified = True
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number"])

        if request.form["action"] == "Calculate number":
            result = get_mode(session["inputs"])
            session.clear()
            session.modified = True
            return '''
                <html>
                    <body>
                        <p>{result}</p>
                        <p><a href="/testmode">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)

    if len(session["inputs"]) == 0:
        numbers_so_far = ""
    else:
        numbers_so_far = "<p>Numbers so far:</p>"
        for number in session["inputs"]:
            numbers_so_far += "<p>{}</p>".format(number)

    return '''
        <html>
            <body>
                {numbers_so_far}
                {errors}
                <p>Enter your number:</p>
                <form method="post" action="/testmode">
                    <p><input name="number" /></p>
                    <p><input type="submit" name="action" value="Add another" /></p>
                    <p><input type="submit" name="action" value="Calculate number" /></p>
                </form>
            </body>
        </html>
    '''.format(numbers_so_far=numbers_so_far, errors=errors)

@app.route("/testsum", methods=['GET', 'POST'])
def file_summer_page():
    if request.method == 'POST':
        input_file = request.files["input_file"]
        input_data = input_file.stream.read().decode("utf-8")
        output_data = process_data(input_data)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        return response

    return '''
        <html>
            <body>
                <p>Select the file you want to sum up:</p>
                <form method="post" action="/testsum" enctype="multipart/form-data">
                    <p><input type="file" name="input_file" /></p>
                    <p><input type="submit" value="Process the file" /></p>
                </form>
            </body>
        </html>
    '''
