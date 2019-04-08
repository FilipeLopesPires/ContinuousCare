USE db;

-- USERS

CREATE USER pi2019cc_flaskapp IDENTIFIED BY "T)[-keLSh.9UFZcN58.+";
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE, CREATE TEMPORARY TABLES
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
  weight                  float,
  height                  float,
  additional_information  varchar(1000)
);
-- create index client_health_num_idx on client (health_number);

create table medic (
  medic_id                integer       primary key auto_increment,
-- PRIMARY KEY
  user_id                 integer,
  foreign key (user_id) references user (user_id),
  specialisation          varchar(30),
  company                 varchar(30)
);

/*
create table authentication (
  client_id               integer   primary key,
  foreign key (client_id) references user (user_id),
-- PRIMARY KEY
  expiration_date         datetime,
  acess_token             varchar(300)
);
*/

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
-- drop index `PRIMARY` on expired_permissions;
-- create index exp_perm_client_idx on expired_permissions (client_id);
-- create index exp_perm_medic_idx on expired_permissions (client_id);

create table status_type (
  id                      integer       primary key auto_increment,
  name                    varchar(30)
);

create table sleep_session (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  day                     date,
  begin                   datetime,
  primary key (client_id, day, begin),
-- PRIMARY KEY
  end                     datetime,
  duration                time
);

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
  foreign key (type_id) references supported_device (id)
);

create table authentication_field (
  device_id               integer,
  foreign key (device_id) references device (id),
  name                    varchar(30),
  primary key (device_id, name),
-- PRIMARY KEY
  value                   varchar(500)
);

create table home_device_location (
  device_id               integer       primary key,
  foreign key (device_id) references device (id),
-- PRIMARY KEY
  latitude                double,
  longitude               double
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
  unit                    varchar(20)
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
    IN _weight float,
    IN _height float,
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
    SELECT EXISTS(SELECT * FROM user WHERE username = _username and password = _password);
  END //

CREATE PROCEDURE get_all_client_devices (
    IN _username VARCHAR(30))
  BEGIN
    SELECT device.id,
           device.type_id,
           supported_device.type,
           supported_device.brand,
           supported_device.model,
           authentication_field.name,
           authentication_field.value,
           home_device_location.latitude,
           home_device_location.longitude
    FROM ((((device JOIN client_device ON device.id = client_device.device_id)
         JOIN client_username ON client_username.client_id = client_device.client_id)
         JOIN supported_device ON supported_device.id = device.type_id)
         JOIN authentication_field ON authentication_field.device_id = device.id)
         LEFT JOIN home_device_location ON home_device_location.device_id = device.id
    WHERE client_username.username = _username;
  END //

CREATE PROCEDURE insert_device (
    IN _username varchar(30),
    IN _type varchar(61), 
    IN _latitude DOUBLE,
    IN _longitude DOUBLE)
 BEGIN
    DECLARE __supported_device_id, __client_id, __new_device_id INTEGER;
    DECLARE __new_device_type enum("bracelet", "home_device");

    SELECT id, type INTO __supported_device_id, __new_device_type
    FROM supported_device
    WHERE concat(brand, " ", model) = _type;

    SELECT client_id INTO __client_id
    FROM client_username
    WHERE username = _username;

    IF __new_device_type = "bracelet" AND
      EXISTS (SELECT *
              FROM (client_device JOIN device ON client_device.device_id = device.id)
                    JOIN supported_device ON device.type_id = supported_device.id
              WHERE client_device.client_id = __client_id AND supported_device.type = __new_device_type) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Client already has a bracelet associated";
    END IF;

    INSERT INTO device (type_id)
    VALUES (__supported_device_id);

    SET __new_device_id = LAST_INSERT_ID();

    INSERT INTO authentication_field (device_id, name, value)
    SELECT __new_device_id, tmp_authentication_fields.*
    FROM tmp_authentication_fields;

    INSERT INTO client_device (client_id, device_id)
    VALUES (__client_id, __new_device_id);

    IF __new_device_type = "home_device" THEN
      INSERT INTO home_device_location (device_id, latitude, longitude)
      VALUES (__new_device_id, _latitude, _longitude);
    END IF;

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
    IN _weight float,
    IN _height float,
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

CREATE PROCEDURE insert_sleep_session (
  IN _username varchar(30),
  IN _day date,
  IN _duration time,
  IN _begin datetime,
  IN _end datetime)
  BEGIN
    DECLARE __client_id INTEGER;

    SELECT client_id INTO __client_id
    FROM client_username
    where username = _username;

    IF EXISTS(SELECT *
              FROM sleep_session
              WHERE ((begin < _begin AND begin > _begin)
                    OR
                     (end > _end AND end < _end)) AND client_id AND client_id = __client_id) THEN
	    SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Intervals of several sleep session overlap";
    END IF;

    INSERT INTO sleep_session (client_id, day, duration, begin, end)
    VALUES (__client_id, _day, _duration, _begin, _end);

  END //

CREATE PROCEDURE get_sleep_sessions (
  IN _username varchar(30),
  IN _begin date,
  IN _end date
)
  BEGIN

  IF _begin = NULL AND _end = NULL THEN
    SELECT sleep_session.day, sleep_session.begin, sleep_session.end, sleep_session.duration
    FROM sleep_session JOIN client_username ON sleep_session.client_id = client_username.client_id
    WHERE sleep_session.day >= _begin AND sleep_session.day <= _end AND client_username.username = _username;
  ELSEIF _begin != NULL THEN
    SELECT sleep_session.day, sleep_session.begin, sleep_session.end, sleep_session.duration
    FROM sleep_session JOIN client_username ON sleep_session.client_id = client_username.client_id
    WHERE sleep_session.day >= _begin AND client_username.username = _username;
  ELSE
    SELECT sleep_session.day, sleep_session.begin, sleep_session.end, sleep_session.duration
    FROM sleep_session JOIN client_username ON sleep_session.client_id = client_username.client_id
    WHERE client_username.username = _username
    ORDER BY begin DESC
    LIMIT 1;
  END IF;

  END //

CREATE PROCEDURE get_all_usernames ()
  BEGIN
    SELECT user.username
    FROM client JOIN user ON client.user_id = user.user_id;
  END //

DELIMITER ;

-- INSERT DATA

INSERT INTO metric (name, unit) values ("Heart Rate", "bpm"),
                                       ("Sleep", "hours"),
                                       ("Calories", "kcal"),
                                       ("Sedentary time", "minutes"),
                                       ("Lightly Active time", "minutes"),
                                       ("Fairly Active time", "minutes"),
                                       ("Very Active time", "minutes"),
                                       ("Steps", "units"),
                                       -- FitBit ^^
                                       ("Particulate Matter (pm)", "µg/m3"),
                                       ("Temperature", "Celcius"),
                                       ("Humidity", "PC"),
                                       ("Carbon dioxide", "ppm"),
                                       ("Volatile Organic Compound", "ppb"),
                                       ("Relative polution", "Percentage (%)");
                                       -- Foobot ^^

INSERT INTO supported_device (type, brand, model) values ("bracelet", "FitBit", "Charge 3"),
                                                         ("home_device", "Foobot", "");

INSERT INTO supported_metric (metric_id, device_id) values (1 , 1),
                                                           (2 , 1),
                                                           (3 , 1),
                                                           (4 , 1),
                                                           (5 , 1),
                                                           (6 , 1),
                                                           (7 , 1),
                                                           (8 , 1),
                                                           (9 , 2),
                                                           (10, 2),
                                                           (11, 2),
                                                           (12, 2),
                                                           (13, 2),
                                                           (14, 2);
