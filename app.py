# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100))
    credits = db.Column(db.Integer)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')
# edit the coourse
@app.route('/api/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify({
        'id': course.id,
        'course_code': course.course_code,
        'course_name': course.course_name,
        'instructor': course.instructor,
        'credits': course.credits
    })

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': course.id,
        'course_code': course.course_code,
        'course_name': course.course_name,
        'instructor': course.instructor,
        'credits': course.credits
    } for course in courses])

@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.json
    new_course = Course(
        course_code=data['course_code'],
        course_name=data['course_name'],
        instructor=data['instructor'],
        credits=data['credits']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully'})

@app.route('/api/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.json
    course.course_code = data['course_code']
    course.course_name = data['course_name']
    course.instructor = data['instructor']
    course.credits = data['credits']
    db.session.commit()
    return jsonify({'message': 'Course updated successfully'})

@app.route('/api/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)