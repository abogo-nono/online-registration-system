import os
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .models import Student, Document, Admission, db


main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register_student():
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_password,
        dob=data['dob'],
        phone_number=data['phone_number'],
        address=data.get('address'),
        program=data['program']
    )

    db.session.add(new_student)

    db.session.commit()

    return jsonify({"message": "Student registered successfully!"}), 201


@main.route('/students/<int:student_id>/documents', methods=['POST'])
def upload_documents(student_id):
    file = request.files['document']

    document_type = request.form['document_type']

    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    # Create document entry in DB
    new_document = Document(
        student_id=student_id,
        document_type=document_type,
        file_path=file_path
    )

    db.session.add(new_document)
    db.session.commit()

    return jsonify({"message": "Document uploaded successfully!"}), 201


@main.route('/students/<int:student_id>/admission', methods=['GET'])
def check_admission_status(student_id):
    admission = Admission.query.filter_by(student_id=student_id).first()

    if admission:
        return jsonify({
            "status": admission.status,
            "review_notes": admission.review_notes
        }), 200
    else:
        return jsonify({"message": "Admission record not found!"}), 404
