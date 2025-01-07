akd_dev=# CREATE DATABASE CRM_LAB;
CREATE DATABASE
akd_dev=# \dt
          List of relations
 Schema |   Name    | Type  |  Owner  
--------+-----------+-------+---------
 public | companies | table | akd_dev
 public | movies    | table | akd_dev
 public | people    | table | akd_dev
 public | roles     | table | akd_dev
 public | seats     | table | akd_dev
(5 rows)

akd_dev=# \l
                                                  List of databases
     Name     |  Owner  | Encoding | Locale Provider | Collate | Ctype | ICU Locale | ICU Rules |  Access privileges  
--------------+---------+----------+-----------------+---------+-------+------------+-----------+---------------------
 advanced_sql | akd_dev | UTF8     | libc            | C       | C     |            |           | 
 akd_dev      | akd_dev | UTF8     | libc            | C       | C     |            |           | 
 carmen       | akd_dev | UTF8     | libc            | C       | C     |            |           | 
 crm_lab      | akd_dev | UTF8     | libc            | C       | C     |            |           | 
 postgres     | akd_dev | UTF8     | libc            | C       | C     |            |           | 
 template0    | akd_dev | UTF8     | libc            | C       | C     |            |           | =c/akd_dev         +
              |         |          |                 |         |       |            |           | akd_dev=CTc/akd_dev
 template1    | akd_dev | UTF8     | libc            | C       | C     |            |           | =c/akd_dev         +
              |         |          |                 |         |       |            |           | akd_dev=CTc/akd_dev
 test_db      | akd_dev | UTF8     | libc            | C       | C     |            |           | 
(8 rows)

akd_dev=# \c crm_lab 
You are now connected to database "crm_lab" as user "akd_dev".
crm_lab=# CREATE TABLE companies;
ERROR:  syntax error at or near ";"
LINE 1: CREATE TABLE companies;
                              ^
crm_lab=# CREATE TABLE companies
crm_lab-# ;
ERROR:  syntax error at or near ";"
LINE 2: ;
        ^
crm_lab=# \dt
Did not find any relations.
crm_lab=# CREATE TABLE companies;
ERROR:  syntax error at or near ";"
LINE 1: CREATE TABLE companies;
                              ^
crm_lab=# CREATE TABLE companies (id SERIAL, name VARCHAR(20) );
CREATE TABLE
crm_lab=# CREATE TABLE employees (id SERIAL, first_name VARCHAR(20), last_name VARCHAR(20) employer_id INT));
ERROR:  syntax error at or near "employer_id"
LINE 1: ...AL, first_name VARCHAR(20), last_name VARCHAR(20) employer_i...
                                                             ^
crm_lab=# CREATE TABLE employees (id SERIAL, first_name VARCHAR(20), last_name VARCHAR(20), employer_id INT));
ERROR:  syntax error at or near ")"
LINE 1: ..._name VARCHAR(20), last_name VARCHAR(20), employer_id INT));
                                                                     ^
crm_lab=# CREATE TABLE employees (id SERIAL, first_name VARCHAR(20), last_name VARCHAR(20), employer_id INT);
CREATE TABLE
crm_lab=# ALTER TABLE companies ADD COLUMN company_id INT;
ALTER TABLE
crm_lab=# \d companies;
                                     Table "public.companies"
   Column   |         Type          | Collation | Nullable |                Default                
------------+-----------------------+-----------+----------+---------------------------------------
 id         | integer               |           | not null | nextval('companies_id_seq'::regclass)
 name       | character varying(20) |           |          | 
 company_id | integer               |           |          | 

crm_lab=# \d employees;
                                      Table "public.employees"
   Column    |         Type          | Collation | Nullable |                Default                
-------------+-----------------------+-----------+----------+---------------------------------------
 id          | integer               |           | not null | nextval('employees_id_seq'::regclass)
 first_name  | character varying(20) |           |          | 
 last_name   | character varying(20) |           |          | 
 employer_id | integer               |           |          | 

crm_lab=# INSERT INTO companies (name, company_id) VALUES ('Retro Action', 4)
crm_lab-# ALTER TABLE people ADD CONSTRAINT unique_seat_id UNIQUE (seat_id);
ERROR:  syntax error at or near "ALTER"
LINE 2: ALTER TABLE people ADD CONSTRAINT unique_seat_id UNIQUE (sea...
        ^
crm_lab=# ALTER TABLE companies ADD CONSTRAINT unique_company_id UNIQUE (company_id);
ALTER TABLE
crm_lab=# INSERT INTO companies (name, company_id) VALUES ('People and People', 4);
INSERT 0 1
crm_lab=# SELECT * FROM companies
crm_lab-# ;
 id |       name        | company_id 
----+-------------------+------------
  1 | People and People |          4
(1 row)

crm_lab=# INSERT INTO companies (name, company_id) VALUES ('Retro', 4);
ERROR:  duplicate key value violates unique constraint "unique_company_id"
DETAIL:  Key (company_id)=(4) already exists.
crm_lab=# ALTER TABLE employees ADD CONSTRAINT employer_id FOREIGN KEY (employer_id) REFERENCES companies (company_id);
ALTER TABLE
crm_lab=# \d empoloyees
Did not find any relation named "empoloyees".
crm_lab=# \d employees
                                      Table "public.employees"
   Column    |         Type          | Collation | Nullable |                Default                
-------------+-----------------------+-----------+----------+---------------------------------------
 id          | integer               |           | not null | nextval('employees_id_seq'::regclass)
 first_name  | character varying(20) |           |          | 
 last_name   | character varying(20) |           |          | 
 employer_id | integer               |           |          | 
Foreign-key constraints:
    "employer_id" FOREIGN KEY (employer_id) REFERENCES companies(company_id)

crm_lab=# INSERT INTO employees (first_name, last_name, employer_id) VALUES ('Retro', 3);
ERROR:  INSERT has more target columns than expressions
LINE 1: INSERT INTO employees (first_name, last_name, employer_id) V...
                                                      ^
crm_lab=# INSERT INTO employees (first_name, last_name, employer_id) VALUES ('Cora', 'Love', 3);
ERROR:  insert or update on table "employees" violates foreign key constraint "employer_id"
DETAIL:  Key (employer_id)=(3) is not present in table "companies".