from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import jsonify

import re
import json
from datetime import datetime
import calendar

from app.auth import UserRole
from app.auth import at_least_role
from app.db_manager import sqliteManager as db
from app.queries import queries

import config


mark = Blueprint('mark', __name__)


@mark.route('/mark', methods=['GET', 'POST'])
@at_least_role(UserRole.STAFF)
def mark_submission():
    if request.method == 'GET':
        db.connect()
        task_id = int(request.args.get('task', None))
        student_id = int(request.args.get('student', None))
        task_info = queries.get_general_task_info(task_id)[0]
        # get deadline
        time_format = '%d/%m/%Y at %I:%M:%S %p'
        due_date = datetime.fromtimestamp(task_info[2])
        weekday = \
            calendar.day_name[datetime.fromtimestamp(task_info[2]).weekday()]

        deadline_text = weekday + " " + due_date.strftime(time_format)

        material = queries.get_material_and_attachment(task_id)
        task_criteria = db.select_columns('task_criteria',
                                          ['id', 'task', 'name', 'max_mark'],
                                          ['task'], [task_id])
        student_details = db.select_columns('users', ['name', 'email'],
                                            ['id'], [student_id])

        student_email = student_details[0][1].split('@')[0]
        submission = db.select_columns('submissions', ['name', 'path'],
                                       ['student', 'task'],
                                       [student_id, task_id])

        task_criteria_id = []
        for criteria in task_criteria:
            task_criteria_id.append(criteria[0])

        return render_template('mark_submission.html',
                               topic_request_text=config.TOPIC_REQUEST_TEXT,
                               heading='Mark Submission',
                               title='Mark Submission',
                               deadline=deadline_text,
                               description=task_info[3],
                               criteria=material[0][0],
                               taskCriteria=task_criteria,
                               studentName=student_details[0][0],
                               studentEmail=student_email,
                               submission=submission[0],
                               studentId=student_id,
                               taskCriteriaId=task_criteria_id)

    data = json.loads(request.data)
    marks = data['marks']
    feedback = data['feedback']
    task_id = data['taskId']
    studentId = data['studentId']
    task_criteria = data['taskCriteria']

    for m in marks:
        try:
            val = int(m)
        except except expression as identifier:
            return jsonify({'status': 'fail',
                            'message':
                            'Please enter a integer value for marks'})

    for f in feedback:
        if f == '':
            return jsonify({'status': 'fail',
                            'message': 'Please enter some feedback'})

    db.connect()
    for i in range(len(marks)):
        try:
            db.insert_single(
                'marks',
                [task_criteria[i], studentId,
                 session['id'], marks[i], feedback[i]],
                ['criteria', 'student', 'marker', 'mark', 'feedback']
            )
        except expression as identifier:
            db.update_rows('marks', [marks[i], feedback[i]],
                           ['mark', 'feedback'],
                           ['criteria', 'student', 'marker'],
                           [task_criteria[i], studentId, session['id']])

    return jsonify({'status': 'ok'})