from authorization_server import AuthorizationServer as AS
from models import User, Feedback


def reset_tables_with_test_users(db):
    db.drop_all()
    db.create_all()
    # db.session.commit()

    # password = monkey
    john = User(first_name="John", last_name="Doe",
                username='john',
                email='almircampos@gmail.com', password='$2b$12$dvfjPb.mLIMhNV1ZXbzyDeKEXgpSr99VXbU3SDsyPrEzu4iIYMiJu',
                is_admin=False)
    john_fb_01 = Feedback(title='john_fb_01', content='john_cfb_01', username='john')
    john_fb_02 = Feedback(title='john_fb_02', content='john_cfb_02', username='john')

    AS.add_or_update_user_autho(john, ['update_feedback'])

    jane = User(first_name="Jane", last_name="D",
                username='jane',
                email='almircampos@gmail.com', password='$2b$12$dvfjPb.mLIMhNV1ZXbzyDeKEXgpSr99VXbU3SDsyPrEzu4iIYMiJu',
                is_admin=True)

    AS.add_or_update_user_autho(jane, [])

    jane_fb_01 = Feedback(title='jane_fb_01', content='jane_cfb_01', username='jane')
    jane_fb_02 = Feedback(title='jane_fb_02', content='jane_cfb_02', username='jane')

    fester = User(first_name="Fester", last_name="Bestertester",
                  username='fester',
                  email='almircampos@gmail.com', password='$2b$12$dvfjPb.mLIMhNV1ZXbzyDeKEXgpSr99VXbU3SDsyPrEzu4iIYMiJu',
                  is_admin=False)

    fester_fb_01 = Feedback(title='fester_fb_01', content='fester_cfb_01', username='fester')
    fester_fb_02 = Feedback(title='fester_fb_02', content='fester_cfb_02', username='fester')

    db.session.add_all([john, john_fb_01, john_fb_02, jane, jane_fb_01, jane_fb_02, fester, fester_fb_01, fester_fb_02])
    # db.session.add(jane)
    # db.session.add(jane_fb_01)
    # db.session.add(jane_fb_02)
    # db.session.add(john)
    # db.session.add(john_fb_01)
    # db.session.add(john_fb_02)
    db.session.commit()


def set_test_authorizations():
    john = UserRepo.get('john')
    jane = UserRepo.get('jane')
    print(john.authorizations, jane.authorizations)


# TODO: make it generic

class FbRepo:
    @staticmethod
    def get_by_id(feedback_id):
        return Feedback.query.get(feedback_id)

    @staticmethod
    def get_user(feedback_id):
        fb = Feedback.get_by_id(feedback_id)
        return fb.user

    @staticmethod
    def get_all():
        return Feedback.query.get_all()


class UserRepo:

    @staticmethod
    def get_authorizations(username):
        # fe_authorizations = []
        user = User.query.get(username)
        if user.is_admin:
            return 'all'
        return AS.get_user_authorizations(username)

    @staticmethod
    def get(username):
        return User.query.get(username)
