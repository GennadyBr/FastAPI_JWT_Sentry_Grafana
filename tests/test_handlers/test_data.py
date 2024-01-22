from uuid import uuid4

from src.db.models import PortalRole

user_data_same = {
    "name": "Petr",
    "surname": "Petrov",
    "email": "lol@kek.com",
    "password": "SamplePass1!",
}
user_data_for_deletion = {
    "user_id": uuid4(),
    "name": "Nikolai",
    "surname": "Nikolaev",
    "email": "lol@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
}
user_data_for_database = {
    "user_id": uuid4(),
    "name": "Nikolai",
    "surname": "Nikolaev",
    "email": "lol@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_USER],
}
user_data_superadmin = {
    "user_id": uuid4(),
    "name": "Admin",
    "surname": "Adminov",
    "email": "admin@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_SUPERADMIN],
}
user_data_create = {
    "name": "Nikolai",
    "surname": "Nikolaev",
    "email": "lol@kek.com",
    "password": "SamplePass1!",
}
user_data = {
    "user_id": uuid4(),
    "name": "Nikolai",
    "surname": "Nikolaev",
    "email": "lol@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_USER],
}
user_data_for_promotion = {
    "user_id": uuid4(),
    "name": "Nikolai",
    "surname": "Nikolaev",
    "email": "lol@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_USER],
}
user_data_who_promoted = {
    "user_id": uuid4(),
    "name": "Ivan",
    "surname": "Ivanov",
    "email": "ivan@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_SUPERADMIN],
}
user_data_for_revoke = {
    "user_id": uuid4(),
    "name": "Nikolai",
    "surname": "Nikolaev",
    "email": "lol@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
}
user_data_who_revoke = {
    "user_id": uuid4(),
    "name": "Ivan",
    "surname": "Ivanov",
    "email": "ivan@kek.com",
    "is_active": True,
    "hashed_password": "SampleHashedPass",
    "roles": [PortalRole.ROLE_PORTAL_SUPERADMIN],
}
