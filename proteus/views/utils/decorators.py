from proteus.services.service_manager import ServiceManager

# --------------------------------------------------------------------------
# Decorator
# --------------------------------------------------------------------------
def component(base_cls):
    def decorator_func(cls):
        class Component(cls, base_cls):
            def __init__(self, parent, *args, **kwargs):
                super().__init__(parent, *args, **kwargs)
                self.parent = parent
                self.archetype_service = ServiceManager.get_archetype_service_instance()
                self.project_service = ServiceManager.get_project_service_instance()

                self.create_component()

        return Component

    return decorator_func