class ServiceContainer:
    _factories = {}
    _instances = {}
    _booted = False

    @classmethod
    def register(cls, key, factory):
        cls._factories[key] = factory

    @classmethod
    def boot(cls):
        cls._booted = True

    @classmethod
    def get(cls, key):
        if not cls._booted:
            raise RuntimeError("Container not booted")

        # Lazy instantiation
        if key not in cls._instances:
            cls._instances[key] = cls._factories[key]()  # create instance only when requested

        return cls._instances[key]