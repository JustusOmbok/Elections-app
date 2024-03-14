from flask import render_template, request, jsonify, url_for, redirect, flash
from app import app, db
from flask import session
import requests
from app.models import Admin, President, Governor, Voter, Vote

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/voter/home')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin_register')
def admin_register():
    return render_template('admin_registration.html')

@app.route('/admin/president_register')
def president_register():
    return render_template('presidential_registration.html')

@app.route('/admin/governor_register')
def governor_register():
    return render_template('governor_registration.html')

# Route for rendering the admin dashboard
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    # Check if the admin is logged in
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return render_template('admin_dashboard.html')
    else:
        # If not logged in, redirect to the admin login page
        return redirect(url_for('admin_login'))

@app.route('/presidential_voting')
def presidential_voting():
    return render_template('presidential_voting.html')

@app.route('/governor_voting')
def governor_voting():
    return render_template('governor_voting.html')

@app.route('/governor_results')
def governor_results():
    return render_template('governor_results.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Admin routes
@app.route('/admin/register', methods=['POST'])
def register_admin():
    data = request.form
    new_admin = Admin(work_id=data['work_id'], station=data['station'], name=data['name'], 
                      phone_number=data.get('phone_number'), email=data.get('email'))
    # Additional logic for admin registration
    db.session.add(new_admin)
    db.session.commit()
    return redirect(url_for('admin_login'))  # Redirect to admin login page

@app.route('/admin/login', methods=['GET'])
def admin_login():
    return render_template('admin_login.html')

# Route for handling admin login form submission
@app.route('/admin/login', methods=['POST'])
def admin_login_submit():
    station = request.form.get('station')
    work_id = request.form.get('work_id')

    # Query the database for an admin with the provided Station and Work ID
    admin = Admin.query.filter_by(station=station, work_id=work_id).first()

    if admin:
        # Set a session variable to indicate that the user is logged in
        session['admin_logged_in'] = True
        # Redirect to a dashboard or admin home page
        return redirect(url_for('admin_dashboard'))
    else:
        # If authentication fails, redirect back to the login page with an error message
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('admin_login'))

# Route for handling admin logout
@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    # Clear the session variables
    session.pop('admin_logged_in', None)
    # Redirect to the login page
    return redirect(url_for('admin'))

# Candidate routes
@app.route('/president/register', methods=['POST'])
def register_president():
    data = request.form
    new_president = President(name=data['name'], party_name=data['party_name'])
    db.session.add(new_president)
    db.session.commit()
    return redirect(url_for('admin_dashboard', success='true'))

@app.route('/governor/register', methods=['POST'])
def register_governor():
    data = request.form
    new_governor = Governor(name=data['name'], party_name=data['party_name'], county=data['county_name'])
    db.session.add(new_governor)
    db.session.commit()
    return redirect(url_for('admin_dashboard', success='true'))

# Voter routes
@app.route('/voter/register', methods=['GET', 'POST'])
def register_voter():
    if request.method == 'POST':
        data = request.form
        new_voter = Voter(national_id=data['national_id'], county=data['county'], name=data['name'],
                          phone_number=data.get('phone_number'), email=data.get('email'))
        # Additional logic for voter registration
        db.session.add(new_voter)
        db.session.commit()
        return redirect(url_for('voter_login'))
    else:
        # Render the voter registration form
        return render_template('voter_registration.html')

@app.route('/voter/login', methods=['GET'])
def voter_login():
    return render_template('login.html')
    
# Route for handling voter login form submission
@app.route('/voter/login', methods=['POST'])
def voter_login_submit():
    name = request.form.get('name')
    national_id = request.form.get('national_id')

    # Query the database for a voter with the provided Station and Work ID
    voter = Voter.query.filter_by(name=name, national_id=national_id).first()

    if voter:
        # Set a session variable to indicate that the user is logged in
        session['voter_logged_in'] = True
        # Redirect to a dashboard or voter home page
        return redirect(url_for('home'))
    else:
        # If authentication fails, redirect back to the login page with an error message
        #flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('voter_login'))

# Route for handling voter logout
@app.route('/voter/logout', methods=['GET'])
def voter_logout():
    # Clear the session variables
    session.pop('voter_logged_in', None)
    # Redirect to the login page
    return redirect(url_for('landing_page'))

@app.route('/vote', methods=['POST'])
def vote():
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in to vote'}), 401

    data = request.json
    candidate_id = data.get('candidate_id')

    voter_id = session['user_id']

    # Check if the voter has already voted
    existing_vote = Vote.query.filter_by(voter_id=voter_id).first()
    if existing_vote:
        return jsonify({'error': 'You have already voted'}), 400

    # Create a new vote
    vote = Vote(candidate_id=candidate_id, voter_id=voter_id)
    db.session.add(vote)
    db.session.commit()

    return jsonify({'message': 'Vote cast successfully'}), 201

@app.route('/results', methods=['GET'])
def results():
    # Get results from the database
    candidates = Candidate.query.all()

    # Format results
    results = [{'name': candidate.name, 'votes': len(candidate.votes)} for candidate in candidates]

    return jsonify({'results': results}), 200

@app.route('/presidential_results', methods=['GET'])
def presidential_results():
    # Fetch data from the /results route within the Flask application
    response = requests.get(url_for('results', _external=True))
    if response.status_code == 200:
        data = response.json()['results']

        # Extract candidate names and votes
        candidate_names = [candidate['name'] for candidate in data]
        votes = [candidate['votes'] for candidate in data]

        # Prepare data for the national chart
        national_data = {
            'labels': candidate_names,
            'datasets': [{
                'label': 'Percentage of Votes',
                'data': votes,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                'borderWidth': 1
            }]
        }

        # Calculate total votes
        total_votes = sum(votes)

        return render_template('presidential_results.html', national_data=national_data, total_votes=total_votes)
    else:
        # Handle error
        return "Failed to fetch data from the API", 500