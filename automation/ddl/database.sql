CREATE DATABASE Pizza;

-- this can't be more obvious, but change the password here..
CREATE USER Pizza_Owner WITH PASSWORD 'password';

-- this can't be more obvious, but change the password here..
ALTER ROLE Pizza_Owner SET client_encoding TO 'utf8';
ALTER ROLE Pizza_Owner SET default_transaction_isolation TO 'read committed';
ALTER ROLE Pizza_Owner SET timezone TO 'UTC';

-- for the privileged few.
GRANT ALL PRIVILEGES ON DATABASE Pizza TO Pizza_Owner;