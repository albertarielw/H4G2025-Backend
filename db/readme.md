brew install postgresql
brew services start postgresql
psql -U postgres
CREATE USER h4g WITH PASSWORD 'h4g';
CREATE DATABASE h4g OWNER h4g;
psql -U h4g -d h4g -h localhost
