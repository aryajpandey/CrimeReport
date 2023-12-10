from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/crimereportfrnt')
def serve_frontend():
    return render_template('crimereportfrnt.html')

@app.route('/api/submitAddress', methods=['POST'])
def submit_address():
    try:
        data = request.get_json()
        # Process the data as needed
        print('Received data:', data)
        return json.dumps({'success': True}), 200, {'ContentType':'application/json'}
    except Exception as e:
        print('Error processing data:', str(e))
        return json.dumps({'success': False}), 500, {'ContentType':'application/json'}

# Configure your PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:passkey@localhost/Crime'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    streetaddress = db.Column(db.String(255))
    zipcode = db.Column(db.String(10))
    precinct_id = db.Column(db.Integer, db.ForeignKey('precinct.precinct_id'))

class Precinct(db.Model):
    __tablename__ = 'precinct'

    precinct_id = db.Column(db.Integer, primary_key=True)
    on_duty = db.Column(db.Boolean, nullable=False)
    precinct_email = db.Column(db.String(255), nullable=False)
    precinct_phonenum = db.Column(db.String(15), nullable=False)

class CrimeDetails(db.Model):
    __tablename__ = 'crime_details'

    crime_id = db.Column(db.Integer, primary_key=True)
    crime_description = db.Column(db.String(255), nullable=False)
    violent = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    addition_info = db.Column(db.Text)

class SuspectDetails(db.Model):
    __tablename__ = 'suspect_details'

    crime_id = db.Column(db.Integer, db.ForeignKey('crime_details.crime_id'), primary_key=True)
    at_large = db.Column(db.Boolean, nullable=False)
    physicaldescription = db.Column(db.Text)

class MissingPersons(db.Model):
    __tablename__ = 'missing_persons'

    id = db.Column(db.Integer, primary_key=True) 
    visual_description = db.Column(db.Text, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    age = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    guardian_phonenum = db.Column(db.String(15), nullable=False)
    addition_info = db.Column(db.Text)


# Define CRUD operations for each table

@app.route('/locations', methods=['GET', 'POST'])
def handle_locations():
    if request.method == 'POST':
        data = request.json
        new_location = Location(state=data['State'], city=data['City'], streetaddress=data['StreetAddress'],
                                zipcode=data['ZipCode'], precinct_id=data['Precinct_ID'])
        db.session.add(new_location)
        db.session.commit()
        return jsonify({'message': 'Location created'}), 201
    else:
        locations = Location.query.all()
        return jsonify([{'Location_ID': loc.location_id, 'State': loc.state, 'City': loc.city} for loc in locations])

@app.route('/locations/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_location(id):
    location = Location.query.get_or_404(id)
    if request.method == 'GET':
        # Get a specific location
        return jsonify({'Location_ID': location.Location_ID, 'State': location.State, 'City': location.City})
    elif request.method == 'PUT':
        # Update a specific location
        data = request.json
        location.state = data['State']
        location.city = data['City']
        location.streetaddress = data['StreetAddress']
        location.zipcode = data['ZipCode']
        location.precinct_id = data['Precinct_ID']
        db.session.commit()
        return jsonify({'message': 'Location updated'})
    elif request.method == 'DELETE':
        # Delete a specific location
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'Location deleted'})

@app.route('/precincts', methods=['GET', 'POST'])
def handle_precincts():
    if request.method == 'POST':
        # Create a new precinct
        data = request.json
        new_precinct = Precinct(on_duty=data['On_duty'], precinct_email=data['Precinct_email'],
                                precinct_phonenum=data['Precinct_phonenum'])
        db.session.add(new_precinct)
        db.session.commit()
        return jsonify({'message': 'Precinct created'}), 201

    else:
        # Get all precincts
        precincts = Precinct.query.all()
        return jsonify([{'Precinct_ID': p.precinct_id, 'On_duty': p.on_duty, 'Precinct_email': p.precinct_email} for p in precincts])

