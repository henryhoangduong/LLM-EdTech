import json
import logging
from contextlib import contextmanager
from typing import List, Optional

from fastapi import HTTPException, status
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from core.config import settings
from core.database import Base
from database.base import DatabaseService
from models.document import SQLDocument
from models.HenryDoc import DateTimeEncoder, HenryDoc

logger = logging.getLogger(__name__)


class PostgresDB(DatabaseService):
    _pool = None
    _engine = None
    _Session = None

    def __init__(self):
        self._get_pool()
        self._initialize_sqlalchemy()
        self._ensure_schema()

    @classmethod
    def _get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = ThreadedConnectionPool(
                    minconn=3,
                    maxconn=10,
                    user=settings.postgres.user,
                    password=settings.postgres.password,
                    host=settings.postgres.host,
                    port=settings.postgres.port,
                    dbname=settings.postgres.db,
                    sslmode="disable",
                )
                logger.info("Created PostgreSQL connection pool")
            except Exception as e:
                logger.error(f"Failed to create connection pool: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to connect to database",
                )
        return cls._pool

    def _initialize_sqlalchemy(self):
        if self._engine is None:
            url = URL.create(
                "postgresql",
                username=settings.postgres.user,
                password=settings.postgres.password,
                host=settings.postgres.host,
                port=settings.postgres.port,
                database=settings.postgres.db,
            )
            self._engine = create_engine(url, poolclass=NullPool)
            self._Session = sessionmaker(bind=self._engine)
            Base.metadata.create_all(self._engine)
            logger.info("Initialized SQLalchemy engine")

    def _ensuer_chema(self):
        Base.metadata.create_all(self._engine)

    @classmethod
    @contextmanager
    def get_connection(cls):
        pool = cls._get_pool()
        conn = None
        try:
            conn = pool.getconn()
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed"
            )
        finally:
            if conn:
                pool.putconn(conn)

    @classmethod
    def execute_query(cls, query, params=None):
        with cls.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    logger.info(f"Executing query: {query}")
                    logger.info(f"Parameters: {params}")
                    cursor.execute(query, params or ())
                    rowcount = cursor.rowcount
                    logger.info(
                        f"Query executed successfully. Affected rows: {rowcount}"
                    )
                conn.commit()
                logger.info("Transactin commited")
                return rowcount
            except Exception as e:
                conn.rollback()
                logger.error(f"Query execution error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database query failed: {str(e)}",
                )

    @classmethod
    def fetch_all(cls, query, params=None):
        with cls.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    logger.info(f"Executing fetch_all query: {query}")
                    logger.info(f"Parameters: {params}")
                    cursor.execute(query, params or ())
                    results = cursor.fetchall()
                    logger.info(f"Query returned {len(results)} results")
                    return [dict(row) for row in results]
            except Exception as e:
                logger.error(f"fetch_all error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database fetch failed: {str(e)}",
                )

    @classmethod
    def fetch_one(cls, query, params=None):
        with cls.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    logger.info(f"Executing fetch_one query: {query}")
                    logger.info(f"Parameters: {params}")
                    cursor.execute(query, params or ())
                    row = cursor.fetchone()
                    if row:
                        logger.info(
                            f"Query returned a row with id: {row.get('id')}")
                        return dict(row)
                    else:
                        logger.warning("Query returned no results")
                        return None
            except Exception as e:
                logger.error(f"fetch_one error: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database fetch failed: {str(e)}",
                )

    def insert_document(self, document: HenryDoc, user_id: str) -> str:
        try:
            session = self._Session()
            db_doc = SQLDocument.from_simbadoc(document, user_id)
            session.add(db_doc)
            session.commit()
            return document.id
        except Exception as e:
            session.rollback()
            logger.error(f"Failed ton insert document: {e}")
            raise
        finally:
            session.close()

    def insert_documents(self,
                         documents: HenryDoc | List[HenryDoc], user_id: str) -> List[str]:
        if not isinstance(documents, list):
            documents = [documents]

        try:
            session = self._Session()
            db_docs = [SQLDocument.from_henrydoc(
                doc, user_id) for doc in documents]
            session.add(db_docs)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to insert documents: {e}")
            raise
        finally:
            session.close()

    def get_document(self, document_id: str | List[str], user_id: str = None) -> Optional[HenryDoc] | List[Optional[HenryDoc]]:
        try:
            session = self._Session()
            if isinstance(document_id, list):
                query = session.query(SQLDocument).filter(
                    SQLDocument.id.in_(document_id)
                )
                if user_id:
                    query = query.filter(SQLDocument.user_id == user_id)
                docs = query.all()
                doc_map = {doc.id: doc for doc in docs}
                return [
                    doc_map.get(doc_id).to_henrydoc(
                    )if doc_map.get(doc_id) else None
                    for doc_id in document_id
                ]
            else:
                query = session.query(SQLDocument).filter(
                    SQLDocument.id == document_id
                )
                if user_id:
                    query = query.filter(SQLDocument.user_id == user_id)
                doc = query.first()
                return doc.to_henrydoc() if doc else None
        except Exception as e:
            logger.error(f"Failed to get document(s) {document_id}: {e}")
            if isinstance(document_id, list):
                return [None for _ in document_id]
            return None
        finally:
            session.close()

    def get_all_documents(self, user_id: str = None) -> List[HenryDoc]:
        try:
            session = self._Session()
            query = session.query(SQLDocument)
            if user_id:
                query = query.filter(SQLDocument.user_id == user_id)
            docs = query.all()
            return [doc.to_henrydoc() for doc in docs]
        except Exception as e:
            logger.error(f"Failed to get all documents: {e}")
            return []
        finally:
            session.close()

    def update_document(self, document_id: str, document: HenryDoc, user_id: str = None) -> bool:
        try:
            session = self._Session()
            doc_dict = json.loads(
                json.dumps(document.model_dump(), cls=DateTimeEncoder)
            )
            query = session.query(SQLDocument).filter(
                SQLDocument.id == document_id)
            if user_id:
                query = query.filter(SQLDocument.user_id == user_id)
            result = query.update({"data": doc_dict})
            return result > 0
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update document {document_id}: {e}")
            return False
        finally:
            session.close()

    def delete_document(self, document_id: str, user_id: str = None) -> bool:
        try:
            session = self._Session()
            query = session.query(SQLDocument).filter(
                SQLDocument.id == document_id)
            if user_id:
                query = query.filter(SQLDocument.user_id == user_id)
            result = query.delete()
            session.commit()
            return result > 0
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False
        finally:
            session.close()

    def delete_documents(self, document_ids):
        return super().delete_documents(document_ids)

    def clear_database(self):
        return super().clear_database()

    def query_documents(self, filters):
        return super().query_documents(filters)

    @classmethod
    def health_check(cls):
        try:
            with cls.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
            return True
        except Exception:
            return False
