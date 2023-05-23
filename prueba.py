from PyQt6.QtWidgets import QTreeWidget, QTabWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from dataclasses import dataclass
from proteus.services.archetype_service import ArchetypeService
from proteus.services.project_service import ProjectService

# --------------------------------------------------------------------------
# Singleton manager
# --------------------------------------------------------------------------
@dataclass
class ServiceManager:
    # Class attributes
    archetype_service: ArchetypeService = None

    @classmethod
    def get_archetype_service_instance(cls) -> ArchetypeService:
        if not cls.archetype_service:
            cls.archetype_service = ArchetypeService()
        return cls.archetype_service


# --------------------------------------------------------------------------
# Decorator
# --------------------------------------------------------------------------
def component(base_cls):
    def decorator_func(cls):
        class Component(cls, base_cls):
            def __init__(self, parent, *args, **kwargs):
                super(base_cls, self).__init__(parent, *args, **kwargs)
                self.archetype_service = ServiceManager.get_archetype_service_instance()

        return Component

    return decorator_func

# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------
@component(QTreeWidget)
class StructureMenu():

    def create_component(self):
        print("Creando el componente")
        print(self.archetype_service.get_project_archetypes())
        print(self.parent)


@component(QTabWidget)
class MenuBar():

    def create_component(self):
        print("Creando el componente")
        print(self.archetype_service)
        print(self.parent)


# --------------------------------------------------------------------------
# Main code
# --------------------------------------------------------------------------

# necesario para que funcione
app = QApplication([])
main_window = QMainWindow()

print(3*"\n")

obj1 = StructureMenu(main_window)
obj1.create_component()
print(obj1.__class__)
# print( issubclass(obj1.__class__, QTreeWidget) )
# print( issubclass(obj1.__class__, QTabWidget) )

print(3*"\n")

obj2 = MenuBar(main_window)
obj2.create_component()
print(obj2.__class__)
# print( issubclass(obj2.__class__, QTabWidget) )
# print( issubclass(obj2.__class__, QTreeWidget) )
