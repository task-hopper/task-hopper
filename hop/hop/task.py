class Task():
    def _bootstrap(self, composer, carrot=None):
        self.composer = composer
        self.carrot = carrot

    def stage(self):
        pass

    #  def generate_callback(self, callback_klass, ctx=None):
        #  child_klass = type(self).__name__
        #  cb_klass = callback_klass.__name__
        #  ctx_str = json.dumps(ctx) if ctx else ""
        #  return f"'{child_klass}::{cb_klass}::{ctx_str}'"

    @classmethod
    def patch(cls, func):
        cls.stage = func


class THCallback():
    def __init__(self, ctx):
        pass
        #  self.ctx = json.loads(ctx) if ctx else None

    #  @classmethod
    #  def rebuild_callback(cls, meta):
        #  parent_cls, child_cls, ctx_str = (
            #  re.match(r'\'(.+)::(.+)::(\{.+\})\'', meta).groups()
        #  )

        #  TODO load callbacks

    def execute(self, *args, **kwargs):
        raise NotImplementedError
