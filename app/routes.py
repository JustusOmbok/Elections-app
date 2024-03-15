from flask import render_template, jsonify, url_for, redirect, flash
from sqlalchemy.orm.exc import NoResultFound
from app import app, db
from flask import session, request
from flask import jsonify
import requests
import time
from sqlalchemy.exc import IntegrityError
from app.models import Admin, President, Governor, Voter, Vote_president, Vote_governor

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

# Route for rendering the vote_president.html file
@app.route('/vote/president', methods=['GET'])
def voting_president():
    # Retrieve all presidents from the database
    presidents = President.query.all()
    return render_template('vote_president.html', presidents=presidents)

# Route for rendering the vote_governor.html file
@app.route('/vote/governor', methods=['GET'])
def voting_governor():
    if 'voter_logged_in' in session:  
        national_id = session.get('national_id')  
        try:
            voter = Voter.query.filter_by(national_id=national_id).one()
            voter_county = voter.county
            governors = Governor.query.filter_by(county=voter_county).all()  # Filter governors by voter's county
            return render_template('vote_governor.html', governors=governors, voter_county=voter_county)
        except NoResultFound:
            flash('No voter found with the provided national ID.', 'error')
            return redirect(url_for('vote_governor'))
    else:
        flash('You need to be logged in to vote.', 'error')
        return redirect(url_for('voter_login'))

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
    new_president = President(name=data['name'], party_name=data['party_name'], party_color=data['party_color'])
    db.session.add(new_president)
    db.session.commit()
    return redirect(url_for('admin_dashboard', success='true'))

@app.route('/governor/register', methods=['POST'])
def register_governor():
    data = request.form
    new_governor = Governor(name=data['name'], party_name=data['party_name'], party_color=data['party_color'], county=data['county_name'])
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
    
@app.route('/voter/login', methods=['POST'])
def voter_login_submit():
    name = request.form.get('name')
    national_id = request.form.get('national_id')

    # Query the database for a voter with the provided name and national_id
    voter = Voter.query.filter_by(name=name, national_id=national_id).first()

    if voter:
        # Set session variables to indicate that the user is logged in
        session['voter_logged_in'] = True
        session['national_id'] = national_id  # Set the national_id in the session
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

# Route for voting for president
@app.route('/vote/president', methods=['POST'])
def vote_president():
    if 'voter_logged_in' in session:  # Ensure the voter is logged in
        national_id = session.get('national_id')  # Get national ID from session
        try:
            voter = Voter.query.filter_by(national_id=national_id).one()
            voter_id = voter.id

            president_id = request.form.get('president_id')
            president = President.query.get(president_id)
            if president:
                # Check if the voter has already voted for this president
                existing_vote = Vote_president.query.filter_by(voter_id=voter_id, president_id=president_id).first()
                if existing_vote:
                    flash('You have already voted for this president.', 'error')
                    return redirect(url_for('home'))

                # Record the vote for president
                new_vote_president = Vote_president(president_id=president_id, voter_id=voter_id)
                db.session.add(new_vote_president)
                db.session.commit()
                flash('Your vote for president has been recorded successfully.', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid president selection.', 'error')
                return redirect(url_for('vote_president'))
        except NoResultFound:
            flash('No voter found with the provided national ID.', 'error')
            return redirect(url_for('vote_president'))
        except IntegrityError:
            flash('You have already voted for this president.', 'error')
            return redirect(url_for('home'))
    else:
        flash('You need to be logged in to vote.', 'error')
        return redirect(url_for('voter_login'))
    
@app.route('/check_vote')
def check_vote():
    if 'voter_logged_in' in session:
        national_id = session.get('national_id')
        try:
            voter = Voter.query.filter_by(national_id=national_id).one()
            voter_id = voter.id
            existing_vote = Vote_president.query.filter_by(voter_id=voter_id).first()
            if existing_vote:
                return jsonify({'alreadyVoted': True})
            else:
                return jsonify({'alreadyVoted': False})
        except NoResultFound:
            return jsonify({'alreadyVoted': False})
    else:
        return jsonify({'alreadyVoted': False})

# Route for voting for governor
@app.route('/vote/governor', methods=['POST'])
def vote_governor():
    if 'voter_logged_in' in session:  # Ensure the voter is logged in
        national_id = session.get('national_id')  # Get national ID from session
        try:
            voter = Voter.query.filter_by(national_id=national_id).one()
            voter_id = voter.id

            governor_id = request.form.get('governor_id')
            governor = Governor.query.get(governor_id)
            if governor:
                # Check if the voter has already voted for this governor
                existing_vote = Vote_governor.query.filter_by(voter_id=voter_id, governor_id=governor_id).first()
                if existing_vote:
                    flash('You have already voted for this governor.', 'error')
                    return redirect(url_for('home'))

                # Record the vote for president
                new_vote_governor = Vote_governor(governor_id=governor_id, voter_id=voter_id)
                db.session.add(new_vote_governor)
                db.session.commit()
                flash('Your vote for governor has been recorded successfully.', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid governor selection.', 'error')
                return redirect(url_for('vote_governor'))
        except NoResultFound:
            flash('No voter found with the provided national ID.', 'error')
            return redirect(url_for('vote_governor'))
        except IntegrityError:
            flash('You have already voted for this governor.', 'error')
            return redirect(url_for('home'))
    else:
        flash('You need to be logged in to vote.', 'error')
        return redirect(url_for('voter_login'))
    
@app.route('/check_vote_governor')
def check_vote_governor():
    if 'voter_logged_in' in session:
        national_id = session.get('national_id')
        try:
            voter = Voter.query.filter_by(national_id=national_id).one()
            voter_id = voter.id
            existing_vote = Vote_governor.query.filter_by(voter_id=voter_id).first()
            if existing_vote:
                return jsonify({'alreadyVoted': True})
            else:
                return jsonify({'alreadyVoted': False})
        except NoResultFound:
            return jsonify({'alreadyVoted': False})
    else:
        return jsonify({'alreadyVoted': False})

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