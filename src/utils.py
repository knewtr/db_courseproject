import psycopg2


def create_db(db_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о работодателе и его вакансиях"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS employers_list (
            employer_id VARCHAR PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL,
            company_url VARCHAR
            );
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id VARCHAR(20) PRIMARY KEY,
            employer_id VARCHAR(20) NOT NULL,
            vacancy_name VARCHAR NOT NULL,
            salary REAL,
            vacancy_url TEXT,
            
            CONSTRAINT fk_vacancies_employers FOREIGN KEY (employer_id) REFERENCES employers_list(employer_id)
            );
        """
        )

    conn.close()


def save_data_to_db(
    employer_data: list[dict], vacancy_data: list[dict], db_name: str, params: dict
) -> None:
    """Сохранение данных о работодателе и вакансиях в таблицы"""
    conn = None
    try:
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for employer in employer_data:
                cur.execute(
                    """
                    INSERT INTO employers_list (employer_id, employer_name, company_url)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        employer["employer_id"],
                        employer["employer_name"],
                        employer["company_url"],
                    ),
                )
            for vacancy in vacancy_data:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        vacancy["vacancy_id"],
                        vacancy.get("employer_id"),
                        vacancy["vacancy_name"],
                        vacancy["salary"],
                        vacancy.get("vacancy_url"),
                    ),
                )
            print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка сохранения данных в бд: {e}.")
    finally:
        if conn:
            conn.close()
