import psycopg2


def create_db(db_name: str, params: dict) -> None:
    """Создание баз данных и таблиц для сохранения данных о работодателе и его вакансиях"""
    conn = psycopg2.connect(db_name='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE employers_list (
            employer_id VARCHAR,
            employer_name VARCHAR(255) NOT NULL,
            employer_url VARCHAR,
            
            CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
            );
        """
    )

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute(
        """
        CREATE TABLE vacancies (
            vacancy_id VARCHAR(20),
            employer_id VARCHAR(20),
            vacancy_name VARCHAR NOT NULL,
            salary real,
            vacancy_url TEXT,
            
            CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id),
            CONSTRAINT fk_vacancies_employers FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
            );
        """
    )

    conn.commit()
    conn.close()

def save_data_to_db(employer_data: list[dict], vacancy_data: list[dict], db_name: str, params: dict) -> None:
    """Сохранение данных о работодателе и вакансиях в базу данных"""
    conn = psycopg2.connect(db_name=db_name, **params)

    with conn.cursor() as cur:
        for employer in employer_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, employer_url)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (employer['employer_id'], employer['employer_name'], ['employer_url']),
            )
        for vacancy in vacancy_data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary, vacancy_url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING vacancy_id
                """,
                (vacancy['vacancy_id'],
                 vacancy['employer_id'],
                 vacancy['vacancy_name'],
                 vacancy['salary'],
                 vacancy['vacancy_url'],
                 ),
            )

        conn.commit()
        conn.close()
