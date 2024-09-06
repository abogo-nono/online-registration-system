from . import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(250), nullable=True)
    program = db.Column(db.String(100), nullable=False)
    admission_status = db.Column(db.String(50), default="Submitted")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    admissions = db.relationship('Admission', backref='student', lazy=True)
    documents = db.relationship('Document', backref='student', lazy=True)
    payments = db.relationship('Payment', backref='student', lazy=True)


class Admission(db.Model):
    __tablename__ = 'admissions'
    admission_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'),
    nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Submitted')
    review_notes = db.Column(db.Text, nullable=True)
    admitted_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Document(db.Model):
    __tablename__ = 'documents'
    document_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'),
    nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    verification_status = db.Column(db.String(50), default="Pending")
    verified_by = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=True)
    verification_notes = db.Column(db.Text, nullable=True)
