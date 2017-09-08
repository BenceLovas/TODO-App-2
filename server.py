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
    todos = common.remaining_time(todos)
    todos = common.format_time(todos)

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
