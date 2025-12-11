## botscanner: Specialized Web Scanner for Chatbot Pattern Analysis

A Master's Thesis Project for the systematic discovery, identification, and structural analysis of graphical interface patterns within web-integrated chatbots widgets.


### Installation

Prerequisites:

* Python (3.x)
* A  ChromeDriver. Ensure your ChromeDriver is correctly installed and accessible in your system's PATH

```Bash
pip install --upgrade https://github.com/shevandrin/botscanner
```

### Setup

All data defining the heuristic properties and implementation patterns used for chatbot identification and analysis is stored in the YAML file: botscanner/data/patterns.yaml.

Note on Updating Data: There is currently no dedicated function or interface for managing these patterns. To introduce new patterns or modify existing ones, please update the botscanner/data/patterns.yaml file directly using a code or text editor.

### Usage

The core functionality of botscanner is designed for modular integration into custom research scripts or interactive environments like Jupyter notebooks or lab. A dedicated Command-Line Interface (CLI) is currently under development.

### Output

### Authorship and License

This package was developed by Andrey Shevandrin as the practical component of a Master's Thesis at TU Chemnitz.

Author: Andrey Shevandrin

Contact: https://github.com/shevandrin/botscanner/issues

Year: 2025