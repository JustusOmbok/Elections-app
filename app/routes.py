from flask import render_template, jsonify, url_for, redirect, flash
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from app import app, db
from flask import session, request
from flask import jsonify
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import time
import logging
from sqlalchemy.exc import IntegrityError
from app.models import Admin, President, Governor, Voter, Vote_president, Vote_governor
import time

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

# Route for rendering the admin dashboard
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    # Check if the admin is logged in
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return render_template('admin_dashboard.html')
    else:
        # If not logged in, redirect to the admin login page
        return redirect(url_for('admin_login'))
    
# Route for admin delete
@app.route('/admin/delete')
def admin_delete():
    return render_template('admin_delete.html')

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
    return redirect(url_for('admin_login_submit'))  # Redirect to admin login page

# Route for handling admin login form submission
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_submit():
    if request.method == 'POST':
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
            return redirect(url_for('admin_login_submit'))
    return render_template('admin_login.html')

# Route for handling admin logout
@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    # Clear the session variables
    session.pop('admin_logged_in', None)
    # Redirect to the login page
    return redirect(url_for('admin'))

# Candidate routes
@app.route('/president/register', methods=['GET', 'POST'])
def register_president():
    success_message = None
    if request.method == 'POST':
        data = request.form
        existing_president = President.query.filter_by(national_id=data['national_id']).first()
        if existing_president:
            flash('Candidate already exists.')
            return render_template('presidential_registration.html')
        else:
            new_president = President(national_id=data['national_id'], name=data['name'], party_name=data['party_name'], party_color=data['party_color'])
            db.session.add(new_president)
            db.session.commit()
            success_message = 'President registered successfully!'
    return render_template('presidential_registration.html', success_message=success_message)


@app.route('/governor/register', methods=['GET', 'POST'])
def register_governor():
    success_message = None
    if request.method == 'POST':
        data = request.form

        existing_governor = Governor.query.filter_by(national_id=data['national_id']).first()
        if existing_governor:
            flash('Candidate already exists.', 'error')
            return render_template('governor_registration.html')
    
        new_governor = Governor(national_id=data['national_id'], name=data['name'], party_name=data['party_name'], party_color=data['party_color'], county=data['county_name'])
        db.session.add(new_governor)
        db.session.commit()
        success_message = 'Governor registered successfully!'
    return render_template('governor_registration.html', success_message=success_message)

@app.route('/voter/register', methods=['GET', 'POST'])
def register_voter():
    if request.method == 'POST':
        data = request.form
        # Check if password and confirm password match
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match. Please try again.', 'error')
            return "Passwords do not match. Please try again."

        # Check if voter already exists
        existing_voter = Voter.query.filter_by(national_id=data['national_id']).first()
        if existing_voter:
            return "Voter already exists."

        hashed_password = generate_password_hash(data['password'])  # Hash the password
        new_voter = Voter(national_id=data['national_id'], county=data['county'], name=data['name'],
                          phone_number=data.get('phone_number'), email=data.get('email'),
                          password_hash=hashed_password)  # Store hashed password
        # Additional logic for voter registration
        db.session.add(new_voter)
        db.session.commit()
        return "Voter registered successfully."
    else:
        # Render the voter registration form
        return render_template('voter_registration.html')
    
# Update Voter Login Route
@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login_submit():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        password = request.form.get('password')  # Get password from form

        # Query the database for a voter with the provided name and national_id
        voter = Voter.query.filter_by(national_id=national_id).first()

        if voter and check_password_hash(voter.password_hash, password):  # Check hashed password
            # Set session variables to indicate that the user is logged in
            session['voter_logged_in'] = True
            session['national_id'] = national_id  # Set the national_id in the session
            # Redirect to a dashboard or voter home page
            return redirect(url_for('home'))
        else:
            # If authentication fails, flash a message and redirect back to the login page
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('voter_login_submit'))
    return render_template('login.html')

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

