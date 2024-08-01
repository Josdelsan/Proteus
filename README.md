<div align = center>

<img src="https://github.com/user-attachments/assets/936f4820-0017-4da3-a8de-901bccdaf952" width="100" />

# PROTEUS

</div>

PROTEUS is a configurable tool for editing structured documents that can be applied in multiple domains, from software development to legal documents. The main concept in Proteus is the archetype, which is a project, document or object that is used to create others through cloning. It allows you to create preconfigured projects with the necessary documents, documents with already established structure and content, and objects in the documents with default values. Any concept that can be expressed in a conceptual model can become an archetype in Proteus. The archetypes are organized in archetype repositories, so that Proteus is actually a meta-tool since each repository configures Proteus with a set of archetypes specific to a specific domain.

In addition to archetypes, Proteus also offers the possibility of having different views for documents and generating PDF files directly. This flexibility is based on the application of XSLT style sheets extended with Python code, allowing HTML, LaTeX or any other text format to be generated from the objects that make up project's documents, all stored in individual XML files for facilitate version management with tools like Git. The goal is for the user to focus on the content and not the format.

XSLT templates, archetypes repositories and plugins are grouped in profiles. A profile completely change the behaviour of the application based on its content, preparing it for a domain specific task. Plugins enhance XSLT templates allowing complex operations using Python and accessing  backend functionalities. Change the profile from the configuration menu inside the application. Profiles may be included in the application or loaded from a directory.

<div align = center>
  <img src="https://github.com/Josdelsan/proteus-tfg/assets/74303153/3e598ba8-590d-4589-87df-0f1d0d97bcab" width="800" />
</div>

## License
PROTEUS is licensed under the BSD 3-Clause "New" or "Revised" License. See [LICENSE](LICENSE) for more information.

## Installation
PROTEUS is a Python application. It is developed using Python 3.10.7. It is recommended to use a virtual environment to install the application. The application dependencies are listed in the `requirements.txt` file. The application can be installed via `pip install -r requirements.txt`.

## Usage
PROTEUS is executed via `python3 -m proteus` from the top-level application directory.
Tests can be executed via `pytest` from the top-level application directory.

Installation and execution can be performed using the `proteus.bat`script in Windows and the `proteus.sh` script in Linux. Linux users might need to restart ibus via `ibus restart`. Installation of `python3-venv` package is required in Linux.

