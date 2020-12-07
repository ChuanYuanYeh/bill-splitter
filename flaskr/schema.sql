drop table if exists user;
drop table if exists friend;

create table user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null,
    first_name text not null,
    last_name text not null
);

create table friend (
    id integer primary key autoincrement,
    user_id integer not null,
    full_name text not null,
    foreign key (user_id) references user (id)
);
