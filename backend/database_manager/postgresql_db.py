# pylint: disable=invalid-name, broad-exception-caught, global-variable-undefined
"""
PostgreSQL 관련 클래스
"""
from typing import List
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class PostgreSQL:
    """PostgreSQL DB 클래스
    (접속 / 조회(S) / 삽입(I) / 수정(U) / 삭제(D))

    psycopg2 모듈 설치 (pip install psycopg2-binary)
    """

    def __init__(self, host, user, port, pw):
        self.host = host
        self.user = user
        self.port = port
        self.pw = pw
        self.conn = None
        self.cur = None

    def connect(self):
        """
        postgresql 연결
        """
        try:
            # postgresql 연결
            self.conn = psycopg2.connect(
                host=self.host, user=self.user, port=self.port, password=self.pw
            )
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # cursor 객체 생성
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def connect_db(self, db_nm: str):
        """
        postgresql Database 연결

        Args:
            db_nm (str): 접속할 DB명
        """
        try:
            # postgresql db 연결
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.pw,
                database=db_nm,
            )
            # cursor 객체 생성
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def disconnect(self):
        """
        postgresql 연결 해제
        """
        try:
            # postgresql 연결 해재
            self.conn.close()
            # cursor 객체 해제
            self.cur.close()
        except Exception as e:
            print(e)

    def exist_db(self, db_nm: str) -> bool:
        """
        Database 존재 여부 확인

        Args:
            db_nm (str): 조회할 DB명

        Returns:
            bool: Database 존재 여부(True/False)
        """
        exist = False
        try:
            self.connect()
            query = (
                "SELECT datname FROM pg_catalog.pg_database "
                + f"WHERE datname = '{db_nm}'"
            )
            self.cur.execute(query)
            row = self.cur.fetchall()
            if len(row) > 0:
                exist = True
        except Exception as e:
            print(e)
        self.disconnect()
        return exist

    def exist_trigger(self, db_nm: str, trigger_nm: str) -> bool:
        """
        Trigger 존재 여부 확인

        Args:
            db_nm (str): 조회할 DB명
            trigger_nm (str): 조회할 trigger명

        Returns:
            bool: Trigger 존재 여부(True/False)
        """
        exist = False
        try:
            self.connect_db(db_nm)
            query = "SELECT tgname FROM pg_trigger"
            self.cur.execute(query)
            row = self.cur.fetchall()
            triggers = [item[0] for item in row]
            if trigger_nm in triggers:
                exist = True
        except Exception as e:
            print(e)
        self.disconnect()
        return exist

    def create_db(self, db_nm: str):
        """
        Database 생성

        Args:
            db_nm (str): 생성할 DB명
        """
        try:
            self.connect()
            query = f"CREATE DATABASE {db_nm}"
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
        self.disconnect()

    def drop_db(self, db_nm: str):
        """
        Database 제거

        Args:
            db_nm (str): Database 명
        """
        try:
            self.connect()
            query = f"DROP DATABASE IF EXISTS {db_nm}"
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
        self.disconnect()

    def select_tables(self, db_nm: str) -> List[str]:
        """
        Database 내 테이블 목록 조회

        Args:
            db_nm (str): 테이블 목록 조회할 Database

        Returns:
            List[str]: Database 내 테이블 목록
        """
        try:
            self.connect_db(db_nm)
            query = (
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                + "WHERE TABLE_SCHEMA = 'public'"
            )
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return [row[0] for row in rows] if len(rows) > 0 else []
        except Exception as e:
            print(e)
        self.disconnect()
        return []

    def create_table(
        self, db_nm: str, tbl_nm: str, cols: List[tuple[str, str]], const: str = None
    ):
        """
        Table 생성

        Args:
            db_nm (str): 테이블 생성될 Database
            tbl_nm (str): 생성할 테이블 명
            cols (List[tuple[str, str]]): (column 이름, column 타입)으로 구성된 리스트
            const (str): 제약 조건
        """
        try:
            self.connect_db(db_nm)
            query_col = f"({','.join([f'{col[0]} {col[1]}' for col in cols])})"
            if const:
                query_col = query_col[:-1] + f", {const})"
            query = f"CREATE TABLE {tbl_nm} {query_col} "
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
        self.disconnect()

    def drop_table(self, db_nm: str, tbl_nm: str):
        """
        Table 제거

        Args:
            db_nm (str): Database 명
            tbl_nm (str): Table 명
        """
        try:
            self.connect_db(db_nm)
            query = f"DROP TABLE IF EXISTS {tbl_nm}"
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
        self.disconnect()

    def add_columns(self, db_nm: str, tbl_nm: str, cols: List[tuple[str, str]]):
        """
        테이블에 컬럼 추가

        Args:
            db_nm (str): Database 명
            tbl_nm (str): Table 명
            cols (List[tuple[str, str]]): 추가할 컬럼 리스트 (컬럼 명, 제약 조건)
        """
        try:
            self.connect_db(db_nm)
            add_query = ",".join(
                [f"ADD COLUMN {col_nm} {const}" for (col_nm, const) in cols]
            )
            query = f"ALTER TABLE {tbl_nm} {add_query}"
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
        self.disconnect()

    def execute(self, db_nm: str, query: str):
        """
        DB내 특정 query 실행

        Args:
            db_nm (str): Database 명
            query (str): 쿼리문
        """
        is_excute = True
        try:
            self.connect_db(db_nm)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            is_excute = False
        self.disconnect()
        return is_excute

    def excute_sql_file(self, db_nm: str, sql_file: str):
        """
        DB 내 sql 파일 실행        
        """
        try:
            self.connect_db(db_nm)
            self.cur.execute(open(sql_file, "r", encoding="utf-8").read())
            self.conn.commit()
        except Exception as e:
            print(e)
        self.disconnect()

    def select(self, db_nm: str, query: str) -> tuple[List[List[object]], List[str]]:
        """
        DB 내 Select문 실행

        Args:
            db_nm (str): Database 명
            query (str): Select 쿼리문

        Returns:
            List[List[object]]: select 결과 리스트
            List[str]: select 결과 컬럼
        """
        rows = None
        cols = None
        try:
            self.connect_db(db_nm)
            self.cur.execute(query)
            cols = [desc[0] for desc in self.cur.description]
            rows = self.cur.fetchall()
        except Exception as e:
            print(e)
            rows = None
        self.disconnect()
        return rows, cols
