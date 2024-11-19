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

## Create new product file / update revision

```
usage: update-product.py [-h] [-r REVISION] [-n NEW_REVISION] [-p NEW_PRODUCT_NAME] [-m NEW_PRODUCT_VENDOR] [-f] product-id [new-product-id]

positional arguments:
  product-id
  new-product-id

options:
  -h, --help            show this help message and exit
  -r REVISION, --revision REVISION
  -n NEW_REVISION, --new-revision NEW_REVISION
  -p NEW_PRODUCT_NAME, --new-product-name NEW_PRODUCT_NAME
  -m NEW_PRODUCT_VENDOR, --new-product-vendor NEW_PRODUCT_VENDOR
  -f, --force
```

### Create new product revision based on latest active revivsion

In order to create a new revision of a product with id `123456`, the following command can be used:

```
python3 scripts/update-product.py 123456
```

Optionally the target revision can be provided with `-n <REVISION>`. 

### Create new product based on an existing template

To create a new product template with id `100123`  based on the product id `123456` with revision `42` run this:

```
python3 scripts/update-product.py -r 42 123456 100123
```

Optionally a target revision for the new template can be provided with `-n <REVISION>`.
Also the product name (`-p <PRODUCT NAME>`) and vendor  (`-m <PRODUCT NAME>`) can be altered.
