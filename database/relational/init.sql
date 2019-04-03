CREATE DATABASE db;
USE db;
SET default_storage_engine=InnoDB; --default after and including MySQL 5.5.5

-- USERS

CREATE USER pi2019cc_flaskapp IDENTIFIED BY "T)[-keLSh.9UFZcN58.+";
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE
  ON db.*
  TO pi2019cc_flaskapp;

-- DDL

create table user (
  user_id                 integer     primary key auto_increment ,
-- PRIMARY KEY
  username                varchar(30) unique,
  password                char(88),
  full_name               varchar(55),
  email                   varchar(30)
);

create table client (
  client_id               integer       primary key auto_increment,
-- PRIMARY KEY
  user_id                 integer,
  foreign key (user_id) references user (user_id),
  health_number           integer       unique,
  birth_date              date,
  weight                  float(24),
  height                  float(24),
  additional_information  varchar(1000),
);
--create index client_health_num_idx on client (health_number);

create table medic (
  medic_id                integer       primary key auto_increment,
-- PRIMARY KEY
  user_id                 integer,
  foreign key (user_id) references user (user_id),
  specialisation          varchar(30),
  company                 varchar(30)
);

create table authentication (
  client_id               integer   primary key,
  foreign key (client_id) references user (user_id),
-- PRIMARY KEY
  expiration_date         datetime,
  acess_token             varchar(300)
);

create table pending_permissions (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  medic_id                integer,
  foreign key (medic_id) references medic (medic_id),
  primary key (client_id, medic_id),
  begin_date              datetime,
  end_date                datetime
);
create table active_permissions (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  medic_id                integer,
  foreign key (medic_id) references medic (medic_id),
  primary key (client_id, medic_id),
  begin_date              datetime,
  expiration_date         datetime
);
create table expired_permissions (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  medic_id                integer,
  foreign key (medic_id) references medic (medic_id),
  begin_date              datetime,
  primary key (client_id, medic_id, begin_date),
  end_date                datetime
);
--drop index `PRIMARY` on expired_permissions;
--create index exp_perm_client_idx on expired_permissions (client_id);
--create index exp_perm_medic_idx on expired_permissions (client_id);

create table status_type (
  id                      integer       primary key auto_increment,
  name                    varchar(30)
);

create table personal_status (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  type                    integer,
  foreign key (type) references status_type (id),
  time                    datetime,
  primary key (client_id, type, time)
);
--drop index `PRIMARY` on personal_status;
--create index pers_stat_client_idx on personal_status (client_id);

create table supported_device (
  id                      integer       primary key auto_increment,
-- PRIMARY KEY
  type                    enum("bracelet", "home_device"), -- TODO doesn't allow extensability
  brand                   varchar(30),
  model                   varchar(30)
);

create table device (
  id                      integer       primary key auto_increment,
-- PRIMARY KEY
  type_id                 integer,
  foreign key (type_id) references supported_device (id),
  acess_token             varchar(300)
);

create table client_device (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  device_id               integer,
  foreign key (device_id) references device (id),
  primary key (client_id, device_id)
);

create table metric (
  id                      integer       primary key auto_increment,
-- PRIMARY KEY
  name                    varchar(30),
  unit                    varchar(10),
  type                    enum("environment", "health_status")
);

create table supported_metric (
  metric_id               integer,
  foreign key (metric_id) references metric (id),
  device_id               integer,
  foreign key (device_id) references supported_device (id),
  primary key(metric_id, device_id)
);

-- PROGRAMMING

CREATE VIEW client_username AS
    SELECT client.client_id AS client_id, user.username AS username
    FROM client JOIN user ON client.user_id = user.user_id;

DELIMITER //

