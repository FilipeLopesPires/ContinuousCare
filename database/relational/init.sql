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
  derived_password        BINARY(44),
  salt                    BINARY(44),
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
  specialities            varchar(200),
  company                 varchar(100)
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

create table pending_permission (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  medic_id                integer,
  foreign key (medic_id) references medic (medic_id),
  primary key (client_id, medic_id),
  duration                time
);
create table accepted_permission (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  medic_id                integer,
  foreign key (medic_id) references medic (medic_id),
  primary key (client_id, medic_id),
  begin_date              datetime,
  expiration_date         datetime
);
CREATE TABLE expired_permission (
  client_id               integer,
  foreign key (client_id) references client (client_id),
  medic_id                integer,
  foreign key (medic_id) references medic (medic_id),
  begin_date              datetime,
  primary key (client_id, medic_id, begin_date),
  end_date         datetime
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
  type                    enum("bracelet", "home_device"), -- TODO doesn't allow easy extensability
  brand                   varchar(30),
  model                   varchar(30),
  photo                   varchar(200)
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

/*
 * Useful to get the client id according to his username.
 * With this view several joins are separed
 */
CREATE VIEW client_username AS
    SELECT client.client_id AS client_id, user.username AS username
    FROM client JOIN user ON client.user_id = user.user_id;

/*
 * Useful to get the medic id according to his username.
 * With this view several joins are separed
 */
CREATE VIEW medic_username AS
    SELECT medic.medic_id AS medic_id, user.username AS username
    FROM medic JOIN user ON medic.user_id = user.user_id;

DELIMITER //

/*
 * Register a new client
 * Fails if for existing same:
 * - username
 * - phpn
 */
CREATE PROCEDURE insert_client (
    IN _username varchar(30),
    IN _derived_password BINARY(44),
    IN _salt BINARY(44),
    IN _full_name varchar(55),
    IN _email varchar(30),
    IN _health_number integer,
    IN _birth_date VARCHAR(10),
    IN _weight float,
    IN _height float,
    IN _additional_information varchar(100))
  BEGIN
    START TRANSACTION;
    -- Check duplicates
    IF EXISTS (SELECT * FROM user WHERE username = _username) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "username already in use.";
    ELSEIF EXISTS (SELECT * FROM client WHERE health_number = _health_number) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Health number already exists.";
    ELSEIF EXISTS (SELECT * FROM user WHERE username != _username AND email = _email) THEN
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Email already in use.";
    END IF;

    -- Insertions
    INSERT INTO user (username, derived_password, salt, full_name, email)
    VALUES (_username, _derived_password, _salt, _full_name, _email);

    INSERT INTO client (user_id, health_number, birth_date, weight, height, additional_information)
    VALUES (LAST_INSERT_ID(), _health_number, STR_TO_DATE(_birth_date, "%d-%m-%Y"), _weight, _height, _additional_information);

    -- Return client_id
    SELECT LAST_INSERT_ID();

    COMMIT;
  END //

/*
 * Register a new medic
 * Fails if for existing same:
 * - username
 */
CREATE PROCEDURE insert_medic (
    IN _username VARCHAR(30),
    IN _derived_password BINARY(44),
    IN _salt BINARY(44),
    IN _full_name VARCHAR(55),
    IN _email VARCHAR(30),
    IN _company VARCHAR(100),
    IN _specialities VARCHAR(200))
  BEGIN
    START TRANSACTION;
    -- Check duplicates
    IF EXISTS (SELECT * FROM user WHERE username = _username) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "username already exists";
    ELSEIF EXISTS (SELECT * FROM user WHERE username != _username AND email = _email) THEN
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Email already in use.";
    END IF;

    -- Insertions
    INSERT INTO user (username, derived_password, salt, full_name, email)
    VALUES (_username, _derived_password, _salt, _full_name, _email);

    INSERT INTO medic (user_id, company, specialities)
    VALUES (LAST_INSERT_ID(), _company, _specialities);

    -- Return medic_id
    SELECT LAST_INSERT_ID();

    COMMIT;
  END //


/*
 * Gets the information needed to check
 *  the credentials and also returns an integer
 *  according to the user type
 */
CREATE PROCEDURE get_credentials (
    IN _username varchar(30))
  BEGIN

    IF EXISTS (SELECT * FROM client_username WHERE username = _username) THEN
      SELECT 1, derived_password, salt
      FROM user
      WHERE username = _username;
    ELSEIF EXISTS (SELECT * FROM medic_username WHERE username = _username) THEN
      SELECT 2, derived_password, salt
      FROM user
      WHERE username = _username;
    END IF;

    SELECT NULL, NULL, NULL;
  END //

/*
 * Get information of the devices associated with a user
 * Contains:
 * - type, brand, model and photo
 * - authentication fields
 * - locations (in case of home devices, otherwise null)
 */
CREATE PROCEDURE get_all_client_devices (
    IN _username VARCHAR(30))
  BEGIN
    SELECT device.id,
           device.type_id,
           supported_device.type,
           supported_device.brand,
           supported_device.model,
           supported_device.photo,
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

/*
 * Associates a device with a user
 * Only allows one bracelet per client
 */
CREATE PROCEDURE insert_device (
    IN _username varchar(30),
    IN _type varchar(61),
    IN _latitude DOUBLE,
    IN _longitude DOUBLE)
 BEGIN
    DECLARE __supported_device_id, __client_id, __new_device_id INTEGER;
    DECLARE __new_device_type enum("bracelet", "home_device");

    START TRANSACTION;

    -- Id of the supported device according to the received parameters
    SELECT id, type INTO __supported_device_id, __new_device_type
    FROM supported_device
    WHERE concat(brand, " ", model) = _type;

    -- Fail if such supported device doesn't exist
    IF __supported_device_id IS NULL THEN
	    SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Not such supported device";
    END IF;

    -- Get id of the client
    SELECT client_id INTO __client_id
    FROM client_username
    WHERE username = _username;

    -- Fail if a bracelet type device is already associated with this client
    IF __new_device_type = "bracelet" AND
      EXISTS (SELECT *
              FROM (client_device JOIN device ON client_device.device_id = device.id)
                    JOIN supported_device ON device.type_id = supported_device.id
              WHERE client_device.client_id = __client_id AND supported_device.type = __new_device_type) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Client already has a bracelet associated";
    END IF;

    -- Insert the device
    INSERT INTO device (type_id)
    VALUES (__supported_device_id);

    -- Get the new device's id
    SET __new_device_id = LAST_INSERT_ID();

    -- Insert authentication fields
    INSERT INTO authentication_field (device_id, name, value)
    SELECT __new_device_id, tmp_authentication_fields.*
    FROM tmp_authentication_fields;

    -- Associate the device with the user
    INSERT INTO client_device (client_id, device_id)
    VALUES (__client_id, __new_device_id);

    -- Register location in case of a home device
    IF __new_device_type = "home_device" THEN
      INSERT INTO home_device_location (device_id, latitude, longitude)
      VALUES (__new_device_id, _latitude, _longitude);
    END IF;

    COMMIT;

    -- Return id of the new device
    select __new_device_id;
  END //


/*
 * Obtains information of all supported devices by the system
 * Information contained:
 * - type (bracelet or home device), brand, model
 * - metrics supported
 */
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

/*
 * Obtains the profile info of a user
 */
CREATE PROCEDURE get_user_info (
    IN _username VARCHAR(30))
  BEGIN
    IF EXISTS (SELECT * FROM client_username WHERE username = _username) THEN
      SELECT "client", client_id, full_name, email, health_number, birth_date, weight, height, additional_information
      FROM client JOIN user ON client.user_id = user.user_id
      WHERE username = _username;

    ELSEIF EXISTS (SELECT * FROM medic_username WHERE username = _username) THEN
      SELECT "medic", medic_id, full_name, email, company, specialities
      FROM medic JOIN user ON medic.user_id = user.user_id
      WHERE username = _username;
    ELSE
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There is no user with that username";
    END IF;

  END //

/*
 * Updates several fields of the client profile
 * Receives them all and overrites them, assuming
 *  that some are equal
 */
CREATE PROCEDURE update_client_info (
    IN _username varchar(30),
    IN _new_derived_password BINARY(44),
    IN _new_salt BINARY(44),
    IN _full_name varchar(55),
    IN _email varchar(30),
    IN _health_number integer,
    IN _birth_date VARCHAR(10),
    IN _weight float,
    IN _height float,
    IN _additional_information varchar(1000))
  BEGIN
    DECLARE __client_id INTEGER;

    START TRANSACTION;

    -- Get id of the client
    SELECT client_id INTO __client_id
    FROM client_username
    where username = _username;

    -- Fails if the new health number is already associated with another user
    IF EXISTS (SELECT *
               FROM client
               WHERE client_id != __client_id AND health_number = _health_number) THEN
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Health number already exists.";
    ELSEIF EXISTS (SELECT * FROM user WHERE username != _username AND email = _email) THEN
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Email already in use.";
    END IF;

    IF _new_derived_password IS NOT NULL THEN
      UPDATE user
      SET derived_password = _new_derived_password,
          salt = _new_salt
      WHERE username = _username;
    END IF;

    -- Update user related data
    UPDATE user
    SET full_name = _full_name,
        email = _email
    WHERE username = _username;

    -- Update client related data
    UPDATE client
    SET health_number = _health_number,
        birth_date = STR_TO_DATE(_birth_date, "%d-%m-%Y"),
        weight = _weight,
        height = _height,
        additional_information = _additional_information
    WHERE client_id = __client_id;

    COMMIT;
  END //

/*
 * Updates several fields of the medic profile
 * Receives them all and overrites them, assuming
 *  that some are equal
 */
CREATE PROCEDURE update_medic_info (
    IN _username varchar(30),
    IN _new_derived_password BINARY(44),
    IN _new_salt BINARY(44),
    IN _full_name varchar(55),
    IN _email varchar(30),
    IN _company varchar(100),
    IN _specialities varchar(200))
  BEGIN
    DECLARE __medic_id INTEGER;

    START TRANSACTION;

    -- Get id of the client
    SELECT medic_id INTO __medic_id
    FROM medic_username
    where username = _username;

    IF EXISTS (SELECT * FROM user WHERE username != _username AND email = _email) THEN
	  	SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Email already in use.";
    END IF;

    IF _new_derived_password IS NOT NULL THEN
      UPDATE user
      SET derived_password = _new_derived_password,
          salt = _new_salt
      where username = _username;
    END IF;

    -- Update user related data
    UPDATE user
    SET full_name = _full_name,
        email = _email
    WHERE username = _username;

    -- Update client related data
    UPDATE medic
    SET company = _company,
        specialities = _specialities
    WHERE medic_id = __medic_id;

    COMMIT;
  END //

/*
 * Register a sleep session
 * Fails if time interval overlaps a existing sleep session
 */
CREATE PROCEDURE insert_sleep_session (
  IN _username varchar(30),
  IN _day date,
  IN _duration time,
  IN _begin datetime,
  IN _end datetime)
  BEGIN
    DECLARE __client_id INTEGER;

    START TRANSACTION;

    -- Get client id
    SELECT client_id INTO __client_id
    FROM client_username
    where username = _username;

    -- Fails if time intervals of existing session with the new one overlap
    IF EXISTS(SELECT *
              FROM sleep_session
              WHERE ((begin < _begin AND begin > _begin)
                    OR
                     (end > _end AND end < _end)) AND client_id AND client_id = __client_id) THEN
	    SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "Intervals of several sleep session overlap";
    END IF;

    -- Insert sleep session
    INSERT INTO sleep_session (client_id, day, duration, begin, end)
    VALUES (__client_id, _day, _duration, _begin, _end);

    COMMIT;
  END //

/*
 * Obtains all sleep session within the received time interval
 */
CREATE PROCEDURE get_sleep_sessions (
  IN _username varchar(30),
  IN _begin date,
  IN _end date
)
  BEGIN

  IF _begin IS NULL AND _end IS NULL THEN
    SELECT sleep_session.day, sleep_session.begin, sleep_session.end, sleep_session.duration
    FROM sleep_session JOIN client_username ON sleep_session.client_id = client_username.client_id
    WHERE sleep_session.day >= _begin AND sleep_session.day <= _end AND client_username.username = _username;
  ELSEIF _begin IS NOT NULL THEN
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

/*
 * Obtains the usernames of all clients on the db
 */
CREATE PROCEDURE get_all_usernames ()
  BEGIN
    SELECT user.username
    FROM client JOIN user ON client.user_id = user.user_id;
  END //

/*
 * Updates authentication fields of a device
 */
CREATE PROCEDURE update_device (
    IN _username VARCHAR(30),
    IN _device_id INTEGER,
    IN _latitude DOUBLE,
    IN _longitude DOUBLE)
  BEGIN
    DECLARE __client_id INTEGER;

    DECLARE __auth_field_name VARCHAR(30);
    DECLARE __auth_field_value VARCHAR(500);

    DECLARE __done INT DEFAULT FALSE;
    DECLARE __cursor CURSOR FOR SELECT * FROM tmp_authentication_fields;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET __done = TRUE;

    START TRANSACTION;

    -- Get client id
    SELECT client_id INTO __client_id
    FROM client_username
    WHERE username = _username;

    -- Fail fail if the device with the received id is not associated with this client
    IF NOT EXISTS(SELECT *
                  FROM client_device
                  WHERE client_id = __client_id AND device_id = _device_id) THEN
	    SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "This users doesn't own the device with this id";
    END IF;

    OPEN __cursor;

    -- Iterate over the received authentication fields
    read_loop: LOOP
      FETCH __cursor INTO __auth_field_name, __auth_field_value;
      IF __done THEN
        LEAVE read_loop;
      END IF;

      -- If a new field is given that didn't exist before
      IF NOT EXISTS(SELECT * FROM authentication_field WHERE name = __auth_field_name
                                                         AND device_id = _device_id) THEN
	      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "One of the authentication fields received doen't exist";
      END IF;

      -- Update a specific authentication field (inside loop)
      UPDATE authentication_field
      SET authentication_field.value = __auth_field_value
      WHERE device_id = _device_id
        AND authentication_field.name = __auth_field_name;
    END LOOP;

    CLOSE __cursor;

    -- If latitude and longitude values were received and the device is a home device
    -- update those values
    IF _latitude IS NOT NULL AND _longitude IS NOT NULL AND (SELECT supported_device.type
                                                                 FROM device JOIN supported_device ON device.type_id = supported_device.id
                                                                 WHERE device.id = _device_id) = "home_device" THEN
      UPDATE home_device_location
      SET latitude = _latitude,
          longitude = _longitude
      WHERE device_id = _device_id;
    END IF;

    COMMIT;
  END //

/*
 * Deletes all information of a device
 */
CREATE PROCEDURE delete_device (
    IN _username VARCHAR(30),
    IN _device_id INTEGER)
  BEGIN
    START TRANSACTION;

    -- Fail if the user doesn't has the device with the received id associated with him
    IF NOT EXISTS(SELECT *
                  FROM client_device JOIN client_username ON client_device.client_id = client_username.client_id
                  WHERE client_username.username = _username AND device_id = _device_id) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "No such device associated with that user";
    END IF;

    -- Delete all information
    DELETE FROM home_device_location WHERE device_id = _device_id;
    DELETE FROM authentication_field WHERE device_id = _device_id;
    DELETE FROM client_device WHERE device_id = _device_id;
    DELETE FROM device WHERE id = _device_id;

    COMMIT;
  END //

/*
 * Moves any active permission that expired to the expired_permission table
 * Used at the beginning of any stored procedure that
 *  operates over the permissions
 */
CREATE PROCEDURE update_permissions (
    IN _client VARCHAR(30),
    IN _medic VARCHAR(30),
    OUT __client_id INTEGER,
    OUT __medic_id INTEGER)
  BEGIN
    START TRANSACTION;

    -- Retrieve client id
    SELECT client_id INTO __client_id
    FROM client_username
    WHERE username = _client;

    -- Retrieve medic id
    SELECT medic_id INTO __medic_id
    FROM medic_username
    WHERE username = _medic;

    -- Move accepted that had expired to expired_permission
    INSERT INTO expired_permission
    SELECT *
    FROM accepted_permission
    WHERE client_id = __client_id
      AND medic_id = __medic_id
      AND expiration_date < NOW();

    -- Delete form the active the expired permission
    DELETE FROM accepted_permission
    WHERE client_id = __client_id
      AND medic_id = __medic_id
      AND expiration_date < NOW();

    COMMIT;
  END //

/*
 * Creates a pending permission
 * Used by the medic
 * Fails if a pending permission already exists
 */
CREATE PROCEDURE request_permission (
    IN _medic VARCHAR(30),
    IN _client VARCHAR(30),
    IN _health_number INTEGER,
    IN _duration time)
  BEGIN
    DECLARE __client_id, __medic_id, __email VARCHAR(30);
    DECLARE __full_name VARCHAR(55);
    DECLARE __health_number INTEGER;

    IF _client IS NULL THEN
      SELECT username, full_name, health_number INTO _client, __full_name, __health_number
      FROM user JOIN client ON user.user_id = client.user_id
      WHERE health_number = _health_number;

      IF _client IS NULL THEN
        SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no patient with the given health number.";
      END IF;
    ELSE
      IF NOT EXISTS(SELECT * FROM client_username WHERE username = _client) THEN
        SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no patient with the given username.";
      END IF;

      SELECT full_name, email, health_number INTO __full_name, __email,  __health_number
      FROM user JOIN client ON user.user_id = client.user_id
      WHERE username = _client;
    END IF;

    CALL update_permissions(_client, _medic, __client_id, __medic_id);

    START TRANSACTION;

    -- Fail if a pending permission already exists
    IF EXISTS (SELECT *
               FROM pending_permission
               WHERE client_id = __client_id
                 AND medic_id = __medic_id) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "A permission request already exists";
    ELSE
      -- Insert otherwise
      INSERT INTO pending_permission VALUES (__client_id, __medic_id, _duration);

    END IF;

    SELECT _client, __full_name, __email, __health_number;

    COMMIT;
  END //

/*
 * The client grants permission to the medic
 * A accepted permission is created
 * Fails if an accepted permission already exists
 */
CREATE PROCEDURE grant_permission (
    IN _client VARCHAR(30),
    IN _medic VARCHAR(30),
    IN _duration TIME)
  BEGIN
    DECLARE __client_id, __medic_id VARCHAR(30);

    IF NOT EXISTS (SELECT * FROM medic_username where username = _medic) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no medic with the given username";
    END IF;

    CALL update_permissions(_client, _medic, __client_id, __medic_id);

    START TRANSACTION;

    -- If an accepted permision doesn't exits
    IF NOT EXISTS (SELECT *
                   FROM accepted_permission
                   WHERE client_id = __client_id
                     AND medic_id = __medic_id) THEN
      -- Insert
      INSERT INTO accepted_permission VALUES (__client_id, __medic_id, NOW(), ADDTIME(NOW(), _duration));
    ELSE
      -- Otherwise fail
      UPDATE accepted_permission
      SET expiration_date = ADDTIME(expiration_date, _duration)
      WHERE client_id = __client_id
        AND medic_id = __medic_id;
    END IF;

    SELECT full_name, email, company
    FROM user JOIN medic ON user.user_id = medic.user_id
    WHERE username = _medic;

    COMMIT;
  END //

/*
 * A client accepts a request for permission
 * Fails if there is no requests
 */
CREATE PROCEDURE accept_permission (
    IN _client VARCHAR(30),
    IN _medic VARCHAR(30))
  BEGIN
    DECLARE __client_id, __medic_id VARCHAR(30);
    DECLARE __pending_duration TIME;

    IF NOT EXISTS (SELECT * FROM medic_username where username = _medic) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no medic with the given username";
    END IF;

    CALL update_permissions(_client, _medic, __client_id, __medic_id);

    START TRANSACTION;

    -- Fail if there is no requests
    IF NOT EXISTS(SELECT *
                  FROM pending_permission
                  WHERE client_id = __client_id
                    AND medic_id = __medic_id) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "No permission to accept";
    ELSE

      -- Get the duration of the request
      SELECT duration INTO __pending_duration
      FROM pending_permission
      WHERE client_id = __client_id
        AND medic_id = __medic_id;

      -- If an accepted permission exists
      IF EXISTS (SELECT *
                 FROM accepted_permission
                 WHERE client_id = __client_id
                   AND medic_id = __medic_id) THEN
        -- Increment the duration of the request
        UPDATE accepted_permission
        SET expiration_date = ADDTIME(expiration_date, __pending_duration)
        WHERE client_id = __client_id
          AND medic_id = __medic_id;
      ELSE
        -- Else Create the accepted permission
        INSERT INTO accepted_permission
        VALUES (__client_id, __medic_id, NOW(), ADDTIME(NOW(), __pending_duration));
      END IF;

      -- Delete the request
      DELETE FROM pending_permission
      WHERE client_id = __client_id
        AND medic_id = __medic_id;
    END IF;

    COMMIT;
  END //

/*
 * Allows a client to remove and accepted permission
 */
CREATE PROCEDURE remove_accepted_permission (
    IN _client VARCHAR(30),
    IN _medic VARCHAR(30))
  BEGIN
    DECLARE __client_id, __medic_id VARCHAR(30);

    IF NOT EXISTS (SELECT * FROM medic_username where username = _medic) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no medic with the given username";
    END IF;

    CALL update_permissions(_client, _medic, __client_id, __medic_id);

    START TRANSACTION;

    -- If no accepted permission exits fails
    IF NOT EXISTS (SELECT *
                   FROM accepted_permission
                   WHERE client_id = __client_id
                     AND medic_id = __medic_id) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "No accepted permission to delete";
    ELSE
      INSERT INTO expired_permission
      SELECT *
      FROM accepted_permission
      WHERE client_id = __client_id
        AND medic_id = __medic_id
        AND expiration_date < NOW();

      -- Otherwise removes it
      DELETE FROM accepted_permission
      WHERE client_id = __client_id
        AND medic_id = __medic_id;
    END IF;

    COMMIT;
  END //

/*
 * Used by
 * - Client to reject permission
 * - Medic to remove requests
 */
CREATE PROCEDURE delete_permission (
    IN _client VARCHAR(30),
    IN _medic VARCHAR(30))
  BEGIN
    DECLARE __client_id, __medic_id VARCHAR(30);

    IF NOT EXISTS (SELECT * FROM client_username WHERE username = _client) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no patient with the given username.";
    ELSEIF NOT EXISTS (SELECT * FROM medic_username WHERE username = _medic) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no medic with the given username.";
    END IF;

    CALL update_permissions(_client, _medic, __client_id, __medic_id);

    START TRANSACTION;

    -- Fail if there is no request for permission
    IF NOT EXISTS(SELECT *
                  FROM pending_permission
                  WHERE client_id = __client_id
                    AND medic_id = __medic_id) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "No permission to reject";
    ELSE
      -- Delete it otherwise
      DELETE FROM pending_permission
      WHERE client_id = __client_id
        AND medic_id = __medic_id;
    END IF;

    COMMIT;
  END //

/*
 * Function executed whenever a medic accesses a client's data
 */
CREATE PROCEDURE has_permission (
    IN _medic VARCHAR(30),
    IN _client VARCHAR(30))
  BEGIN
    DECLARE __client_id, __medic_id VARCHAR(30);

    IF NOT EXISTS (SELECT * FROM client_username where username = _client) THEN
      SIGNAL SQLSTATE '03000' SET MESSAGE_TEXT = "There's no patient with the given username.";
    END IF;

    CALL update_permissions(_client, _medic, __client_id, __medic_id);

    -- If a permission is active, has permission
    IF EXISTS (SELECT *
               FROM accepted_permission
               WHERE client_id = __client_id
                 AND medic_id = __medic_id) THEN
      SELECT TRUE;
    ELSE
      SELECT FALSE;
    END IF;

  END //

/*
 * Similar as the stored procedure update_permissions
 *  however just updates permissions related to a single user
 */
CREATE PROCEDURE update_permissions_user (
    IN _user VARCHAR(30))
  BEGIN
    DECLARE __user_id INTEGER;

    SELECT medic_id INTO __user_id
    FROM medic JOIN user ON medic.user_id = user.user_id
    WHERE username = _user;

    IF __user_id IS NULL THEN
      SELECT client_id INTO __user_id
      FROM client JOIN user ON client.user_id = user.user_id
      WHERE username = _user;

      INSERT INTO expired_permission
      SELECT *
      FROM accepted_permission
      WHERE client_id = __user_id
        AND expiration_date < NOW();

      DELETE FROM accepted_permission
      WHERE medic_id = __user_id
        AND expiration_date < NOW();

      SELECT FALSE;
    ELSE
      INSERT INTO expired_permission
      SELECT *
      FROM accepted_permission
      WHERE medic_id = __user_id
        AND expiration_date < NOW();

      DELETE FROM accepted_permission
      WHERE medic_id = __user_id
        AND expiration_date < NOW();

      SELECT TRUE;
    END IF;

  END //

/*
 * Obtains all pending permissions from a user displaying information of the associated medic/client
 */
CREATE PROCEDURE get_pending_permissions (
    IN _user VARCHAR(30),
    IN _is_medic BOOLEAN)
  BEGIN
    -- If the user is a medic
    IF _is_medic THEN
      SELECT TIME_FORMAT(pending_permission.duration, "%H:%i"),
             user.username,
             user.full_name,
             user.email,
             client.health_number
      FROM ((pending_permission JOIN medic_username ON medic_username.medic_id = pending_permission.medic_id)
      JOIN client ON client.client_id = pending_permission.client_id)
      JOIN user on user.user_id = client.user_id
      WHERE medic_username.username = _user;
    ELSE
      -- Else is a client
      SELECT TIME_FORMAT(pending_permission.duration, "%H:%i"),
             user.username,
             user.full_name,
             user.email,
             medic.company
      FROM ((pending_permission JOIN client_username ON client_username.client_id = pending_permission.client_id)
      JOIN medic ON medic.medic_id = pending_permission.medic_id)
      JOIN user on user.user_id = medic.user_id
      WHERE client_username.username = _user;
    END IF;
  END //

/*
 * Obtains all accepted permissions from a user displaying information of the associated medic/client
 */
CREATE PROCEDURE get_accepted_permissions (
    IN _user VARCHAR(30),
    IN _is_medic BOOLEAN)
  BEGIN
    -- If the user is a medic
    IF _is_medic THEN
      SELECT TIME_FORMAT(TIMEDIFF(accepted_permission.expiration_date, NOW()), "%H:%i"),
             user.username,
             user.full_name,
             user.email,
             client.health_number
      FROM ((accepted_permission JOIN medic_username ON medic_username.medic_id = accepted_permission.medic_id)
      JOIN client ON client.client_id = accepted_permission.client_id)
      JOIN user on user.user_id = client.user_id
      WHERE medic_username.username = _user;
    ELSE
      -- Else is a client
      SELECT TIME_FORMAT(TIMEDIFF(accepted_permission.expiration_date, NOW()), "%H:%i"),
             user.username,
             user.full_name,
             user.email,
             medic.company
      FROM ((accepted_permission JOIN client_username ON client_username.client_id = accepted_permission.client_id)
      JOIN medic ON medic.medic_id = accepted_permission.medic_id)
      JOIN user on user.user_id = medic.user_id
      WHERE client_username.username = _user;
    END IF;

  END //

CREATE PROCEDURE get_expired_permissions (
    IN _user VARCHAR(30),
    IN _is_medic BOOLEAN)
  BEGIN
    -- If the user is a medic
    IF _is_medic THEN
      SELECT DATE_FORMAT(expired_permission.begin_date, "%Y-%m-%d %H:%i:%s"),
             DATE_FORMAT(expired_permission.end_date, "%Y-%m-%d %H:%i:%s"),
             user.username,
             user.full_name,
             user.email,
             client.health_number
      FROM ((expired_permission JOIN medic_username ON medic_username.medic_id = expired_permission.medic_id)
      JOIN client ON client.client_id = expired_permission.client_id)
      JOIN user on user.user_id = client.user_id
      WHERE medic_username.username = _user;
    ELSE
      -- Else is a client
      SELECT DATE_FORMAT(expired_permission.begin_date, "%Y-%m-%d %H:%i:%s"),
             DATE_FORMAT(expired_permission.end_date, "%Y-%m-%d %H:%i:%s"),
             user.username,
             user.full_name,
             user.email,
             medic.company
      FROM ((expired_permission JOIN client_username ON client_username.client_id = expired_permission.client_id)
      JOIN medic ON medic.medic_id = expired_permission.medic_id)
      JOIN user on user.user_id = medic.user_id
      WHERE client_username.username = _user;
    END IF;

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

INSERT INTO supported_device (type, brand, model, photo) values ("bracelet", "FitBit", "Charge 3", "https://ss7.vzw.com/is/image/VerizonWireless/fitbit-charge3-graphite-black-fb409gmbk-a?$png8alpha256$&hei=410"),
                                                         ("home_device", "Foobot", "", "https://cdn.shopify.com/s/files/1/0008/7330/0029/products/foobot_x700.jpg?v=1528342886");

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
