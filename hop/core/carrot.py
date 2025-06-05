class Carrot:
    """
    A base class intended to be inherited from when developing a plugin.
    This class should not be used directly.

    Attributes
    ----------
    configs : Configs
        the loaded `Configs` instance that represents the
        Task Hopper configuration
    loader : LoaderProxy
        the `LoaderProxy` instance that allows limited access
        to the core `Loader` instance
    subparsers : argparse.subparsers
        the subparsers of the main argparse parser
    """
    def _bootstrap(self, *, configs, loader, subparsers):
        self.configs = configs
        self.loader = loader
        self.subparsers = subparsers
