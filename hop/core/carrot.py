class Carrot:
    def _bootstrap(self,*, configs, loader, subparsers):
        self.configs = configs
        self.loader = loader
        self.subparsers = subparsers
