# Tools

## Update README (`update-readme.py`)

This script automatically updates the `README.md` file in the repository root.
The content is build by iterating over files matching `revpi-hat-PR*R*.json` and gathering their product information.

### Usage

```
python3 scripts/update-readme.py

# Dont' forget to commit the updated README
# git add README.md
# git commit -s
```

## Create release tag with changelog (`create-tag.py`)

This script is a helper which creates a new annotated GIT tag with a changelog. The changelog contains added template files and also lists updated templates with their respective version numbers.

### Usage

Install dependencies: 
```
pip3 install -r scripts/requirements.txt
```

Run script:
```
python3 scripts/create-tag.py
```
Output:
```
Found 1 changes. The following tag would be created:

----------------------------------------------------------------------
Release 20230404-1

PR100375R00 V1
----------------------------------------------------------------------

In order to proceed please press any key...

Successfully created tag '20230404-1'. Please check the result and don't forget to push tag via 'git push --tags' if everything is ok.
```
