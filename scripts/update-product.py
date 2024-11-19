#!/usr/bin/env python3

import argparse
import glob
import json
import os
import sys
from typing import Optional

PRODUCT_ID_BASE = 100000
FILE_PATTERN = "revpi-hat-PR{product_id}R{revision}.json"


def find_latest_revision(product_id: int) -> Optional[int]:
    """Find latest revision of a hat template for a given product id."""
    filename = FILE_PATTERN.format(product_id=product_id, revision="*")
    hat_files = sorted(glob.glob(filename))

    if not hat_files:
        return None

    last_filename = hat_files[-1]
    _, revision = last_filename.rsplit("R", maxsplit=1)
    revision = int(revision.replace(".json", ""))

    return revision


def update_template(
    template: dict,
    vendor: str = None,
    name: str = None,
    product_id: int = None,
    revision: int = None,
) -> None:
    """Update template dict with provided values."""
    if name is not None:
        template["pstr"] = name

    if vendor is not None:
        template["vstr"] = vendor

    if product_id is not None:
        if product_id > PRODUCT_ID_BASE:
            product_id -= PRODUCT_ID_BASE
        template["pid"] = product_id

    if revision is not None:
        template["prev"] = revision
        template["pver"] = 100 + revision


class ProductFileNotFoundException(Exception):
    def __init__(self, filename: str):
        super().__init__(f"Cannot find hat template: {filename}")
        self.filename = filename


class HatTemplate:
    def __init__(self, product_id: int, revision: int):
        self.product_id = product_id
        self.revision = revision
        self.content = None

    @property
    def filename(self) -> str:
        return FILE_PATTERN.format(
            product_id=self.product_id, revision=f"{self.revision:02d}"
        )

    def exists(self) -> bool:
        return os.path.exists(self.filename)

    def load(self) -> None:
        """Load json content of hat template from file."""
        if not self.exists():
            raise ProductFileNotFoundException(self.filename)

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.content = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from {self.filename}: {e}")

    def save(self) -> None:
        """Save json content of hat template to file."""
        if self.content is None:
            raise ValueError("Content is empty. Nothing to save.")

        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.content, file, indent=4)
                # add final empty line
                file.write("\n")
        except IOError as e:
            raise IOError(f"Error writing to {self.filename}: {e}")

    def copy_to(
        self,
        product_id: int,
        revision: int,
        name: str = None,
        vendor: str = None,
        *,
        override: bool = False,
    ) -> "HatTemplate":
        """Copy an existing hat template into a new one."""
        if self.product_id == product_id and self.revision == revision:
            raise ValueError("Cannot copy to same product id and revision")

        # check if a template with the new id and revision already exists
        new_template = HatTemplate(product_id, revision)
        if new_template.exists() and not override:
            raise FileExistsError(
                f"hat template {new_template.filename} already exists. Use --force to override"
            )

        # Copy actual content, because a dict is mutable
        new_template.content = self.content.copy()

        # Update content, dict is mutable and will be modified in the update function
        update_template(
            new_template.content,
            vendor=vendor,
            name=name,
            product_id=product_id,
            revision=revision,
        )

        if new_template.content["version"] > 1:
            # Ensure a new revision starts with version 1
            new_template.content["version"] = 1

        return new_template

    @classmethod
    def find(
        cls: "HatTemplate", product_id: int, revision: Optional[int] = None
    ) -> Optional["HatTemplate"]:
        """Try to find hat template by product id and optional revision (latest if none provided)."""
        if revision is None:
            # revision was not specified, try to find existing revision
            revision = find_latest_revision(product_id)

        if revision is None:
            # no existing revision found
            return None

        template = cls(product_id, revision)

        if not template.exists():
            return None

        return template


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_id", metavar="product-id", type=int)
    parser.add_argument("new_product_id", metavar="new-product-id", nargs="?", type=int)
    parser.add_argument("-r", "--revision", type=int, required=False)
    parser.add_argument("-n", "--new-revision", type=int, required=False)
    parser.add_argument("-p", "--new-product-name", type=str, required=False)
    parser.add_argument("-m", "--new-product-vendor", type=str, required=False)
    parser.add_argument(
        "-s",
        "--short-product-ids",
        action="store_true",
        default=False,
        required=False,
        help="Auto complete short product ids (e.g. 123 will be expanded to 100123)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", default=False, required=False
    )

    args = parser.parse_args()

    if args.product_id < PRODUCT_ID_BASE and args.short_product_ids:
        print(
            "Detected short product id. Product id will be updated "
            f"from {args.product_id} to {args.product_id + PRODUCT_ID_BASE}"
        )
        args.product_id += PRODUCT_ID_BASE

    try:
        template = HatTemplate.find(args.product_id, args.revision)

        if template is None:
            raise Exception("HAT template for product is missing")

        template.load()

        new_product_id = (
            args.new_product_id if args.new_product_id is not None else args.product_id
        )
        if new_product_id < PRODUCT_ID_BASE and args.short_product_ids:
            print(
                "Detected short new product id. New product id will be updated "
                f"from {new_product_id} to {new_product_id + PRODUCT_ID_BASE}"
            )
            new_product_id += PRODUCT_ID_BASE

        new_revision = (
            args.new_revision
            if args.new_revision is not None
            else template.revision + 1
        )

        new_template = template.copy_to(
            new_product_id,
            new_revision,
            vendor=args.new_product_vendor,
            name=args.new_product_name,
            override=args.force,
        )
        new_template.save()

    except Exception as e:
        print("ERROR:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
