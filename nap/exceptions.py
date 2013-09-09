# -*- coding: utf-8 -*-


class NapException(Exception):
    def __init__(self, message=None, **kwargs):
        self.message = message if message else self.__class__.__name__
        super(NapException, self).__init__(self.message)

        self.__dict__.update(kwargs)

    def __unicode__(self):
        return unicode(self.__dict__)

    def __str__(self):
        return unicode(self).encode('utf-8')

    __repr__ = __str__

    def to_dict(self):
        return dict(self.__dict__)


class UnsupportedMethodException(NapException):

    def __init__(self, model_name):
        super(UnsupportedMethodException, self).__init__(message='Method not supported.', model_name=model_name)


class ModelNotFoundException(NapException):

    def __init__(self, model_name, model_id):
        super(ModelNotFoundException, self).__init__(message='Model not found.', model_name=model_name, model_id=model_id)


class ModelInvalidException(NapException):

    def __init__(self, model_name, errors):
        super(ModelInvalidException, self).__init__(message='Model is invalid.', model_name=model_name, errors=errors)


class UnauthenticatedException(NapException):

    def __init__(self, model_name):
        super(UnauthenticatedException, self).__init__(message='Unauthenticated.', model_name=model_name)


class UnauthorizedException(NapException):

    def __init__(self, model_name):
        super(UnauthorizedException, self).__init__(message='Unauthorized.', model_name=model_name)
