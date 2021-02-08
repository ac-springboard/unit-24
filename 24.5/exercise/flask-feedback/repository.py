from authorization_server import AuthorizationServer as AS
from models import User, Feedback


def reset_tables(db):
    db.drop_all()
    db.create_all()
    db.session.commit()

    # password = monkey
    john = User(first_name="John", last_name="Doe",
                username='john',
                email='almircampos@gmail.com', password='$2b$12$dvfjPb.mLIMhNV1ZXbzyDeKEXgpSr99VXbU3SDsyPrEzu4iIYMiJu',
                admin=False)
    john_fb_01 = Feedback(title='john_fb_01', content='john_cfb_01', username='john')
    john_fb_02 = Feedback(title='john_fb_02', content='john_cfb_02', username='john')

    jane = User(first_name="Jane", last_name="D",
                username='jane',
                email='almircampos@gmail.com', password='$2b$12$dvfjPb.mLIMhNV1ZXbzyDeKEXgpSr99VXbU3SDsyPrEzu4iIYMiJu',
                admin=True)

    jane_fb_01 = Feedback(title='jane_fb_01', content='jane_cfb_01', username='jane')
    jane_fb_02 = Feedback(title='jane_fb_02', content='jane_cfb_02', username='jane')

    AS.add_or_update_user_autho(john, ['edit_feedback'])
    AS.add_or_update_user_autho(jane, [])

    db.session.add_all([john, jane, john_fb_01, john_fb_02, jane_fb_01, jane_fb_02])
    db.session.commit()


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
