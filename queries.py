
INSERT_FORM = "INSERT INTO todo (id, title, message, deadline) \
               VALUES (DEFAULT, %(title)s, %(message)s, %(deadline)s) \
               RETURNING id"

ADD_TYPE = "INSERT INTO type (type) VALUES (%s)"
SELECT_TYPES = "SELECT type FROM type"

INSERT_TODO_ID_TYPE_ID = "INSERT INTO todo_type VALUES (%s, %s)"
SELECT_TYPE_ID = "SELECT id FROM type WHERE type = %s"

GROUP_BY_TYPES = "SELECT type.type, COUNT(todo_type.todo_id) AS total FROM todo_type \
                  INNER JOIN type ON todo_type.type_id = type.id \
                  INNER JOIN todo ON todo_type.todo_id = todo.id \
                  GROUP BY type.type"

SELECT_TODO = "SELECT \
                 todo.id AS id, \
                 todo.title AS title, \
                 todo.message AS message, \
                 todo.creation_time AS creation_time, \
                 todo.deadline AS deadline, \
                 type.type AS type \
               FROM todo_type \
               INNER JOIN todo ON todo.id = todo_type.todo_id \
               INNER JOIN type ON todo_type.type_id = type.id"

DELETE_TODO = "DELETE FROM todo WHERE id = %s"