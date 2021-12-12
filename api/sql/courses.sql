create table courses(
    id serial not null,
    title varchar not null,
    description varchar not null,
    hashtags varchar not null,
    type varchar not null,
    category varchar not null,
    exams integer not null,
    suscription varchar not null,
    location varchar not null,
    creator integer not null,
    PRIMARY KEY (id),
    FOREIGN KEY (type) REFERENCES courses_types(id),
    FOREIGN KEY (suscription) REFERENCES suscriptions(id),
    FOREIGN KEY (category) REFERENCES courses_categories(id),
    FOREIGN KEY (creator) REFERENCES users(id)
);