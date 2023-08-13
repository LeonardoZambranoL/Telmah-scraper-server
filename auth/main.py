import bcrypt
from sqlalchemy_utils import database_exists
from models import Base, User, Ruc
from authdbAttributes import *
from sqlalchemy.orm import sessionmaker
import AuthServer


def init_auth_database():
    if not database_exists(authdb_engine.url):
        # If the database doesn't exist, create it
        Base.metadata.create_all(bind=authdb_engine)
        createDummyEntries()
        print(f"Database '{authdb_path}' created.")
    else:
        print(f"Database '{authdb_path}' already exists.")


def createDummyEntries():
    Session = sessionmaker(bind=authdb_engine)
    session = Session()
    person = User("a@b.com", "dummy", "person", bcrypt.hashpw("asdads".encode('utf-8'), bcrypt.gensalt()).decode())
    person2 = User("c@d.com", "dummy2", "person2", bcrypt.hashpw("asdads".encode('utf-8'), bcrypt.gensalt()).decode())
    ruc1 = Ruc("123", person)
    ruc2 = Ruc("123321", person2)
    ruc3 = Ruc("123321234", person2)
    session.add(person)
    session.add(person2)
    session.commit()
    for u in session.query(User).all():
        print(u)
    session.close()

def run():
    init_auth_database()
    AuthServer.serve()


if __name__ == "__main__":
    run()
    Session = sessionmaker(bind=authdb_engine)
    session = Session()
    users = session.query(User)
    for u in users:
        print(u)