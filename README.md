<div align = center>

<img src="https://github.com/Josdelsan/proteus-tfg/assets/74303153/22db167f-c696-4f66-81ab-20250187eb99" width="100" />

# PROTEUS

</div>
Proteus is an archetype-based editor for structured documents. An archetype is an off-the-shelf object, document or project that can be cloned as needed to create new ones. Archetypes are organized into profiles, that can be developed for different domains, from software development to legal documents. Any concept that can be expressed in a conceptual model can become an archetype in Proteus. The archetypes are organized in archetype profiles, so that Proteus is actually a meta-tool since each profile configures Proteus with a set of archetypes from a specific domain.

In addition to archetypes, Proteus also offers the possibility of having different views for documents and generating PDF files directly. This flexibility is based on the application of XSLT style sheets extended with Python code, allowing HTML, LaTeX or any other text format to be generated from the objects that make up project's documents, all stored in individual XML files for facilitating version control with tools like Git. The goal is letting the user focus on the content but not the format.

XSLT templates, archetypes repositories and plugins are grouped in profiles. A profile completely change the behaviour of the application based on its content, preparing it for a domain specific task. Plugins enhance XSLT templates allowing complex operations using Python and accessing advanced functionalities. Progiles can be selected from the configuration menu and may be included in the application or loaded from a external directory.

This application has been developed at the University of Seville (Andalusia, Spain) under the supervision of Professor Amador Durán and with the effort of several students (José Renato Ramos González, José Gamaza Díaz, Pablo Rivera Jiménez and José María Delgado). This version is mainly the evolution of the results of the End-Of-Degree project of José María Delgado."

<div align = center>
  <img src="https://github.com/user-attachments/assets/936f4820-0017-4da3-a8de-901bccdaf952" width="800" />
</div>

## License
PROTEUS is licensed under the BSD 3-Clause "New" or "Revised" License. See [LICENSE](LICENSE) for more information.

## Installation
PROTEUS is a Python application. It is developed using Python 3.10 or 3.11. It does not work with Python 3.12 for the moment. It is recommended to use a virtual environment to install the application. The application dependencies are listed in the `requirements.txt` file.

### Detailed installation instructions

Clone the repository and navigate to the top-level directory of the application.

```bash
git clone https://github.com/Josdelsan/Proteus.git

cd Proteus
```

Create a virtual environment and activate it. You can call it `proteus_env` or any other name. In Windows, it is recommended to use PowerShell instead of CMD.

If you use another Python alias, replace `python` with the correct alias.

```bash
python -m venv proteus_env

source venv/bin/activate # Linux and MacOS
./venv/Scripts/activate # Windows
```

Install the dependencies once the virtual environment is activated.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python -m proteus
```

### Installation scripts

Installation scripts are provided for Windows, Linux and MacOS. The scripts create a virtual environment called `proteus_env`, install the dependencies and run the application. The first time you run the script it will take a while to install the dependencies and create python cache files.

Scripts will look for `python3.11`, `python` and `python3` aliases in that order. It displays the version of Python found, take into account that the application was only tested with Python 3.10 and 3.11. Python 3.12 will be supported in the future.

Windows:
- It is recommended to use de PowerShell script `proteus.ps1`.
- It may be necessary to [change the execution policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3) to allow virtual environment activation.


Linux and MacOS:
- You may need to give execution permissions to the script.
- Since PROTEUS writes logs and configuration files inside the repository directory, it may be also necessary to give write permissions to the repository directory.
- Depending on the system previous configuration, you may need to install `python3-venv` package.
- Some users may need to restart ibus via `ibus restart` the first time they run the application.

**WARNING**, directory names changes may affect the virtual environment. If you encounter any problem, delete the virtual environment and create/run the scripts again.

## Developer features

### XSLT debugging

XSLT debugging features enable XSL files reloading each time the application performs a rendering operation. This feature may impact performance, but prevents the need to restart the application when changes are made to the XSL files. It can be enabled by setting the following variable to `True` in the `proteus.ini` file:
```
xslt_debug_mode = True
```

If an XSLT error occurs, it will be displayed in the document view. It is recommended to check the log files in order to see all the error messages, usually the last error is not relevant enough. There are error that may cause the application to crash, these are usually related to XSL files missing or Python plugins.

### Developer mode

Developer mode enables some features that are useful for archetypes/profiles development.
- Meta-model editor: It is available in the context menu when right-clicking on an object in the document tree. It allows to edit object's properties (add,remove,position,edit) and to edit object's XML attributes like acceptedChildren, classes, etc.
- Store object/document as archetype: Add document or object archetypes, available in the context menu when right-clicking on an object in the document tree. They allow to add archetypes to the current profile.

These features make easier archetypes creation and edition. The whole archetype creation process is not covered yet, icons and translations must be added manually.

Developer mode can be enabled by setting the following variable to `True` in the `proteus.ini` file:
```
developer_features = True
```