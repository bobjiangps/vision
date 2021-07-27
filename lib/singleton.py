import threading


class Singleton:
    objs = {}
    objs_locker = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls in cls.objs:
            return cls.objs[cls]["obj"]
        cls.objs_locker.acquire()
        try:
            if cls in cls.objs:
                return cls.objs[cls]["obj"]
            obj = object.__new__(cls)
            cls.objs[cls] = {"obj": obj, "init": False}
            setattr(cls, "__init__", cls.decorate_init(cls.__init__))
            obj.__init__(*args)
            return obj
        finally:
            cls.objs_locker.release()
   
    @classmethod
    def decorate_init(cls, fn):
        def init_wrap(*args):
            if not cls.objs[cls]["init"]:
                fn(*args)
                cls.objs[cls]["init"] = True
            return
        return init_wrap
