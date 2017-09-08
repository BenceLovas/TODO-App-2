from flask import Flask, request, render_template, redirect, url_for
import common
import database_manager
import queries
import datetime


app = Flask(__name__)

TO_FORMAT = ['deadline_year', 'deadline_month', 'deadline_day', 'deadline_hour', 'deadline_minute']


@app.route('/')
def index():
    date = datetime.datetime.now()
    types = database_manager.query_select(queries.SELECT_TYPES)
    types_list = common.values_from_list_of_dictionaries(types, 'type')
    total_by_type = database_manager.query_select(queries.GROUP_BY_TYPES)
    todos = database_manager.query_select(queries.SELECT_TODO)
    for i in todos:
        time_left = i['deadline'] - datetime.datetime.now()
        print("time_left", time_left)
        s = time_left.total_seconds()
        print("s", s)
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        if s < 0:
            i['time_left'] = "overdue"
        elif time_left.days > 0:
            if time_left.days == 1:
                i['time_left'] = "{} day left".format(time_left.days)
            else:
                i['time_left'] = "{} days left".format(time_left.days)
        elif hours > 0:
            if hours == 1:
                i['time_left'] = "{} hour left".format(int(hours))
            else:
                i['time_left'] = "{} hours left".format(int(hours))
        elif minutes > 0:
            if minutes == 1:
                i['time_left'] = "{} minute left".format(int(minutes))
            else:
                i['time_left'] = "{} minutes left".format(int(minutes))
        elif seconds > 0:
            if seconds == 1:
                i['time_left'] = "{} second left".format(int(second))
            else:
                i['time_left'] = "{} seconds left".format(int(seconds))
        
        
        # print("time left", i['time_left'])
        # print("type", type(i['time_left']))
        # print("days", i['time_left'].days)
    for i in todos:
        i['creation_time'] = i['creation_time'].strftime('%Y  /  %b / %-d - %H:%M')
    return render_template('index.html', date=date, types_list=types_list, total_by_type=total_by_type, todos=todos)


@app.route('/add-type', methods=['POST'])
def add_type():
    database_manager.query_modify(queries.ADD_TYPE, (request.form['new_type'], ))
    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save_todo():
    data = request.form.to_dict()
    data['deadline'] = common.add_0_before_numbers_under_10_convert_to_datetime(TO_FORMAT, data)
    todo_id_dict = database_manager.query_modify_returning(queries.INSERT_FORM, data)
    todo_id = todo_id_dict[0]['id']
    todo_type = request.form['type']
    type_id_dict = database_manager.query_select(queries.SELECT_TYPE_ID, (todo_type, ))
    type_id = type_id_dict[0]['id']
    database_manager.query_modify(queries.INSERT_TODO_ID_TYPE_ID, (todo_id, type_id))
    return redirect(url_for('index'))


@app.route('/<todo_id>/delete')
def delete_todo(todo_id):
    database_manager.query_modify(queries.DELETE_TODO, (todo_id, ))
    return redirect(url_for('index'))


@app.route('/type/<type_id>/delete')
def delete_type(type_id):
    print("type_id in delete: ", type_id)
    x = database_manager.query_select(queries.SELECT_TODO_BASED_ON_TYPE, (type_id, ))

    todo_id_list = []
    for i in x:
        todo_id_list.append(i['todo_id'])

    database_manager.query_modify(queries.DELETE_TYPE, (type_id, ))
    database_manager.query_modify(queries.DELETE_TODO_BASED_ON_TYPE, (todo_id_list, ))

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
