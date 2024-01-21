# CSV Field Validator

## Prerequisites

Make sure you have Python installed on your system. If not, you can download it from [python.org](https://www.python.org/).

## Step-by-Step Installation Guide

### 1. Open a Terminal or Command Prompt

Open your terminal or command prompt to execute the following commands.

### 2. Install `virtualenv` (if not already installed)

```bash
pip install virtualenv
```

### 3. Create a Virtual Environment

Choose a directory for your project and create a virtual environment:

```bash
python -m venv venv
```

Replace `venv` with your preferred virtual environment name.

### 4. Activate the Virtual Environment

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install Project Dependencies

Once the virtual environment is activated, use `pip` to install your project dependencies:

```bash
pip install -r requirements.txt
```

Replace `requirements.txt` with the actual file containing your project dependencies.

### 6. Deactivate the Virtual Environment

When you're done working on your project, deactivate the virtual environment:

```bash
deactivate
```

## Conclusion

You have successfully set up a virtual environment for your Python project. Activate the virtual environment whenever you work on your project to ensure you are using the correct dependencies.


## Script Execution Guide

### Command to execute field validating script

```bash
python .\script.py <filepath with extension>
```

The command Ex: `python .\script.py .\target.csv` is used to execute a Python script named `script.py` with a specified input or target file, `target.csv`.

Breaking down the command:

- `python`: This is the Python interpreter command. It is used to run Python scripts from the command line.

- `.\script.py`: Here, `.\` represents the current directory, and `script.py` is the name of the Python script you want to run. The script file should be in the same directory from which the command is executed.

- `.\target.csv`: This specifies the input or target file for the Python script. In this case, it's assumed that `target.csv` is the file containing data or information that the Python script will process.

So, when you run this command in the terminal or command prompt, Python will execute the `script.py` script, taking `target.csv` as an argument or input for the script's processing. The specific functionality of the script and the purpose of processing the `target.csv` file would be defined in the script itself.
Open your terminal or command prompt to execute the following commands.

