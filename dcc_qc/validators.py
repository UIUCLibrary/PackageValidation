import abc


class AbsFactory(metaclass=abc.ABCMeta):

    @abc.abstractstaticmethod
    def check_technical():
        pass

    @abc.abstractstaticmethod
    def check_metadata():
        pass

    @abc.abstractstaticmethod
    def check_completeness():
        pass