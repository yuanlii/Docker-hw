FROM postgres:9.6

ENV POSTGRES_PASSWORD 12345

ADD init.sql /docker-entrypoint-initdb.d/init.sql
