# aimedic ![](https://github.com/ibukun-brain/aimedic/workflows/CI/badge.svg)

<!-- ## Useful links

- [Github repo](https://github.com/ibukun-brain/aimedic)
<!-- - [Theme](https://codescandy.com/coach/bootstrap-5/index.html) -->

## Requirements

- Python / Django 4.2

## Project setup

If not using docker, you can setup a virtual environment using the command below

```sh
python -m venv env
```

then activate it with

```sh
./env/Scripts/activate   # windows or
source env/bin/activate  # linux or mac
```

## Install required packages

Run the command below

```sh
python -m pip install -r requirements-dev.txt
```

Once the virtual environment has been activated, install the necessary requirements by using the command below

```sh
python manage.py migrate
```

## Database backups and restore

Sometimes you may want to delete your database but don't want to lose your data. To do this, run the following script

## Backup command

```sh
python -Xutf8 manage.py dumpdata --natural-primary --exclude=contenttypes --exclude=auth.permission --exclude=admin.logentry --exclude=sessions.session > ../data.json
```

## Restore command

```sh
python manage.py loaddata ../data.json
```

## Important steps

### Pre development

- Go to the Github issues (https://github.com/ibukun-brain/aimedic/issues/)
- In the `selected for development` lane, choose a ticket an assign to yourself
- Move the chosen ticket to in progress
- Create a branch in your local pc but branching from the develop branch.

```sh
git checkout -b aimedic-1/lowercased-short-description
```

### Dev complete

- Once coding is done, run `git commit -m "short description"`
- run the `scripts.sh` script.
- Alternatively, you can manually run the commands below

```sh
pylint $(git ls-files '*.py')
flake8
python manage.py test --keepdb -v 2
```

- If successful, `git push` your code to Github
- Create a merge request using the link generated from the terminal

### Dev complete

- Notify two colleagues to perform code reviews
- If code review is successful, merge to develop and move ticket to `closed` lane on Github

## Contribution

Pick a ticket on the [Github Repository](https://github.com/ibukun-brain/aimedic). If you haven't cloned the repository, use the command to clone from the terminal

```sh
git clone https://github.com/ibukun-brain/aimedic
```

When creating a new branch, **ENSURE** that the branch name starts with the format **SSS-&lt;issue-no&gt;-&lt;short-description&gt;** e.g. **aimedic-1-project-setup** and the main branch is from develop. use the command below when creating a new branch.

```
git checkout develop
git branch -b <branch name>
```

Before creating a pull request, run the commands and fix any warning/errors encountered

```
sh ./scripts.sh

git add .
git commit -m "my commit message"
git push -u origin <branch name>
```

> **Note:** You will need to have isort, autopep8, black and pylint installed for this to work and you can install it using the commands below.

```sh
python -m pip install autopep8 pylint isort flake8
```

When creating a pull request, please select the target branch as `develop`.

- After writing your code, make sure to run the `scripts.sh` file and **ENSURE** it passes before pushing to the git repository. Use the command below to run the test.

```sh
sh ./scripts.sh
```

## Pushing to the repository

Run the following command

```sh
 # if pushing for the first time
$ git push -u origin <branchname>

# if pushing normally
$ git push
```

## Installing make

```sh
# Install make on windows
choco install make

# Linux or mac
sudo apt install make
```

## Using make command

- Export database content as json for backup purposes

```sh
make backup
```

- Creates a virtual environment in current working directory

```sh
make env
```

- Fixes your database if it gets corrupted. Creates a backup and also restore current data

```sh
make fixdb
```

- Displays help text on how to use the makefile

```sh
make help
```

- Syncs the project dependencies

```sh
make install
```

- Checks if code is conforming to best practices like PEP8

```sh
make lint
```

- Runs makemigrations and migrate commands

```sh
make migrate
```

- Pushes committed changes to the Github remote repository

```sh
make push
```

- Loads previously backed up data into the database

```sh
make restore
```

- Spawns the Django server

```sh
make server
```

- Runs unit test

```sh
make test
```

- Syncs the project dependencies

```sh
make update
```
