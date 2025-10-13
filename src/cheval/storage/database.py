# database.py

import os
from typing import List, Optional, Tuple

from sqlmodel import SQLModel, Field, create_engine, Session, select

from ..models.models import DataType, CodeRecorder, Match, Race, ResultOfRace, Horse, ResultOfHorse, Jockey, Trainer, SummaryOfJockeyTrainer
from ..config import DIR_FOR_DATA

class ChevalDB:
    def __init__(self, folder: str = DIR_FOR_DATA, filename: str = "cheval.db"):
        """Initialize database connection and engine"""
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        self.engine = create_engine(f"sqlite:///{path}")
        self.session_factory = Session(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Create database table"""
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Obtain database session"""
        return self.session_factory

    def get_all_codes(self):
        with self.get_session() as session:
            records = session.exec(select(CodeRecorder)).all()
            if not records:
                return []
            result = []
            for r in records:
                result.append(r)
            return result
    
    def check_code(self, code: str, datetype: DataType):
        """Finds a code based on the combination of code and datetype (which, according to the table constraints, must be unique if it exists).
        Returns the code if it exists, otherwise returns None."""
        with self.get_session() as session:
            stmt = select(CodeRecorder).where(
                CodeRecorder.code == code,
                CodeRecorder.datetype == datetype
            )
            record = session.exec(stmt).first()
            if record:
                record.count += 1
                session.add(record)
                session.commit()
                session.refresh(record)
            return record

    def insert_match(self, thematch: Match):
        """Insert match data. Before calling this function, you must firstly call check_code to ensure that there is no Match record with the same code."""
        thecode = CodeRecorder(code=thematch.code, name=thematch.name, datetype=DataType.MATCH)
        with self.get_session() as session:
            session.add(thematch)
            session.add(thecode)
            session.commit()

    def get_match_by_code(self, code: str) -> Optional[Match]:
        """Get the match by code."""
        with self.get_session() as session:
            return session.get(Match, code)

    def insert_race(self, therace: Race):
        """Insert race data. Before calling this function, you must firstly call check_code to ensure that there is no Race record with the same code."""
        thecode = CodeRecorder(code=therace.code, name=therace.name, datetype=DataType.RACE)
        #print(thecode)
        with self.get_session() as session:
            session.add(therace)
            session.add(thecode)
            session.commit()

    def get_race_by_code(self, code: str) -> Optional[Race]:
        """Get the race by code."""
        with self.get_session() as session:
            return session.get(Race, code)

    def insert_race_result_list(self, theraceresults: List[ResultOfRace]):
        """Insert a race result list."""
        #print(thecode)
        with self.get_session() as session:
            for result in theraceresults:
                session.add(result)
            session.commit()

    def get_results_by_race_code(self, code: str):
        """Get the horse results by horse code."""
        with self.get_session() as session:
            statement = select(ResultOfRace).where(ResultOfRace.race_code == code)
            return session.exec(statement).all()

    def insert_horse(self, thehorse: Horse):
        """Insert horse data. Before calling this function, you must firstly call check_code to ensure that there is no Race record with the same code."""
        thecode = CodeRecorder(code=thehorse.code, name=thehorse.name, datetype=DataType.HORSE)
        #print(thecode)
        with self.get_session() as session:
            session.add(thehorse)
            session.add(thecode)
            session.commit()

    def get_horse_by_code(self, code: str) -> Optional[Horse]:
        """Get the horse by code."""
        with self.get_session() as session:
            return session.get(Horse, code)

    def insert_horse_result_list(self, thehorseresults: List[ResultOfHorse]):
        """Insert a horse result list."""
        #print(thecode)
        with self.get_session() as session:
            for result in thehorseresults:
                session.add(result)
            session.commit()

    def get_results_by_horse_code(self, code: str):
        """Get the horse results by horse code."""
        with self.get_session() as session:
            statement = select(ResultOfHorse).where(ResultOfHorse.horse_code == code)
            return session.exec(statement).all()

    def insert_jockey(self, thejockey: Jockey):
        """Insert jockey data. Before calling this function, you must firstly call check_code to ensure that there is no Race record with the same code."""
        thecode = CodeRecorder(code=thejockey.code, name=thejockey.name, datetype=DataType.JOCKEY)
        #print(thecode)
        with self.get_session() as session:
            session.add(thejockey)
            session.add(thecode)
            session.commit()

    def get_jockey_by_code(self, code: str) -> Optional[Jockey]:
        """Get the jockey by code."""
        with self.get_session() as session:
            return session.get(Jockey, code)

    def insert_trainer(self, thetrainer: Trainer):
        """Insert trainer data. Before calling this function, you must firstly call check_code to ensure that there is no Race record with the same code."""
        thecode = CodeRecorder(code=thetrainer.code, name=thetrainer.name, datetype=DataType.TRAINER)
        #print(thecode)
        with self.get_session() as session:
            session.add(thetrainer)
            session.add(thecode)
            session.commit()

    def get_trainer_by_code(self, code: str) -> Optional[Trainer]:
        """Get the trainer by code."""
        with self.get_session() as session:
            return session.get(Trainer, code)

    def insert_jockey_trainer_summary_list(self, thesummaries: List[SummaryOfJockeyTrainer]):
        """Insert jockey or trainer summary list."""
        #print(thecode)
        with self.get_session() as session:
            for summary in thesummaries:
                session.add(summary)
            session.commit()

    def get_summaries_by_jockey_trainer_code(self, code: str):
        """Get the jockey or trainer summaries by jockey or trainer code."""
        with self.get_session() as session:
            statement = select(SummaryOfJockeyTrainer).where(SummaryOfJockeyTrainer.jockey_trainer_code == code)
            return session.exec(statement).all()

    '''def insert_horse(self, horse: Horse):
        """插入马匹数据"""
        with self.get_session() as session:
            session.add(horse)
            session.commit()

    def get_horse_by_code(self, code: str) -> Optional[Horse]:
        """根据马匹代码查询马匹数据"""
        with self.get_session() as session:
            return session.get(Horse, code)

    def insert_result(self, result: ResultOfHorse):
        """插入马匹赛果数据"""
        with self.get_session() as session:
            session.add(result)
            session.commit()

    def get_results_by_horse_code(self, horse_code: str):
        """根据马匹代码查询赛果"""
        with self.get_session() as session:
            results = session.query(ResultOfHorse).filter(ResultOfHorse.horse_code == horse_code).all()
            return results'''

    def close(self):
        """关闭数据库连接"""
        self.session_factory.close()
