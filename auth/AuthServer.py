from concurrent import futures
import bcrypt
import grpc
from cryptography.fernet import Fernet

import requests_pb2
import requests_pb2_grpc
from sqlalchemy.orm import sessionmaker
from authdbAttributes import authdb_engine
from communicationAttributes import comm_encryption_key, secret_key
from models import User
import jwt
import datetime


class Listener(requests_pb2_grpc.AuthServiceServicer):

    def validate_credentials(self, user, pw):
        if user and bcrypt.hashpw(pw.encode('utf-8'), user.password_hash.encode('utf-8')):
            return True
        return False

    def generate_session_token(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
        }
        session_token = jwt.encode(payload, secret_key, algorithm="HS256")
        return session_token

    def get_user(self, email):
        Session = sessionmaker(bind=authdb_engine)
        session = Session()
        user = session.query(User).filter_by(email=email).first()
        session.close()
        return user

    def auth(self, request, context):
        cipher_suite = Fernet(comm_encryption_key)
        email = request.credentials.email
        pwhash = cipher_suite.decrypt(request.credentials.password.encode()).decode()
        user = self.get_user(email)
        if user:
            if self.validate_credentials(user, pwhash):
                return requests_pb2.OptionalToken(authenticated=True, session_token=self.generate_session_token(str(user.id)))
            else:
                return requests_pb2.OptionalToken(authenticated=False, session_token="0000")
        else:
            return requests_pb2.OptionalToken(authenticated=False, session_token="0000")


def serve():
    max_workers = 2
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    requests_pb2_grpc.add_AuthServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("-----------------------RUNNING-----------------------")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