@app.route('/viewp_results', methods=['GET'])
def viewp_results():
    # Fetch national results
    national_results = calculate_results()

    # Fetch list of counties from the database
    counties = db.session.query(Voter.county).distinct().all()
    counties = [county[0] for county in counties]  # Convert list of tuples to list of strings

    # Check if county parameter is provided in the request
    county = request.args.get('county')

    if county:
        # Calculate county-wise results
        county_results = calculate_results(county=county)
        logging.debug(f"County Results: {county_results}")
        print("County Results:", county_results)  # Debugging statement
        return render_template('presidential_results.html', national_results=national_results, county_results=county_results, county=county, counties=counties)
    else:
        # Handle the case when county parameter is not provided
        county_results = None
        return render_template('presidential_results.html', national_results=national_results, county_results=county_results, counties=counties)

def calculate_results(county=None):
    logging.info(f"Calculating results for county: {county}")

    # Query to get total votes for each president
    if county:
        president_votes = db.session.query(Vote_president.president_id, func.count(Vote_president.id)).\
            join(Voter).filter(Voter.county == county).\
            group_by(Vote_president.president_id).all()
        total_voters = db.session.query(func.count(Vote_president.id)).\
            join(Voter).filter(Voter.county == county).scalar()
    else:
        president_votes = db.session.query(Vote_president.president_id, func.count(Vote_president.id)).\
            group_by(Vote_president.president_id).all()
        total_voters = db.session.query(func.count(Vote_president.id)).scalar()

    logging.info(f"President votes: {president_votes}")
    logging.info(f"Total voters: {total_voters}")

    # Calculate percentages
    total_votes = sum(votes for _, votes in president_votes)
    results = []
    for president_id, votes in president_votes:
        president = President.query.get(president_id)
        if president:
            percentage = (votes / total_votes) * 100 if total_votes != 0 else 0
            results.append({
                'president': {
                    'id': president.id,
                    'name': president.name,
                    # Add other relevant president attributes here if needed
                },
                'votes': votes,
                'percentage': percentage
            })

    return {'results': results, 'total_voters': total_voters}

# Route for rendering governor election results
@app.route('/results/governor', methods=['GET', 'POST'])
def governor_election_results():
    counties = db.session.query(Voter.county).distinct().all()  # Get distinct counties
    print(counties)
    if request.method == 'POST':
        selected_county = request.form.get('county')
        if selected_county:
            governor_results = db.session.query(Governor.name, func.count(Vote_governor.id)) \
                .join(Vote_governor, Governor.id == Vote_governor.governor_id) \
                .join(Voter, Voter.id == Vote_governor.voter_id) \
                .filter(Voter.county == selected_county) \
                .group_by(Governor.name).all()
            total_votes = db.session.query(func.count(Vote_governor.id)) \
                .join(Voter, Voter.id == Vote_governor.voter_id) \
                .filter(Voter.county == selected_county).scalar()
            return render_template('governor_results.html', governor_results=governor_results, total_votes=total_votes, selected_county=selected_county, counties=counties)
    else:
        # Default to the voter's county if available
        if 'voter_logged_in' in session:
            national_id = session.get('national_id')
            try:
                voter = Voter.query.filter_by(national_id=national_id).one()
                selected_county = voter.county
            except NoResultFound:
                flash('No voter found with the provided national ID.', 'error')
                return redirect(url_for('home'))
        else:
            flash('You need to be logged in to view results.', 'error')
            return redirect(url_for('voter_login'))

        governor_results = db.session.query(Governor.name, func.count(Vote_governor.id)) \
            .join(Vote_governor, Governor.id == Vote_governor.governor_id) \
            .join(Voter, Voter.id == Vote_governor.voter_id) \
            .filter(Voter.county == selected_county) \
            .group_by(Governor.name).all()
        total_votes = db.session.query(func.count(Vote_governor.id)) \
            .join(Voter, Voter.id == Vote_governor.voter_id) \
            .filter(Voter.county == selected_county).scalar()
        return render_template('governor_results.html', governor_results=governor_results, total_votes=total_votes, selected_county=selected_county, counties=counties)
    
# Route for deleting a president
@app.route('/admin/delete_president', methods=['POST'])
def delete_president():
    national_id = request.form.get('national_id')
    president = President.query.filter_by(national_id=national_id).first()
    if president:
        db.session.delete(president)
        db.session.commit()
        flash(f"Removed {president.name}", 'success')
        #time.sleep(3)  # Wait for 3 seconds
        return f"Removed {president.name}"
    else:
        flash("President does not exist.", 'danger')
        return "President does not exist."

