# photodup
Find duplicate photos on your computer.

# Step 0

Setup workspace and install requirements.

```shell
pip install -r requirements.txt
```

# Step 1

Create the database structure.

```shell
python db.py
```

This action will create a `photo.db` in workspace.

# Step 2

Run command to scan all photos from somewhere.

```shell
python scan.py dir1 dir2
```

This action will save all photo files(*.jpg only) into database.

# Step2 

Run command to start a webserver to help identify duplicate photos.

```
python web.py
```

Launch browser to http://127.0.0.1:5000 to cleanup duplicate photos.