# proteus
PROTEUS project directory structure based on ["Dead Simple Python: Project Structure and Imports"](https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6).

Repositoy created at [GitHub](https://github.com) selecting the following options:
* Add a README file (this file)
* Add `.gitignore` using Python template provided by [GitHub](https://github.com)
* Choose a license: `BSD 3-Clause "New" or "Revised" License`, based on the recommendations at [Why your academic code needs a software licence](https://bastian.rieck.me/blog/posts/2020/licence/).

This project is developed using Python 3.10.7 under a virtual environment generated with `python3 -m venv venv` at the top-level application directory.

Package dependencies are in the `requirements.txt` file at the top-level application directory.

After virtual environment activation (operating system dependant), dependencies must be installed via `pip -r install requirements.txt`.

Applicaton must be run via `python3 -m proteus` from the top-level application directory.

Tests must be run via `pytest` from the top-level application directory.


