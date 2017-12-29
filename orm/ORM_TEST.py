class Field(object):
    def __init__(self, name, colum_type) -> None:
        super().__init__()
        self.name = name
        self.colum_type = colum_type

    def __str__(self) -> str:
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name) -> None:
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):
    def __init__(self, name) -> None:
        super(IntegerField, self).__init__(name, 'bigint')


class ModeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Modle':
            return type.__new__(cls, name, bases, attrs)
        print('Found model:%s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mappings: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModeMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Modle' object has no attribute '%s" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        parms = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            parms.append('?')
            args.append(getattr(self, k, None))
            sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(parms))
            print('SQL:%s' % sql)
            print('ARGS: %s' % str(args))


class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


u = User(id=12345, name='chenlong', email='794400859@qq.com', password='admin')
u.save()
