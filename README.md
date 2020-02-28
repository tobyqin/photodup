# photodup
Find duplicate photos (or any other file types) on your computer. Python 3.x required.

# Step 0

Setup workspace and install requirements.

```shell
pip install -r requirements.txt
```

# Step 1

Create a database for later scanning.

```shell
python db.py
```

This action will create a `photo.db` in workspace.

# Step 2

Run command to scan all photos from somewhere, multiple `dirs` accepted.

```shell
python scan.py dir1 dir2
```

This action will scan all photo files into database (*.jpg by default, check `config.py`).

# Step3 

Run command to start a web page to help you identify duplicate photos / files.

```
python web.py
```

Launch browser to http://127.0.0.1:5001 to cleanup the duplicates. You will be able to clean up files by hash or file name.

![dup_by_hash](web/static/dup_by_hash.png)

![dup_by_name](web/static/dup_by_name.png)

# Auto mode

There is a `auto.py` in repo, it can clean up duplicates more quickly.

Auto mode will help you clean up duplicate files in other folders but keep in main folders, or vice versa.

For example, you have duplicate files:

- c:\photo\1.jpg
- c:\somewhere\1.jpg
- d:\somewhere\1.jpg

when: `main_is_keep = True`:
    This script will **keep files in main** folder (c:\photo) and **cleanup all other files**.

when: `main_is_keep = False`:
    This script will **clean files in main** folder (c:\photo) and **keep all other files**.

Script Usage:
  python auto.py

The clean up rules:

- when keep main, clear all duplicates out of main.
- when clear main, clear all duplicates in main.
