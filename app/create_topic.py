from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from flask import session

from app.auth import at_least_role
from app.auth import UserRole
from app.db_manager import sqliteManager as db
from app.helpers import error
from app.queries import queries

import re
import json

import config


create_topic = Blueprint('create_topic', __name__)


@create_topic.route('/create_topic', methods=['GET', 'POST'])
@at_least_role(UserRole.STAFF)
def create():
    if request.method == 'GET':
        return render_template('create_topic.html', heading='Create Topic',
                               title='Create Topic')

    try:
        data = json.loads(request.data)
        topic = data['topic']
        areas = [area['tag'] for area in data['topic_area']]
        prereqs = [prereq['tag'] for prereq in data['prereqs']]
        details = data['details']
    except ValueError as e:
        return e.args[0]

    # make sure the course codes are uppercase and strip for areas and prereqs
    if len(areas) == 0:
        return error('You should enter at least one topic area')
    original_prereqs = prereqs
    prereqs = [x.upper().strip() for x in prereqs]
    areas = [x.strip() for x in areas]

    db.connect()
    user_id = session['id']

    # test if there are such courses in the database
    course_ids = []
    i = 0
    for prereq in prereqs:
        course_id = db.select_columns(
            'courses', ['id', 'prereq'], ['code'], [prereq]
        )
        if len(course_id) == 0:
            db.close()
            err_msg = f'{original_prereqs[i]} is an unknown course code!'
            if not re.match(config.COURSE_CODE_FORMAT, prereqs[i]):
                err_msg = f'{original_prereqs[i]} is an invalid course code!'
            return error(err_msg)
        if course_id[0][1] == 0:
            db.close()
            return error(f'{prereqs[i]} cannot be a prerequisite!')
        course_ids.append(course_id[0][0])
        i += 1

    # test if there is such topic in the database
    res = db.select_columns('topics', ['name'], ['name'], [topic])

    # only check the name of the topic
    if len(res):
        db.close()
        return error('A topic with that name already exists!')

    # now start to insert data into db
    # insert topic and get its id
    db.insert_single('topics', [topic, user_id, details],
                     ['name', 'supervisor', 'description'])
    topic_id = db.select_columns('topics',
                                 ['id'], ['name'], [topic])[0][0]

    # now get topic areas
    for area in areas:
        # get area_id if area in database
        area_id = db.select_columns('topic_areas',
                                    ['id'],
                                    ['name'],
                                    [area])
        # else add area to database and get the id
        if len(area_id) == 0:
            db.insert_single('topic_areas',
                             [area],
                             ['name'])
            area_id = db.select_columns('topic_areas',
                                        ['id'],
                                        ['name'],
                                        [area])

        # add to linking table
        db.insert_single('topic_to_area',
                         [topic_id, area_id[0][0]],
                         ['topic', 'topic_area'])

    # now insert prereqs
    for i in range(len(course_ids)):
        db.insert_single(
            'prerequisites',
            [0, topic_id, course_ids[i]],
            ['type', 'topic', 'course']
        )

    db.close()
    return jsonify({'status': 'ok'})


@create_topic.route('/get_topic_prereqs', methods=['GET'])
@at_least_role(UserRole.STAFF)
def get_chips():
    db.connect()
    topic_areas = db.select_columns('topic_areas', ['name'])
    prereqs = db.select_columns('courses', ['code'], ['prereq'], [1])

    chips_topic = {}
    for topic in topic_areas:
        chips_topic[topic[0]] = None

    chips_prereqs = {}
    for prereq in prereqs:
        chips_prereqs[prereq[0]] = None

    return jsonify({'status': 'ok', 'chipsTopic': chips_topic,
                    'chipsPrereqs': chips_prereqs})