@app.route('/precincts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_precinct(id):
    precinct = Precinct.query.get_or_404(id)
    if request.method == 'GET':
        # Get a specific precinct
        return jsonify({'Precinct_ID': precinct.Precinct_ID, 'On_duty': precinct.On_duty, 'Precinct_email': precinct.Precinct_email})
    elif request.method == 'PUT':
        # Update a specific precinct
        data = request.json
        precinct.on_duty = data['On_duty']
        precinct.precinct_email = data['Precinct_email']
        precinct.precinct_phonenum = data['Precinct_phonenum']
        db.session.commit()
        return jsonify({'message': 'Precinct updated'})
    elif request.method == 'DELETE':
        # Delete a specific precinct
        db.session.delete(precinct)
        db.session.commit()
        return jsonify({'message': 'Precinct deleted'})

@app.route('/crimedetails', methods=['GET', 'POST'])
def handle_crimedetails():
    if request.method == 'POST':
        # Create a new crime detail
        data = request.json
        new_crime_detail = CrimeDetails(crime_description=data['Crime_description'], violent=data['Violent'],
                                        time=data['Time'], date=data['Date'], location_id=data['Location_ID'],
                                        addition_info=data['addition_info'])
        db.session.add(new_crime_detail)
        db.session.commit()
        return jsonify({'message': 'Crime detail created'}), 201

    else:
        # Get all crime details
        crime_details = CrimeDetails.query.all()
        return jsonify([{'Crime_ID': cd.crime_id, 'Crime_description': cd.crime_description} for cd in crime_details])

@app.route('/crimedetails/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_crimedetail(id):
    crime_detail = CrimeDetails.query.get_or_404(id)
    if request.method == 'GET':
        # Get a specific crime detail
        return jsonify({'Crime_ID': crime_detail.crime_id, 'Crime_description': crime_detail.crime_description})
    elif request.method == 'PUT':
        # Update a specific crime detail
        data = request.json
        crime_detail.crime_description = data['Crime_description']
        crime_detail.violent = data['Violent']
        crime_detail.time = data['Time']
        crime_detail.date = data['Date']
        crime_detail.location_id = data['Location_ID']
        crime_detail.addition_info = data['addition_info']
        db.session.commit()
        return jsonify({'message': 'Crime detail updated'})
    elif request.method == 'DELETE':
        # Delete a specific crime detail
        db.session.delete(crime_detail)
        db.session.commit()
        return jsonify({'message': 'Crime detail deleted'})

@app.route('/suspectdetails', methods=['GET', 'POST'])
def handle_suspectdetails():
    if request.method == 'POST':
        # Create a new suspect detail
        data = request.json
        new_suspect_detail = SuspectDetails(crime_id=data['Crime_ID'], at_large=data['At_large'],
                                            physicaldescription=data['PhysicalDescription'])
        db.session.add(new_suspect_detail)
        db.session.commit()
        return jsonify({'message': 'Suspect detail created'}), 201

    else:
        # Get all suspect details
        suspect_details = SuspectDetails.query.all()
        return jsonify([{'Crime_ID': sd.crime_id, 'At_large': sd.at_large} for sd in suspect_details])

@app.route('/suspectdetails/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_suspectdetail(id):
    suspect_detail = SuspectDetails.query.get_or_404(id)
    if request.method == 'GET':
        # Get a specific suspect detail
        return jsonify({'Crime_ID': suspect_detail.crime_id, 'At_large': suspect_detail.at_large})
    elif request.method == 'PUT':
        # Update a specific suspect detail
        data = request.json
        suspect_detail.at_large = data['At_large']
        suspect_detail.physicaldescription = data['PhysicalDescription']
        db.session.commit()
        return jsonify({'message': 'Suspect detail updated'})
    elif request.method == 'DELETE':
        # Delete a specific suspect detail
        db.session.delete(suspect_detail)
        db.session.commit()
        return jsonify({'message': 'Suspect detail deleted'})

@app.route('/missingpersons', methods=['GET', 'POST'])
def handle_missingpersons():
    if request.method == 'POST':
        # Create a new missing person
        data = request.json
        new_missing_person = MissingPersons(visual_description=data['Visual_description'], location_id=data['Location_ID'],
                                            age=data['Age'], date=data['Date'], guardian_phonenum=data['Guardian_phonenum'],
                                            addition_info=data['addition_info'])
        db.session.add(new_missing_person)
        db.session.commit()
        return jsonify({'message': 'Missing person added'}), 201

    else:
        # Get all missing persons
        missing_persons = MissingPersons.query.all()
        return jsonify([{'ID': mp.id, 'Visual_description': mp.visual_description} for mp in missing_persons])

@app.route('/missingpersons/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_missingperson(id):
    missing_person = MissingPersons.query.get_or_404(id)
    if request.method == 'GET':
        # Get a specific missing person
        return jsonify({'ID': missing_person.id, 'Visual_description': missing_person.visual_description})
    elif request.method == 'PUT':
        # Update a specific missing person
        data = request.json
        missing_person.visual_description = data['Visual_description']
        missing_person.location_id = data['Location_ID']
        missing_person.age = data['Age']
        missing_person.date = data['Date']
        missing_person.guardian_phonenum = data['Guardian_phonenum']
        missing_person.addition_info = data['addition_info']
        db.session.commit()
        return jsonify({'message': 'Missing person updated'})
    elif request.method == 'DELETE':
        # Delete a specific missing person
        db.session.delete(missing_person)
        db.session.commit()
        return jsonify({'message': 'Missing person deleted'})
    

# Create a route to display recorded data
@app.route('/recordedCrimes')
def recorded_crimes():
    # Retrieve all crime details from the database
    crime_details = CrimeDetails.query.all()

    # Render a template to display the recorded data
    return render_template('rec_crimes.html', crime_details=crime_details)

# Create a route to display recorded data with a given ZIP code
@app.route('/recordedCrimes/<string:zip_code>')
def recorded_crimes_by_zip(zip_code):
    # Retrieve all crime details with the specified ZIP code from the database
    crime_details = CrimeDetails.query.join(Location).filter(Location.zipcode == zip_code).all()

    # Render a template to display the recorded data
    return render_template('rec_crimes.html', crime_details=crime_details)



if __name__ == '__main__':
    app.run(debug=True)

