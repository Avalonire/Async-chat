import datetime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime


class Storage:
    class AllClients:
        def __init__(self, username):
            self.id = None
            self.name = username
            self.last_login = datetime.datetime.now()

    class ClientHistory:
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class UserContacts:
        def __init__(self, id_main_user, name_main_user, id_contact):
            self.id = None
            self.id_main_user = id_main_user
            self.name_main_user = name_main_user
            self.id_contact = id_contact

    def __init__(self):
        self.database_engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=10800)

        self.metadata = MetaData()

        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime)
                            )

        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        user_contacts = Table('Contacts', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', ForeignKey('Users.id')),
                              Column('id', Integer, ForeignKey('Users.id')),
                              Column('id', Integer, ForeignKey('Users.id')),
                              )

        self.metadata.create_all(self.database_engine)

        mapper(self.AllClients, users_table)
        mapper(self.ClientHistory, user_login_history)
        mapper(self.UserContacts, user_contacts)
        session = sessionmaker(bind=self.database_engine)
        self.session = session()

    def user_login(self, username, ip_address, port):
        check_user = self.session.query(self.AllClients).filter_by(name=username)
        if check_user.count():
            user = check_user.first()
            user.last_login = datetime.datetime.now()
        else:
            user = self.AllClients(username)
            self.session.add(user)
            self.session.commit()

        user_history = self.ClientHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(user_history)
        self.session.commit()

    def user_logout(self, username):

        user = self.session.query(self.AllClients).filter_by(name=username).first()
        user_logout = self.ClientHistory(user.id, datetime.datetime.now(), user.ip_adress, user.port)
        self.session.add(user_logout)
        self.session.commit()

    def user_contact(self, main_user, contact):
        user = self.session.query(self.AllClients).filter_by(name=main_user).first()
        contact = self.session.query(self.AllClients).filter_by(name=contact).first()
        create_contacts = self.UserContacts(user.name, user.id, contact.id)
        self.session.add(create_contacts)
        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllClients.name,
            self.AllClients.last_login,
        )
        return query.all()

    def login_history(self, username=None):
        query = self.session.query(self.AllClients.name,
                                   self.ClientHistory.date_time,
                                   self.ClientHistory.ip,
                                   self.ClientHistory.port
                                   ).join(self.AllClients)
        if username:
            query = query.filter(self.AllClients.name == username)
        return query.all()


if __name__ == '__main__':
    # Testing Database
    test_db = Storage()
    test_db.user_login('client_1', '192.168.1.5', 7777)
    test_db.user_logout('client_1')
    test_db.login_history('client_1')
    print(test_db.users_list())