CREATE PROCEDURE insert_client (
    IN _username varchar(30),
    IN _password char(88),
    IN _full_name varchar(55),
    IN _email varchar(30),
    IN _health_number integer,
    IN _birth_date date,
    IN _weight float(24),
    IN _height float(24),
    IN _additional_information varchar(100))
  BEGIN
    -- Verifications
    IF EXISTS (SELECT * FROM user WHERE username = _username) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "username already exists";
    ELSEIF EXISTS (SELECT * FROM client WHERE health_number = _health_number) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "health number already exists";
    END IF;

    -- Insertions
    INSERT INTO user (username, password, full_name, email) 
    VALUES (_username, _password, _full_name, _email);
    
    INSERT INTO client (user_id, health_number, birth_date, weight, height, additional_information)
    VALUES (LAST_INSERT_ID(), _health_number, _birth_date, _weight, _height, _additional_information);
    
    -- Return client_id
    SELECT LAST_INSERT_ID();
  END //

CREATE PROCEDURE verify_credentials (
    IN _username varchar(30),
    IN _password char(88))
  BEGIN
    SELECT EXISTS(SELECT * FROM user WHERE username = _username and passoword = _password);
  END //

CREATE PROCEDURE get_all_client_devices (
    IN _username VARCHAR(30))
  BEGIN
    SELECT device.id, device.type_id, device.acess_token
    FROM (device JOIN client_device ON device.id = client_device.device_id)
         JOIN client_username ON client_username.client_id = client_device.client_id
    WHERE client_username.username = _username;
  END //

CREATE PROCEDURE insert_device (
    IN _username varchar(30),
    IN _type_id INTEGER,
    IN _acess_token VARCHAR(300))
  BEGIN
    DECLARE __client_id, __new_device_id INTEGER;

    SELECT client_id INTO __client_id
    FROM client_username
    WHERE username = _username;

    INSERT INTO device (type_id, acess_token)
    VALUES (_type_id, _acess_token);

    SET __new_device_id = LAST_INSERT_ID();

    INSERT INTO client_device (client_id, device_id)
    VALUES (__client_id, __new_device_id);

    select __new_device_id;
  END //


CREATE PROCEDURE get_all_supported_devices ()
  BEGIN
    SELECT supported_device.id,
           supported_device.type,
           supported_device.brand,
           supported_device.model,
           metric.name,
           metric.unit
    FROM (supported_device JOIN supported_metric
         ON supported_device.id = supported_metric.device_id) JOIN
           metric ON supported_metric.metric_id = metric.id;
  END //

CREATE PROCEDURE get_user_info (
    IN _username VARCHAR(30))
  BEGIN
    SELECT client_id, full_name, email, health_number, birth_date, weight, height
    FROM client JOIN user ON client.user_id = user.user_id
    WHERE username = _username;
  END //

CREATE PROCEDURE update_user_info (
    IN _username varchar(30),
    IN _password char(88),
    IN _full_name varchar(55),
    IN _email varchar(30),
    IN _health_number integer,
    IN _birth_date date,
    IN _weight float(24),
    IN _height float(24),
    IN _additional_information varchar(1000))
  BEGIN
    DECLARE __client_id INTEGER;
    
    SELECT client_id INTO __client_id
    FROM client_username
    where username = _username;
    
    IF EXISTS (SELECT *
               FROM client
               WHERE client_id != __client_id AND health_number = _health_number) THEN
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "health number already exists";
    END IF;
    
    UPDATE user
    SET password = _password,
        full_name = _full_name,
        email = _email
    WHERE username = _username;
    
    UPDATE client
    SET health_number = _health_number,
        birth_date = _birth_date,
        weight = _weight,
        height = _height,
        additional_information = _additional_information
    WHERE client_id = __client_id;
  END //

CREATE PROCEDURE get_environment_metrics ()
  BEGIN
    SELECT name
    FROM metric
    where type = "environment";
  END //

CREATE PROCEDURE get_health_status ()
  BEGIN
    SELECT *
    FROM metric
    WHERE type = "health_status";
  END //

DELIMITER ;

