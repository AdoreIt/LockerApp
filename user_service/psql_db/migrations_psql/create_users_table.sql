CREATE TABLE users
(
  user_id serial NOT NULL,
  user_name character varying(80) UNIQUE,
  locker_id INTEGER
);
ALTER TABLE users
  OWNER TO cvmasters;
