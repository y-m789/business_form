from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DATETIME
from sqlalchemy import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class BaseInfo(Base):
    """
    基本情報のデータベース
    """
    __tablename__ = 'baseinfo'
    id = Column(Integer, primary_key=True)
    name = Column(String)        # 代表者名
    company = Column(String)     # 会社名
    department = Column(String)  # 部署名
    post = Column(String)        # 郵便番号
    address = Column(String)     # 住所
    tel = Column(String)         # 電話番号
    email = Column(String)       # E-mail
    bank = Column(String)        # 振込先
    memo_estimate = Column(String)  # 見積書備考
    memo_bill = Column(String)      # 請求書備考
    memo_deliver = Column(String)   # 納品書備考

    def __repr__(self):
        return "Base<{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>".format(
            self.id,
            self.name,
            self.company,
            self.department,
            self.post,
            self.address,
            self.tel,
            self.email,
            self.bank,
            self.memo_estimate,
            self.memo_bill,
            self.memo_deliver,
        )


class Content(Base):
    """
    取引先情報のデータベース
    """
    __tablename__ = 'contents'
    customer_id = Column(Integer, primary_key=True)  # 書類ID
    customer = Column(String)               # 取引先会社名
    customer_department = Column(String)    # 取引先部署名
    customer_name = Column(String)          # 取引先担当者名
    title = Column(String)      # 取引先担当者名
    # 品目、数量、単位、単価、成立
    item1, volume1, unit1, price1, tax1 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item2, volume2, unit2, price2, tax2 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item3, volume3, unit3, price3, tax3 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item4, volume4, unit4, price4, tax4 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item5, volume5, unit5, price5, tax5 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item6, volume6, unit6, price6, tax6 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item7, volume7, unit7, price7, tax7 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    item8, volume8, unit8, price8, tax8 = Column(String), Column(Integer), Column(String), Column(Integer), Column(Integer)
    num_estimate = Column(String)  # 見積書番号
    num_bill = Column(String)      # 請求書番号
    num_deliver = Column(String)   # 納品書番号
    timestamp = Column(DATETIME)   # 登録日
    timestamp_estimate = Column(DATETIME)  # 見積書発行日
    timestamp_bill = Column(DATETIME)      # 請求書発行日
    timestamp_deliver = Column(DATETIME)   # 納品書発行日
    limit_bill = Column(DATETIME)      # 支払期限

    def __repr__(self):
        return "Content<{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>".format(
            self.customer_id,
            self.customer,
            self.customer_department,
            self.customer_name,
            self.title,
            self.item1, self.volume1, self.unit1, self.price1, self.tax1,
            self.item2, self.volume2, self.unit2, self.price2, self.tax2,
            self.item3, self.volume3, self.unit3, self.price3, self.tax3,
            self.item4, self.volume4, self.unit4, self.price4, self.tax4,
            self.item5, self.volume5, self.unit5, self.price5, self.tax5,
            self.item6, self.volume6, self.unit6, self.price6, self.tax6,
            self.item7, self.volume7, self.unit7, self.price7, self.tax7,
            self.item8, self.volume8, self.unit8, self.price8, self.tax8,
            self.num_estimate,
            self.num_bill,
            self.num_deliver,
            self.timestamp_bill,
            self.timestamp_estimate,
            self.timestamp_deliver,
            self.limit_bill)


def mk_db():
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = scoped_session(session_maker)
    return session
