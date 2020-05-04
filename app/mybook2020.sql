drop database IF EXISTS mybook2020;
create database mybook2020;
use mybook2020;

drop table IF EXISTS user;
drop table IF EXISTS friend_of;
drop table IF EXISTS creates_profile;
drop table IF EXISTS user_profile;
drop table IF EXISTS add_photo;
drop table IF EXISTS photo;
drop table IF EXISTS create_post;
drop table IF EXISTS cv_post;
drop table IF EXISTS posts;
drop table IF EXISTS content_editior;
drop table IF EXISTS UCG;
drop table IF EXISTS grouped;

/* derived from entities */
create table user (
    user_id int auto_increment not null,
    f_name varchar(15) not null,
    l_name varchar(15) not null,
    username varchar(15) not null,
    email varchar(35) not null,
    password varchar(300) not null,
    primary key(user_id)
);


create table user_profile (
    prof_id int not null,
    createdProf_date date,
    primary key(prof_id), 
    foreign key (prof_id) references user(user_id) on update cascade on delete cascade
);

create table photo (
    photo_id int auto_increment not null,
    photo_name varchar(50) not null,
    primary key(photo_id)
);

create table posts (
    post_id int auto_increment not null,
    createdPost_date date,
    post_type varchar(15) not null,
    primary key(post_id)
);

create table grouped (
    grp_id int auto_increment not null,
    grp_name varchar(20) not null,
    purpose varchar(50) not null,
    primary key(grp_id)
);

/* derived from relationships */
create table friend_of (
    user_id int not null,
    friend_id int not null,
    primary key(user_id),
    foreign key(user_id) references user(user_id) on update cascade on delete cascade,
    foreign key(friend_id) references user(user_id) on update cascade on delete restrict
);

create table add_photo (
    prof_id int not null,
    photo_id int not null,
    primary key(prof_id),
    foreign key (prof_id) references user_profile(prof_id) on update cascade on delete cascade
);

create table create_post (
    user_id int not null,
    post_id int not null,
    primary key(user_id),
    foreign key (user_id) references user(user_id) on update cascade on delete cascade
);

create table cv_post (
    user_id int not null,
    post_id int not null,
    primary key(user_id, post_id),
    foreign key (user_id) references user(user_id) on update cascade on delete cascade,
    foreign key (post_id) references posts(post_id) on update cascade on delete cascade
);

-- Ternary Relationship
create table UCG (
    user_id int,
    ce_id int,
    grp_id int,
    primary key(user_id, ce_id, grp_id),
    foreign key (user_id) references user(user_id) on update cascade on delete cascade,
    foreign key (ce_id) references user(user_id) on update cascade on delete cascade,
    foreign key (grp_id) references grouped(grp_id) on update cascade on delete cascade
);

-- LOAD DATA LOCAL INFILE 'C:/Users/Loretta/Desktop/MyBook/app/static/scripts/CSV Files/user_data.csv' INTO TABLE user FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (user_id, f_name, l_name, username, email, password);
-- LOAD DATA LOCAL INFILE 'C:/Users/Theda/Documents/GitHub/DB-2020/app/static/scripts/CSV Files/user_data_fake.csv' INTO TABLE user FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (user_id, f_name, l_name, username, email, password);
