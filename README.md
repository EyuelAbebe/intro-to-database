rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

## To construct the necessary database follow the following steps.
+ Create database called __tournament__.
    ```sh
    create database tournament
    ```
+ create the tables from tournament.sql Make sure to open psql from the directory that contians __tournament.sql__
    ```sh
    psql -d  tournament
    \i tournament.sql
    ```

## To Run test file
+ Navigate to folder containing __tournament_test.py__
    ```python
    python tournament_test.py
    ```