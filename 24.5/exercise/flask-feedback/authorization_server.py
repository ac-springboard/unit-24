class AuthorizationServer:
    # autho_table = {
    #     'jane': {
    #         'admin': True,
    #         'resources': []
    #     },
    #     'john': {
    #         'admin': False,
    #         'resources': ['edit_feedback']
    #     },
    #
    # }

    authorizations = {
        'delete_feedback': 'Can delete feedbacks of any user',
        'update_feedback': 'Can update feedbacks of any user'
    }

    autho_table = {

    }

    # TODO: IMPLEMENT THE OBSERVER PATTERN TO UPDATE THE USER'S AUTHORIZATIONS
    @staticmethod
    def add_or_update_user_autho(user, resources: list):
        user_autho = {
            'admin': user.is_admin,
            'resources': resources
        }
        AuthorizationServer.autho_table[user.username] = user_autho
        return resources

    @staticmethod
    def get_user_authorizations(username):
        user_authorizations = AuthorizationServer.autho_table.get(username, None)
        if not user_authorizations:
            return []
        return user_authorizations.get('resources', [])
