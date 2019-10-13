#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Api
from api.handlers.UserHandlers import Register, Login, Logout, RefreshToken, UsersData, ResetPassword, \
    DataAdminRequired, DataUserRequired, AddUser


def generate_routes(app):

    # Create api.
    api = Api(app)

    # Add all routes resources.
    # Register page.
    api.add_resource(Register, '/v1/auth/register')

    # Login page.
    api.add_resource(Login, '/v1/auth/login')

    # Logout page.
    api.add_resource(Logout, '/v1/auth/logout')

    # Refresh page.
    api.add_resource(RefreshToken, '/v1/auth/refresh')

    # Password reset page. Not forgot.
    api.add_resource(ResetPassword, '/v1/auth/password_reset')

    # Get users page with admin permissions.
    api.add_resource(UsersData, '/users')

    # Example admin handler for admin permission.
    api.add_resource(DataAdminRequired, '/data_admin')

    # Example user handler for user permission.
    api.add_resource(DataUserRequired, '/data_user')

    # Example user handler for user permission.
    api.add_resource(AddUser, '/user_add')
