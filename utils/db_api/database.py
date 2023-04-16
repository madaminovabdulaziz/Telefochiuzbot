from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        age BIGINT,
        card_status BOOLEAN,
        work_status BOOLEAN,
        phone VARCHAR (255),
        status INTEGER,
        lang VARCHAR (50)
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, age=0, card_status=False, work_status=False,
                       phone="null", status=0, lang='uz'):
        sql = "INSERT INTO users (full_name, username, telegram_id, age, card_status, work_status, phone, status, " \
              "lang) " \
              "VALUES($1, $2, $3, $4, " \
              "$5, $6, $7, $8, $9) returning *"
        return await self.execute(sql, full_name, username, telegram_id, age, card_status, work_status, phone, status,
                                  lang, fetchrow=True)

    async def update_user_name(self, telegram_id, name):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET full_name='{name}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_user_card(self, telegram_id, status):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET card_status='{status}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_user_phone(self, telegram_id, phone):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET phone='{phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_user_age(self, telegram_id, age):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET age='{age}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_user_status(self, telegram_id, status):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET status='{status}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)


    async def update_user_language(self, telegram_id, lang):
        telegram_id = str(telegram_id)
        sql = f"UPDATE Users SET lang='{lang}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def getUser_name(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT full_name FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def get_all_names(self):
        sql = f"SELECT full_name FROM Users"
        return await self.execute(sql, execute=True)

    async def getUser_phone(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT phone FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def getUser_age(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT age FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)
    
    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def getUser_work(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT work_status FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def getUser_card(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT card_status FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def getUser_lang(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT lang FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def getUser_status(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT status FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def getUser_score(self, telegram_id):
        telegram_id = str(telegram_id)
        sql = f"SELECT score FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchval=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM Users WHERE telegram_id = '{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def get_Users_username(self):
        sql = "SELECT telegram_id FROM Users"
        return await self.execute(sql, fetchrow=True)

    async def get_user_role(self, telegram_id):
        sql = f"SELECT role FROM Users WHERE telegram_id = '{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_work(self, telegram_id, status):
        sql = f"UPDATE Users SET work_status='{status}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_user_by_id(self, telegram_id):
        await self.execute(f"DELETE FROM Users WHERE telegram_id = '{telegram_id}'", execute=True)

    async def delete_user(self, telegram_id):
        await self.execute(f"DELETE FROM Users WHERE telegram_id = '{telegram_id}'", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def create_table_managers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Managers (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        telegram_id BIGINT,
        counter BIGINT,
        status INTEGER,
        datetime VARCHAR (255)
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_managers_counters(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Counter (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT,
        counter BIGINT,
        datetime VARCHAR (255)
        );
        """
        await self.execute(sql, execute=True)

    async def add_manager(self, full_name, telegram_id, datetime, counter, status=1):
        sql = "INSERT INTO Managers (full_name, telegram_id, counter, status, datetime) " \
              "VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, telegram_id, counter, status,
                                  datetime, fetchrow=True)

    async def add_counter(self, telegram_id, counter, datetime):
        sql = """
        INSERT INTO Counter (telegram_id, counter, datetime) VALUES ($1, $2, $3) returning *
        """
        return await self.execute(sql, telegram_id, counter, datetime, fetchrow=True)

    async def switch_on_manager(self, full_name):
        sql = f"UPDATE Managers SET status='{1}' WHERE full_name='{full_name}'"
        return await self.execute(sql, execute=True)

    async def switch_off_manager(self, full_name):
        sql = f"UPDATE Managers SET status='{0}' WHERE full_name='{full_name}'"
        return await self.execute(sql, execute=True)

    async def update_name(self, full_name):
        sql = f"UPDATE Managers SET status='{1}' WHERE full_name='{full_name}'"
        return await self.execute(sql, execute=True)

    async def get_manager_names(self):
        sql = "SELECT full_name from Managers"
        return await self.execute(sql, execute=True)

    async def is_manager(self, id):
        sql = f"SELECT telegram_id from Managers WHERE telegram_id = '{id}'"
        return await self.execute(sql, fetchval=True)

    async def getAllMenegers(self):
        sql = f"SELECT telegram_id from Managers"
        return await self.execute(sql, fetchrow=True)

    async def show_off(self):
        sql = f"SELECT full_name, telegram_id from Managers WHERE status = '{0}'"
        return await self.execute(sql, fetch=True)

    async def show_on(self):
        sql = f"SELECT full_name, telegram_id from Managers WHERE status = '{1}'"
        return await self.execute(sql, fetch=True)

    async def showByName(self, full_name):
        sql = f"SELECT telegram_id from Managers WHERE full_name = '{full_name}'"
        return await self.execute(sql, fetchval=True)

    async def show_both(self):
        sql = """
        SELECT full_name, telegram_id from Managers
        """
        return await self.execute(sql, fetch=True)

    async def delete_manager(self, full_name):
        await self.execute(f"DELETE FROM Managers WHERE full_name = '{full_name}'", execute=True)

    async def drop_managers(self):
        await self.execute("DROP TABLE Managers", execute=True)

    async def showStatistcs(self, telegram_id, year, month):
        sql = f"""
        SELECT SUM(counter) as total_counter
        FROM Counter
        WHERE telegram_id = '{telegram_id}'
        AND extract(month from datetime::date) = CAST('{month}' AS INTEGER)
        AND extract(year from datetime::date) = CAST('{year}' AS INTEGER)
        """
        return await self.execute(sql, fetchval=True)

    async def getMonthYear(self):
        sql = """
        SELECT DISTINCT EXTRACT(MONTH FROM datetime::date) AS month, CAST(EXTRACT(YEAR FROM datetime::date) AS INTEGER) AS year
        FROM Counter
        ORDER BY year, month
        """
        return await self.execute(sql, fetch=True)
