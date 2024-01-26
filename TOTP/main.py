from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, get_flashed_messages
import pyotp
import qrcode
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Sample user database (replace with your actual database connection)
user_database = {
    'Gopi': {'password': '12345', 'secret_key': 'A7FT4VIKVJDH2CMZT2UXERESKG44V5OR'},
    'Nishanth': {'password': '67890', 'secret_key': 'FJA26ZXGVFXXXSO6PPMY7HCEN2IWFQLB'},
    # Add more users as needed
}

@app.route("/")
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    totp = pyotp.TOTP(user_database[session['username']]['secret_key'])
    current_otp = totp.now()

    uri = totp.provisioning_uri(session['username'], issuer_name="YourApp")
    qr_code_data = generate_qr_code(uri)

    return render_template("index.html", username=session['username'], otp=current_otp, qr_code=qr_code_data)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in user_database and user_database[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Wrong Password. Please try again.", "error")

    # Pass flash messages directly to the template
    return render_template("login.html", flash_messages=get_flashed_messages())

@app.route("/verify_totp", methods=["POST"])
def verify_totp():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user = user_database.get(username)

    if user:
        # Get the TOTP from the form data
        entered_totp = request.form.get("totp")

        # Verify the entered TOTP
        totp = pyotp.TOTP(user['secret_key'])
        is_totp_valid = totp.verify(entered_totp)

        if is_totp_valid:
            # TOTP is valid, you can proceed with further actions
            flash("TOTP verification successful.", "success")
        else:
            # TOTP is invalid, flash an error message
            flash("Invalid TOTP. Please try again.", "error")

    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/qr_code")
def get_qr_code():
    if 'username' not in session:
        return redirect(url_for('login'))

    totp = pyotp.TOTP(user_database[session['username']]['secret_key'])
    uri = totp.provisioning_uri(session['username'], issuer_name="YourApp")
    qr_code_data = generate_qr_code(uri)

    return send_file(qr_code_data, mimetype='image/png', download_name='qr_code.png')

def generate_qr_code(uri):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes_io = BytesIO()
    img.save(img_bytes_io)
    img_bytes_io.seek(0)

    return img_bytes_io

if __name__ == "__main__":
    app.run(debug=True)
