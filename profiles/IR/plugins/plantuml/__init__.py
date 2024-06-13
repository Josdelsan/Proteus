from plantuml.class_diagram import ClassDiagramGenerator

def register(register_xslt_function, register_qwebchannel_class, register_proteus_component):

    # Class Diagram
    register_xslt_function("generate_class_diagram", ClassDiagramGenerator.create)
    register_proteus_component("classDiagramGenerator", ClassDiagramGenerator)