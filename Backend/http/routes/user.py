from Backend.resources.User import UserResource, UsersResource, UserAuth, Username


def routes(register):
    register(UsersResource, '/user')
    register(UserResource, '/user/<int:user_id>')
    register(UserAuth, '/user/auth')
    register(Username, '/username/<int:user_id>')