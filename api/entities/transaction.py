class Transaction():
    def __init__(self, name, description, value, kind, account):
        self.__name = name
        self.__description = description
        self.__value = value
        self.__kind = kind
        self.__account = account


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def kind(self):
        return self.__kind

    @kind.setter
    def kind(self, kind):
        self.__kind = kind

    @property
    def account(self):
        return self.__account

    @account.setter
    def kind(self, account):
        self.__account = account
