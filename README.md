# Wrangling Helper

## Introduction
![alt text][WranglingHelper.png?raw=true "Wrangling Helper"]

The main idea of this tool, it helping all the RenderFarm Wranglers out there.  
You are able to set automatic wrangling rules, that will autowrang the farm for you.  
You have a to set a list of conditional rules, like:  
* **User is asierra**
* **Dept is Comp**

Or even, you can set several conditional rules at once:  
* **User is asierra & Dept is Comp**

After that, you only have to set how those jobs will be wranglered, like:
* **MachineLimit = 5**
* **Chunk Frames += 5**
* **Priority = 50**
* ...

All jobs that match the rules that you have specified, will be automatically set with the options that you have provided.

## Limitations
* This tool only works with [Deadline](https://www.awsthinkbox.com/deadline). Your Deadline Python Standalone API must be within the `PYTHONPATH` environment variable

## Requeriments
* Only works with Python 2.7, due to Deadline API limitations
* I'm using Qt.py to handle PySide, so you need to install it

## HowTo
It's really easy to start with this tool:
```python
from wrangling_helper import model
model.initialize()
```

## TODOs
* I should expose the Deadline Configuration (RepoHost, RepoPort), to fill up that information without changing the code. This is my number 1 priority now




