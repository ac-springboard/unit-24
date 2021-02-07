from flask import session, redirect, flash
from flask_api.exceptions import NotAuthenticated
from werkzeug.exceptions import Unauthorized


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


def authorized(func):
    def check_authorization(*args, **kwargs):
        logged_username = session.get('username')
        if not logged_username:
            try:
                raise Unauthorized()
            except Unauthorized:
                flash(u"Please contact the system administration"
                      u"to get access to this resource.",
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


class AuthorizationServer:
    # autho_table = {
    #     'jane': {
    #         'admin': True,
    #         'resources': []
    #     },
    #     'john': {
    #         'admin': False,
    #         'resources': ['edit_feedback', 'delete_feedback']
    #     },
    #
    # }

    autho_table = {

    }

    @staticmethod
    def add_or_update_user_autho(user, resources: list):
        AuthorizationServer.autho_table['user.username']['admin'] = user.admin
        AuthorizationServer.autho_table['user.username']['resources'] = resources
