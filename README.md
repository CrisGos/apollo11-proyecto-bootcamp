## Classes

# FileManager

Manages file operations.

:param logClass: Class providing logging functionality.
:type logClass: class

# DeviceFileManager

Manages device-specific file operations.

This class extends FileManager to handle device-specific file operations such as simulating data, generating reports,
and managing disconnections.

:param FileManager: Class providing file management functionality.
:type FileManager: class

# Apolo11Simulator

Simulates the operation of the Apollo 11 devices (Main Class).

:param DeviceFileManager: Class providing device file management functionality.
:type DeviceFileManager: class
:param logClass: Class providing logging functionality.
:type logClass: class

# Functions

# log_event

Decorator to log events.

:param func: The function to be decorated.
:type func: function

inside:

Wrapper function to log events.

:return: The result of the decorated function.
:rtype: Any

# limpiar_archivos_procesados

Moves processed files to the backup directory.

Clears out processed files from the devices directory and moves them to a backup directory with a timestamped folder name.

#

#

## flake8

poetry run flake8 apolo11

## Run project

poetry run apolo11

<a name="readme-top"></a>

# Proyecto Apollo 11

> Program that generates analysis of aerospace devices and their functionality status, producing periodic analyses and reports of their condition. Additionally, it generates alerts for any new developments that arise.

## Built With

- Python

## Live Demo (if available)

[Portfolio](git@github.com:CrisGos/apollo11-proyecto-bootcamp.git)

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

--Poetry
--OS
--Pandas
--Text editor (VsCode)

### Install

1. Clone the repo
   ```sh
   git clone git@github.com:CrisGos/apollo11-proyecto-bootcamp.git
   ```
2. Install packages

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage

1.Run project

```poetry run apolo11

```

## Authors

👤 **Cristian Gabriel Ortega Saldarriaga**

- GitHub: [@CrisGos](https://github.com/CrisGos)
- LinkedIn: [LinkedIn](https://www.linkedin.com/in/cristian-ortega-saldarriaga/)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](git@github.com:CrisGos/apollo11-proyecto-bootcamp.git).

## Show your support

Give a ⭐️ if you like this project!

## Acknowledgments

Luis Vazquez
Kaylee Paez
Santiago Isazaar
