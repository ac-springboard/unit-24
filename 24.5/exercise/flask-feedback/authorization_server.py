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

    autho_table = {

    }

    @staticmethod
    def add_or_update_user_autho(user, resources: list):
        user_autho = {
            'admin': user.admin,
            'resources': resources
        }
        AuthorizationServer.autho_table[user.username] = user_autho
        print('=====>>>>> autho_table:', AuthorizationServer.autho_table)
