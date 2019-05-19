CREATE TABLE clients_lockers
(
  client_id INTEGER PRIMARY KEY,
  client_name character varying(80) UNIQUE,
  locker_id INTEGER
);
ALTER TABLE clients_lockers
  OWNER TO cvmasters;
