import re
from geopy.distance import geodesic
from math import radians, sin, cos, sqrt, atan2
from flask import Flask, render_template, request, redirect, url_for, flash,session,send_file,abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,FileField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField  
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector 
from mysql.connector import pooling
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import send_from_directory
# db_connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="emergencyservices"
# )


connection_pool = pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    pool_reset_session=True,
    host='localhost',
    user='root',
    password='',
    database='emergencyservices'
)
db_connection = connection_pool.get_connection()






app = Flask(__name__)
app.config['12'] = 'sr123' 
app.secret_key = 'sr123'


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    for user in user:
        if user.id == user_id:
            return user
    return None



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def home():
     return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        registration_type = request.form['registrationType']
        if registration_type == 'user':
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            email = request.form['email']
            fullName = request.form['fullName']
            phoneNumber = request.form['phoneNumber']
            profilePic=request.files['profilePic']
            pic_path = os.path.join('user_profile_pic', profilePic.filename)
            profilePic.save(pic_path)
            cursor =   db_connection.cursor()
            cursor.execute("INSERT INTO user (username, password_hash, email, full_name, phone_number,profile_pic_path) VALUES (%s, %s, %s, %s, %s,%s)",
                (username, password, email, fullName, phoneNumber,pic_path))
            cursor.close()
        elif  registration_type == 'service_provider' :
            providerType = request.form['providerType']
            userName = request.form['userName']
            password = generate_password_hash(request.form['password'])
            email = request.form['email']
            contactNumber = request.form['contactNumber']
            license=request.files['license']
            license_path = os.path.join('serviceprovider_license', license.filename)
            license.save(license_path)
            location = request.form['location']
            profilePic=request.files['profilePic']
            pic_path = os.path.join('serviceprovider_profile_pic', profilePic.filename)
            profilePic.save(pic_path)
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO service_provider (provider_type, user_name, password, email, contact_number,license_document_path,location,profile_pic_path) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)",
                (providerType, userName, password, email, contactNumber,license_path,location,pic_path))
            db_connection.commit()
            cursor.close()
       
        
        
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['loginType']

        cursor = db_connection.cursor()

        if login_type == 'user':
            cursor.execute("SELECT id, password_hash FROM user WHERE username = %s", (username,))
        elif login_type == 'service_provider':
            cursor.execute("SELECT id, password FROM service_provider WHERE user_name = %s", (username,))

        user = cursor.fetchone()
     
        if user and check_password_hash(user[1], password):
            # Login successful
            session['user_id'] = user[0]
            flash('Login successful.', 'success')
        if login_type == 'user':
                return redirect(url_for('user_dashboard'))
        elif login_type == 'service_provider':
                return redirect(url_for('service_provider_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
        cursor.close()
    
    return render_template('login.html')


        
@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        user_id=session['user_id']
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user is not None and 'profile_pic_path' in user:
            image_path = f"{user['profile_pic_path']}"
        else:
            image_path = "defaultimage.png" 
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        cursor.close()
        if user:
            return render_template('user_dashboard.html', user=user,encoded_image=encoded_image)
           
        else:
            return redirect(url_for('login'))
    cursor.commit()   
@app.route('/service_provider_dashboard')
def service_provider_dashboard():
    if 'user_id' in session:
        service_provider_id = session['user_id']
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM service_provider WHERE id = %s", (service_provider_id,))
        user = cursor.fetchone()
        image_path = f"{user['profile_pic_path']}"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        cursor.close()
        # db_connection.close()
       
        if user:
            return render_template('service_provider_dashboard.html', service_provider=user,encoded_image=encoded_image)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login')) 



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/request_help_form')
def request_help_form():
    return render_template('request_help.html')









@app.route('/submit_help_request', methods=['GET', 'POST'])
def request_help():
    if request.method == 'POST':
        user_id = session['user_id']
        location = request.form['location']
        help_type = request.form['help_type']
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO requests (user_id, location, help_type, status) VALUES (%s, %s, %s, 'Pending')",
            (user_id, location, help_type))
        db_connection.commit()
        cursor.close()
        # db_connection.close()
        return redirect(url_for('request_confirmation'))
        # return redirect(url_for('user_view_accepted_requests'))
    return render_template('request_help.html')



@app.route('/request_confirmation')
def request_confirmation():
    return redirect(url_for('user_dashboard'))



@app.route('/view_requests/<string:provider_type>/<int:provider_id>', methods=['GET'])
def view_requests(provider_type,provider_id):
    if provider_type== "doctor":
        helpType="medical"
    if provider_type== "mechanic":
        helpType="vehicle_repair"
    if provider_type== "fuel_provider":
        helpType="fuel_delivery"

    cursor = db_connection.cursor()
   
    cursor.execute("SELECT * FROM requests WHERE help_type = %s AND status IN ('Pending', 'Accepted', 'Rejected') AND id NOT IN ( SELECT request_id FROM accepted_request WHERE service_provider_id = %s);",(helpType,provider_id))
    pending_requests = cursor.fetchall()
    # cursor.close()
    # db_connection.close()
    return render_template('view_requests.html', requests=pending_requests,provider_type=provider_type,provider_id=provider_id)



@app.route('/accept_request/<int:request_id>/<string:provider_type>/<int:provider_id>', methods=['POST'])
def accept_request(request_id,provider_type,provider_id):
    if request.method == 'POST':
        accept_value = request.form['accept']
        if accept_value == '1':
            cursor = db_connection.cursor()
            cursor.execute("UPDATE requests SET status = 'Accepted' WHERE id = %s", (request_id,))
            db_connection.commit()
            cursor.close()
            cursor = db_connection.cursor()
            cursor.execute("INSERT into accepted_request (request_id,service_provider_id) VALUES (%s,%s)", (request_id,session['user_id']))
            db_connection.commit() 
            cursor.close()
            # db_connection.close()
            return redirect(url_for('view_requests', provider_type=provider_type,provider_id=provider_id))
        elif accept_value == '0':
            cursor = db_connection.cursor()
            cursor.execute("UPDATE requests SET status = 'Rejected' WHERE id = %s", (request_id,))
            db_connection.commit()  
            cursor.close()
            # db_connection.close()
            return redirect(url_for('view_requests', provider_type=provider_type,provider_id=provider_id))
            
    else :
        return redirect(url_for('view_requests', provider_type=provider_type,provider_id=provider_id))







@app.route('/user_view_accepted_requests', methods=['GET'])
def user_view_accepted_requests():
    request_id = request.args.get('request_id')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM accepted_request WHERE request_id = %s", (request_id,))
    accepted_providers = cursor.fetchall()  
    cursor.close()
    # db_connection.close()
    return render_template('user_view_accepted_requests.html', providers=accepted_providers)




@app.route('/confirm_request', methods=['POST'])
def confirm_request():
    request_id = request.form.get('request_id')
    service_provider_id = request.form.get('service_provider_id')
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO accepted_request (request_id, service_provider_id) VALUES (%s, %s)", (request_id, service_provider_id))
    db_connection.commit()
    cursor.close()
    # db_connection.close()
    return redirect(url_for('confirmation_page'))

   

        

      
    







@app.route('/user_request_dashboard')
def user_request_dashboard():
    user_id = session.get('user_id')
    past_requests = get_past_requests(user_id) 
    print(past_requests)
    return render_template('user_request_dashboard.html', past_requests=past_requests)

def get_past_requests(user_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM requests WHERE user_id = %s AND status = 'Completed'", (user_id,))
    past_requests = cursor.fetchall()
    cursor.close()
    # db_connection.close()
    return past_requests

def get_current_requests(user_id):
    cursor = db_connection.cursor()             
    cursor.execute("SELECT * FROM requests WHERE user_id = %s AND status != 'Completed'", (user_id,))
    current_requests = cursor.fetchall()
    cursor.close()
    # db_connection.close()
    return current_requests

def get_accepted_service_providers(request_id):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT s.* FROM service_provider s JOIN accepted_request ar ON s.id = ar.service_provider_id WHERE ar.request_id = %s", (request_id,))
    accepted_providers = cursor.fetchall()
    cursor.close()
    # db_connection.close()
    return accepted_providers




@app.route('/get_accepted_providers')
def get_accepted_providers():
    request_id = request.args.get('request_id')
    accepted_providers = get_accepted_service_providers(request_id)
    return jsonify({"accepted_providers": accepted_providers})


# @app.route('/confirm_service_provider', methods=['POST'])
# def confirm_service_provider():
#     data = request.get_json()
#     request_id = data['request_id']
#     service_provider_id = data['service_provider_id']
#     cursor = db_connection.cursor()
#     cursor.execute("UPDATE request SET confirmed_service_provider_id = %s WHERE id = %s",(service_provider_id, request_id))
#     cursor.commit()
#     cursor.close()
#     # db_connection.close()
#     return jsonify({"success": True}) 



@app.route('/confirm_service_provider', methods=['POST'])
def confirm_service_provider():
    if 'user_id' in session:
        user_id = session['user_id']
        request_id = request.form.get('request_id')
        provider_id = request.form.get('provider_id')

        cursor = db_connection.cursor()

        # Check if the user is authorized to confirm the service provider
        # cursor.execute("SELECT * FROM accepted_request WHERE request_id IN (SELECT id FROM requests WHERE user_id = %s AND status != 'Completed' ORDER BY id DESC LIMIT 1) AND service_provider_id = %s", (user_id, provider_id))
        # accepted_request = cursor.fetchone()

        # if accepted_request:
            # Perform the confirmation logic here, e.g., update the database
            # cursor.execute("UPDATE request SET confirmed = 1 WHERE request_id = %s AND service_provider_id = %s", (accepted_request[0], provider_id))
        
        cursor.execute("UPDATE service_provider SET sender_user_id = %s WHERE id = %s", (user_id,provider_id,))
        cursor.execute("UPDATE requests SET status = 'Confirmed', confirmed_service_provider_id = %s WHERE id = %s", (provider_id, request_id))
        db_connection.commit()
        cursor.close()
        flash('Service provider confirmed successfully.', 'success')
        return redirect(url_for('service_provider_details', service_provider_id=provider_id,request_id=request_id))

    else:
        flash('User is not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route('/service_provider_details/<int:service_provider_id>/<int:request_id>')
def service_provider_details(service_provider_id, request_id):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service_provider WHERE id = %s", (service_provider_id,))
    service_provider = cursor.fetchall()
    cursor.close()
    location_string = service_provider[0]['location']
    pattern = r'Latitude: ([-+]?\d*\.\d+|\d+), Longitude: ([-+]?\d*\.\d+|\d+)'
    match = re.search(pattern, location_string)
    latitude = float(match.group(1))
    longitude = float(match.group(2))
    loc=f"{latitude},{longitude}"

    send_mail(service_provider[0]['email'],loc,)
    # Update the has_notification status for the selected service provider
    cursor = db_connection.cursor()
    cursor.execute("UPDATE service_provider SET has_notification = 1 WHERE id = %s", (service_provider_id,))
    db_connection.commit()
    cursor.close()
    image_path = f"{service_provider[0]['profile_pic_path']}"
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    user_id=session['user_id']
    return render_template('service_provider_details.html', service_provider=service_provider,requestid=request_id,userid=user_id,image=encoded_image)



def send_mail(receiver_email, location):
    sender_email = "roadsidehelperhub@gmail.com"
    sender_password = "cxjc kvsa esnm xssa"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "You've been selected!"

    # Email content with clickable location link
    body = f"You have been selected as the service provider for the request. Please provide the service as soon as possible.\n\nLocation: <a href='https://www.google.com/maps?q={location}' target='_blank'>Click here to view the location on Google Maps</a>\n\n\n"
    
    # Attach HTML content
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email could not be sent:", str(e))








@app.route('/cancel_request/<int:request_id>')
def cancel_request(request_id):
    # Implement logic to cancel the request with the specified request_id
    # Update the request status or remove it from the database
    return redirect('/user_request_dashboard')









# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Check admin credentials (you may use a database for this)
        username = request.form.get('username')
        password = request.form.get('password')
        # Validate credentials (replace this with your authentication logic)
        if username == 'sr' and password == 'sr':
            # Redirect to admin dashboard on successful login
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')











@app.route('/confirmation_page')
def confirmation_page():
    return render_template('confirmation_page.html')






@app.route('/user_details/<int:user_id>')
def user_details(user_id):
     cursor = db_connection.cursor()
     cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
     user_details = cursor.fetchone()
     cursor.execute("SELECT location FROM requests WHERE user_id = %s AND status != 'Completed' ORDER BY id DESC LIMIT 1", (user_id,))
     location=cursor.fetchone()
     image_path = f"{user_details[6]}"
 
     with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
     cursor.close()
     return render_template('user_details.html', user = user_details,encoded_image=encoded_image,location=location)





















@app.route('/admin_dashboard')
def admin_dashboard():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service_provider")
    all_providers = cursor.fetchall()
    
    return render_template('admin_dashboard.html', all_providers=all_providers)

@app.route('/activate_service_provider/<int:provider_id>', methods=['POST'])
def activate_service_provider(provider_id):
    cursor=db_connection.cursor()
    cursor.execute("UPDATE service_provider SET status = 1 WHERE id = %s", (provider_id,))
    db_connection.commit()
    cursor.close()
    # Perform the activation process, update the provider's status in the database, etc.
    # Return a JSON response indicating the success or failure of the activation
    return jsonify({'success': True})  # Adjust based on your implementation

@app.route('/deactivate_service_provider/<int:provider_id>', methods=['POST'])
def deactivate_service_provider(provider_id):
    cursor=db_connection.cursor()
    cursor.execute("UPDATE service_provider SET status = 0 WHERE id = %s", (provider_id,))
    db_connection.commit()
    cursor.close()
    # Perform the deactivation process, update the provider's status in the database, etc.
    # Return a JSON response indicating the success or failure of the deactivation
    return jsonify({'success': True})  # Adjust based on your implementation









@app.route('/admin_logout')
def admin_logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))





@app.route('/feedback_form', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        service_provider_id = request.form.get('service_provider_id')
        user_id = request.form.get('user_id')
        rating = request.form.get('rating')
        comments = request.form.get('comments')
        cursor = db_connection.cursor()
        try:
            cursor.execute("INSERT INTO feedback (request_id, service_provider_id, user_id, rating, comments) VALUES (%s, %s, %s, %s, %s)",
                   (request_id, service_provider_id, user_id, rating, comments))
            cursor.execute("UPDATE service_provider SET rating_points = rating_points + %s WHERE id = %s", (rating, service_provider_id))
            db_connection.commit()
            print("Record inserted successfully")
        except Exception as e:
            print(f"Error inserting record: {e}")
            db_connection.rollback()
        return redirect(url_for('thank_you'))

    return render_template('feedback.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    user_id = request.args.get('userid')
    request_id = request.args.get('requestid') 
    service_provider_id = request.args.get('serviceproviderid')
    cursor = db_connection.cursor()
    cursor.execute("UPDATE service_provider SET has_notification = 0 WHERE id = %s", (service_provider_id,))
    cursor.execute("UPDATE requests SET  status = 'Completed' WHERE id = %s", (request_id,))
    db_connection.commit()
    return render_template('feedback.html',userid=user_id,serviceproviderid=service_provider_id,requestid=request_id)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')






@app.route('/feedback_display/<int:provider_id>')
def feedback_display(provider_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM feedback WHERE service_provider_id = %s", (provider_id,))
    feedback_list =  cursor.fetchall()
    return render_template('feedback_display.html', feedback_list=feedback_list)








@app.route('/user_editprofile/<int:user_id>', methods=['GET', 'POST'])
def user_editprofile(user_id):
    if request.method == 'GET':
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        image_path = f"{user['profile_pic_path']}"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return render_template('user_editprofile.html', user=user,encoded_image=encoded_image)

    elif request.method == 'POST':
        username= request.form.get('username')
        email= request.form.get('email')
        full_name = request.form.get('fullName')
        phone_number= request.form.get('phoneNumber')
        cursor =   db_connection.cursor()
        cursor.execute(" UPDATE user SET username = %s, email = %s, full_name = %s, phone_number = %s WHERE id = %s", (username,email,full_name,phone_number,user_id,))
        db_connection.commit()
        if 'profilePic' in request.files:
            profile_pic = request.files['profilePic']
            pic_path = os.path.join('user_profile_pic', profile_pic.filename)
            profile_pic.save(pic_path)        
            cursor =   db_connection.cursor()
            cursor.execute(" UPDATE user SET profile_pic_path = %s WHERE id = %s", (pic_path,user_id,))
            db_connection.commit()
            # Save the new profile picture and update the path in user data
            # You need to implement the logic to save the file to the server
            # and update the 'profile_pic_path' accordingly.
        return redirect(url_for('user_dashboard'))





@app.route('/serviceprovider_editprofile/<int:provider_id>', methods=['GET', 'POST'])
def serviceprovider_editprofile(provider_id):
    if request.method == 'GET':
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM service_provider WHERE id = %s", (provider_id,))
        user = cursor.fetchone()
        cursor.close()
    
        image_path = f"{user['profile_pic_path']}"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return render_template('serviceprovider_editprofile.html', user=user,encoded_image=encoded_image)

    elif request.method == 'POST':
        username= request.form.get('username')
        email= request.form.get('email')
        provider_type = request.form.get('providerType')
        location = request.form.get('location')
        phone_number= request.form.get('phoneNumber')
        cursor =   db_connection.cursor()
        cursor.execute(" UPDATE service_provider SET user_name = %s, email = %s, provider_type = %s, location = %s, contact_number = %s WHERE id = %s", (username,email,provider_type,location,phone_number,))
        db_connection.commit()
        if 'profilePic' in request.files:
            profile_pic = request.files['profilePic']
            pic_path = os.path.join('serviceprovider_profile_pic', profile_pic.filename)
            profile_pic.save(pic_path)        
            cursor =   db_connection.cursor()
            cursor.execute(" UPDATE service_provider SET profile_pic_path = %s WHERE id = %s", (pic_path,provider_id,))
            db_connection.commit()
            # Save the new profile picture and update the path in user data
            # You need to implement the logic to save the file to the server
            # and update the 'profile_pic_path' accordingly.
        return redirect(url_for('service_provider_dashboard'))

          


          

@app.route('/user_profilepic/<filename>')
def user_profilepic(filename):
    return send_from_directory(app.config['user_profile_pic'], filename)














@app.route('/view_license/<filename>')
def view_license(filename):
    try:
        # Provide the correct path to your PDF files
        path = f'./{filename}'
        return send_file(path, mimetype='application/pdf')
    except FileNotFoundError:
        abort(404)










def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on a sphere
    R = 6371  # Radius of the Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def get_closest_locations(target_latitude, target_longitude,service_providers):
    cursor = db_connection.cursor()
    print(service_providers)
    locations = cursor.fetchall()

    # Calculate distances using the Haversine formula and create a list of tuples
    location_distances = []
    for location_string in locations:
        match = re.search(r'Latitude: ([-\d.]+), Longitude: ([-\d.]+)', location_string[0])

        if match:
            lat, lon = map(float, match.groups())
            distance = haversine(target_latitude, target_longitude, lat, lon)
            location_distances.append((location_string[0], distance))

    # Close the database connection
    cursor.close()
    db_connection.close()

    # Sort the locations based on distance
    sorted_locations = sorted(location_distances, key=lambda x: x[1])

    return sorted_locations



   

   



import re
from geopy.distance import geodesic

@app.route('/current_request_details')
def current_request_details():
    user_id = session.get('user_id')
    if user_id:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user_profile = cursor.fetchall()
        cursor.close()
        # Get the user's current request 
        current_request = get_current_request(user_id)
        if current_request:
            location_string = current_request['location']
            pattern = r'Latitude: ([-+]?\d*\.\d+|\d+), Longitude: ([-+]?\d*\.\d+|\d+)'
            match = re.search(pattern, location_string)
            latitude = float(match.group(1))
            longitude = float(match.group(2))
            
            def calculate_distance(provider):
                provider_location_str = provider['location']
                provider_location = tuple(float(coord.split(': ')[1]) for coord in provider_location_str.split(', '))
                return geodesic(target_location, provider_location).km
            
            target_location = (latitude, longitude)
            accepted_providers = get_accepted_service_providers(current_request['id'])
            sorted_providers = sorted(accepted_providers, key=calculate_distance)
            
            
            
            return render_template('current_request_details.html', user=user_profile, request=current_request, accepted_providers=sorted_providers)
        else:
            return "You don't have a current request."
    else:
        return redirect(url_for('login'))

def get_current_request(user_id):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM requests WHERE user_id = %s AND status != 'Completed' ORDER BY id DESC LIMIT 1", (user_id,))

    current_request = cursor.fetchone()
    cursor.close()
    return current_request
























@app.route('/get_requests_by_date', methods=['GET'])
def get_requests_by_date():
    try:
        start = request.args.get('start_date')
        end = request.args.get('end_date')
        start_date = start+' 00:00:00'
        end_date = end+' 00:00:00'
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM requests WHERE timestamp_column BETWEEN %s AND %s"
        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return str(e)







@app.route('/get_service_provider_details/<int:provider_id>', methods=['GET'])
def get_service_provider_details(provider_id):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service_provider WHERE id = %s", (provider_id,))
    service_provider = cursor.fetchone()
    cursor.close()
    print(service_provider)
    return jsonify(service_provider)

@app.route('/get_user_details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    print(user)
    return jsonify(user)
   






if __name__ == '__main__' :
    app.run(debug=True)