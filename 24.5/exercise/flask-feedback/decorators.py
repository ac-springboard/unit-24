from flask import session, redirect, flash
from flask_api.exceptions import NotAuthenticated
from werkzeug.exceptions import Unauthorized

from authorization_server import AuthorizationServer as AS
from repository import FbRepo


def authenticated(func):
    def check_authentication(*args, **kwargs):
        logged_username = session.get('username')
        if not logged_username:
            # raise Unauthorized()
            try:
                raise NotAuthenticated()
            except NotAuthenticated as na:
                flash(u'Please, login first.', 'bg-warning')
                return redirect('/login')

        if not args:
            if not kwargs:
                return func()
            else:
                return func(**kwargs)
        else:
            if not kwargs:
                return func(*args)
            else:
                return func(*args, **kwargs)

    check_authentication.__name__ = func.__name__
    return check_authentication


def get_ref_user(kwargs):
    if 'feedback_id' in kwargs:
        return FbRepo.get_by_id(kwargs['feedback_id'])
    return None


def authorized(resource_key):
    def authorized_decorator(func):
        def check_authorization(*args, **kwargs):
            logged_username = session.get('username')
            user_autho = AS.autho_table[logged_username]
            is_admin = user_autho['admin']
            if not is_admin:
                is_owner = get_ref_user(kwargs).username == logged_username
                if not is_owner:
                    is_authorized_resource = resource_key in user_autho['resources']
                    if not is_authorized_resource:
                        try:
                            raise Unauthorized()
                        except Unauthorized:
                            flash(u"Please contact the system administration"
                                  u" to get access to this resource.",
                                  'bg-warning')
                            return redirect('/contact-us')

            if not args:
                if not kwargs:
                    return func()
                else:
                    return func(**kwargs)
            else:
                if not kwargs:
                    return func(*args)
                else:
                    return func(*args, **kwargs)

        check_authorization.__name__ = func.__name__
        return check_authorization

    return authorized_decorator



