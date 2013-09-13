# -*- coding: utf-8 -*-
"""
Hannes,

I think we need an Action class, partly to allow to use non string "actions"
an partly because we need support for "umbrella" actions such as "manage"
"moderate" etc...

But we also want to bea able to just use strings to identify actions and
to allow future users of API to define custom actions.

So I am thinking:

class ApplicationActions(Actions):

    approve_store_product = 'approve_store_product'
    read_secrets = 'read_secrets'



class ControllerActions(Actions):
    index = 'index'
    read = 'read'
    create = 'create'
    update = 'update'
    delete = 'delete'
    query = 'query'
    manage = alias(index, read, create, update, delete, query)


class Roles(object):
    
    guest = Role()
    guest.grant(ControllerActions.read, Product)
    guest.grant(ControllerActions.read, ProductType)


    owner = Role(inherit=[guest])
    owner.grant(ApplicationActions.read_secrets, Store, UserIdentity.is_store_owner)
    owner.grant(ApplicationActions.read_secrets, Product, UserIdentity.is_store_owner_of_product)
    owner.grant(ControllerActions.manage, Store, UserIdentity.is_store_owner)
    owner.grant(ControllerActions.manage, Product, UserIdentity.is_store_owner_of_product)

    admin = Role(inherit=[guest])
    admin.grant(ControllerActions.manage, Store)
    admin.grant(ControllerActions.manage, Product)


class StoreController(ModelController):
    guard = Guard


UserIdentity(Identity):
    def __init__(self, user):
        user = User

    def is_store_owner(self, store):
        return store.owner_id == self.user.id

    def is_store_owner_of_product(self, product):
        return product.store.owner_id == self.user.id


class StoreView(ModelView):
    controller = StoreController
    filter_chain = [
        CamelizeFilter,
        ExcludeActionFilter(
            exclude=['api_key', 'password'],
            ApplicationActions.read_secrets,
            Guard
        )
    ]
    serializer = SAModelSerializer




context.identity = Identity([Roles.admin])

guard.can(context.identity, action_name, subject)

## Not sure about where to put the guard, maybe on API or controller?!
## Prolly better on controller, even if it is repetitive.

"""

from inflection import underscore


def subject_alias(subject):
    if isinstance(subject, basestring):
        return underscore(subject)
    elif isinstance(subject, type):
        return underscore(subject.__name__)
    elif isinstance(subject, list) and all(type(item) == type(subject[0]) for item in subject):
        return underscore(type(subject[0]).__name__)
    else:
        return underscore(type(subject).__name__)


class Guard(object):
    """
    Identity is the base class for users, roles, services, etc.
    Identity provides a set of permissions.
    """

    def can(self, identity, action, subject):
        subject_name = subject_alias(subject)
        key = (action, subject_name)

        subjects = subject if isinstance(subject, list) else [subject]

        results = []
        for item in subjects:
            results.append(self._authorize(item, identity, key))

        if len(results) > 0 and all(results):
            return True

        return False

    def cannot(self, identity, action, subject):
        return not self.can(identity, action, subject)

    def _authorize(self, subject, identity, key):
        for role in identity.roles:
            for permission in role.permissions:
                if permission.key == key and permission.granted_on(subject, identity):
                    return True
        return False


class Identity(object):

    def __init__(self, roles):
        self.roles = roles


def true_condition(self, *args, **kwargs):
    return True


class Role(object):
    def __init__(self, inherit=[]):
        self.permissions = []
        for role in inherit:
            self.permissions += role.permissions

    def grant(self, actions, subject, condition=true_condition):
        if not isinstance(actions, list):
            actions = [actions]

        for action in actions:
            self.permissions.append(Permission(action, subject, condition))


class Actions(object):

    @classmethod
    def alias(cls, *args, **kwargs):
        return list(args)


class ControllerActions(Actions):
    index = 'index'
    read = 'read'
    create = 'create'
    update = 'update'
    delete = 'delete'
    query = 'query'
    manage = Actions.alias(index, read, create, update, delete, query)


class Permission(object):

    def __init__(self, action, subject, condition):
        self.action = action
        self.subject = subject_alias(subject)
        self.condition = condition

    @property
    def key(self):
        return (self.action, self.subject)

    def granted_on(self, subject, identity):
        return self.condition(subject, identity)
