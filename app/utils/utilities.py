class AuthEngine(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(AuthEngine, cls).__new__(cls)
      cls.mongoDb = None
      cls.revokedToken = set()
    return cls.instance