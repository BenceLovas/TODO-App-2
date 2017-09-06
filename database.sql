
ALTER TABLE IF EXISTS ONLY todo DROP CONSTRAINT IF EXISTS todo_pk CASCADE;
ALTER TABLE IF EXISTS ONLY type DROP CONSTRAINT IF EXISTS type_pk CASCADE;

DROP TABLE IF EXISTS todo;
DROP TABLE IF EXISTS type;
DROP TABLE IF EXISTS todo_type;

CREATE TABLE todo (
    id SERIAL NOT NULL,
    title VARCHAR(255) NOT NULL,
    message VARCHAR(255),
    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
    deadline TIMESTAMP
);

CREATE TABLE type (
    id SERIAL NOT NULL,
    type VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE todo_type (
    todo_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL
);

ALTER TABLE ONLY todo
    ADD CONSTRAINT todo_pk PRIMARY KEY (id);

ALTER TABLE ONLY type
    ADD CONSTRAINT type_pk PRIMARY KEY (id);

ALTER TABLE ONLY todo_type
    ADD CONSTRAINT fk_todo_type_id PRIMARY KEY (todo_id, type_id);

ALTER TABLE ONLY todo_type
    ADD CONSTRAINT fk_todo_id FOREIGN KEY (todo_id) REFERENCES todo(id) ON DELETE CASCADE;

ALTER TABLE ONLY todo_type
    ADD CONSTRAINT fk_type_id FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE;