# Route for deleting a governor
@app.route('/admin/delete_governor', methods=['POST'])
def delete_governor():
    national_id = request.form.get('national_id')
    governor = Governor.query.filter_by(national_id=national_id).first()
    if governor:
        db.session.delete(governor)
        db.session.commit()
        flash(f"Removed {governor.name}", 'success')
        #time.sleep(3)  # Wait for 3 seconds
        return f"Removed {governor.name}"
    else:
        flash("Governor does not exist.", 'danger')
        return "Governor does not exist."

# Route for deleting a voter
@app.route('/admin/delete_voter', methods=['POST'])
def delete_voter():
    national_id = request.form.get('national_id')
    voter = Voter.query.filter_by(national_id=national_id).first()
    if voter:
        db.session.delete(voter)
        db.session.commit()
        flash(f"Removed {voter.name}", 'success')
        return f"Removed {voter.name}"
    else:
        flash("Voter does not exist.", 'danger')
        return "Voter does not exist."

@app.route('/admin/update/president/<national_id>', methods=['GET', 'POST'])
def update_president(national_id):
    president = President.query.filter_by(national_id=national_id).first()
    success_message = None  # Initialize success message flag
    if request.method == 'POST':
        if president:
            president.name = request.form['name']
            president.party_name = request.form['party_name']
            president.party_color = request.form['party_color']
            db.session.commit()
            success_message = 'President details updated successfully!'
        else:
            flash('President with provided National ID not found!', 'error')
            return redirect(url_for('update_president', national_id=national_id))  # Redirect back to update page
    return render_template('update_president.html', president=president, success_message=success_message)

@app.route('/admin/get_president_details/<national_id>')
def get_president_details(national_id):
    president = President.query.filter_by(national_id=national_id).first()
    if president:
        return jsonify({'success': True, 'candidate': {'name': president.name, 'party_name': president.party_name, 'party_color': president.party_color}})
    else:
        return jsonify({'success': False})

@app.route('/admin/update_governor', methods=['POST'])
def update_governor():
    national_id = request.form['national_id']
    governor = Governor.query.filter_by(national_id=national_id).first()
    if governor:
        governor.name = request.form['name']
        governor.party_name = request.form['party_name']
        governor.party_color = request.form['party_color']
        governor.county = request.form['county']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Governor details updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'Governor not found'})

@app.route('/admin/get_governor_details/<national_id>')
def get_governor_details(national_id):
    governor = Governor.query.filter_by(national_id=national_id).first()
    if governor:
        return jsonify({'success': True, 'candidate': {'name': governor.name, 'party_name': governor.party_name, 'party_color': governor.party_color, 'county': governor.county}})
    else:
        return jsonify({'success': False})

@app.route('/admin/get_governors_by_county', methods=['GET', 'POST'])
def get_governors_by_county():
    if request.method == 'POST':
        county_name = request.form['county']  # Assuming the dropdown in the HTML sends the selected county name
        governors = Governor.query.filter_by(county=county_name).all()
        governor_list = [{'national_id': governor.national_id, 'name': governor.name} for governor in governors]
        return jsonify({'governors': governor_list})
    return render_template('update_governor.html')

@app.route('/admin/get_counties', methods=['GET'])
def get_counties():
    counties = Governor.query.distinct(Governor.county).all()
    county_list = [county.county for county in counties]
    return jsonify({'counties': county_list})
    
# Update the Flask route to fetch the details of the logged-in voter
@app.route('/update_voter', methods=['GET', 'POST'])
def update_voter():
    national_id = session.get('national_id')
    voter = Voter.query.filter_by(national_id=national_id).first()
    success_message = None

    if request.method == 'POST':
        if voter:
            voter.county = request.form['county']
            voter.name = request.form['name']
            voter.phone_number = request.form['phone_number']
            voter.email = request.form['email']
            db.session.commit()
            success_message = 'Voter details updated successfully!'
        else:
            flash('Voter with provided National ID not found!', 'error')

    return render_template('update_voter.html', voter=voter, success_message=success_message)