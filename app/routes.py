from flask import render_template, request, jsonify, url_for
from app import app, db
from flask import session
import requests
from app.models import Admin, Candidate, Voter, Vote

@app.route('/')
def landng_page():
    return render_template('landing_page.html')

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/presidential_voting')
def presidential_voting():
    return render_template('presidential_voting.html')

@app.route('/governor_voting')
def governor_voting():
    return render_template('governor_voting.html')

#@app.route('/presidential_results')
#def presidential_results():
 #   return render_template('presidential_results.html')

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
    data = request.json
    new_admin = Admin(work_id=data['work_id'], station=data['station'], name=data['name'], 
                      phone_number=data.get('phone_number'), email=data.get('email'))
    # Additional logic for admin registration
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin registered successfully'}), 201

@app.route('/admin/login', methods=['POST'])
def admin_login():
    # Implementation for admin login
    pass

# Candidate routes
@app.route('/candidate/register', methods=['POST'])
def register_candidate():
    data = request.json
    new_candidate = Candidate(name=data['name'], party_name=data['party_name'], party_symbol=data['party_symbol'])
    db.session.add(new_candidate)
    db.session.commit()
    return jsonify({'message': 'Candidate registered successfully'}), 201

# Voter routes
@app.route('/voter/register', methods=['POST'])
def register_voter():
    data = request.json
    new_voter = Voter(national_id=data['national_id'], county=data['county'], name=data['name'],
                      phone_number=data.get('phone_number'), email=data.get('email'),
                      username=data['username'], password=data['password'])
    # Additional logic for voter registration
    db.session.add(new_voter)
    db.session.commit()
    return jsonify({'message': 'Voter registered successfully'}), 201

@app.route('/voter/login', methods=['POST'])
def voter_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verify credentials
    voter = Voter.query.filter_by(username=username).first()
    if voter and voter.check_password(password):
        session['user_id'] = voter.id
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/voter/logout', methods=['POST'])
def voter_logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

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