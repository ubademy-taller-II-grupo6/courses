create table collaborators(
    collaborator_id int not null,
    course_id integer not null,
    primary key (collaborator_id, course_id),
    FOREIGN KEY (collaborator_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);