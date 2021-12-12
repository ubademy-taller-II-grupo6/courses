CREATE TABLE users(
                    id serial,
                    name varchar NOT NULL,
                    lastname varchar NOT NULL,
                    email varchar unique NOT NULL,
                    blocked BOOLEAN,
                    primary key (id)
)