import inspect
import os
import pkgutil

class Carrot(object):
    """Base class that each carrot will inherit from.
    """

    def __init__(self):
        self.description = 'UNKNOWN'

    def perform_operation(self, argument):
        """The main method for all plugins.
        """
        raise NotImplementedError


class CarrotBunch(object):
    """Upon creation, this class will read the carrots package for modules
    that contain a class definition that is inheriting from the Carrot class
    """

    def __init__(self, carrot_package):
        """Constructor that initiates the reading of all available carrots
        when an instance of the CarrotBunch object is created
        """
        self.carrot_package = carrot_package
        self.reload_carrots()

    def reload_carrots(self):
        """Reset the list of all carrots and initiate the walk over the main
        provided carrot package to load all available carrots
        """
        self.carrots = []
        self.seen_paths = []
        print()
        print(f'Looking for carrots under package {self.carrot_package}')
        self.walk_package(self.carrot_package)

    def apply_all_carrots_on_value(self, argument):
        """Apply all of the carrots on teh argument supplied to this function
        """
        print()
        print(f'Applying all carrots on value {argument}:')
        for carrot in self.carrots:
            print(f'    Applying {carrot.description} on value {argument} yields value {carrot.perform_operation(argument)}')

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all carrots
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, carrot_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not is_pkg:
                carrot_module = __import__(carrot_name, fromlist=['blah'])
                cls_members = inspect.getmembers(carrot_module, inspect.isclass)
                for (_, c) in cls_members:
                    if issubclass(c, Carrot) & (c is not Carrot):
                        print(f'    Found carrot class: {c.__module__}.{c.__name__}')
                        self.carrots.append(c())

        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)
