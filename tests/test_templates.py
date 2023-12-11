import glob
import hashlib
import json
import os
import subprocess

import pytest


def checksum(name: str) -> str:
    """Calculate sha256 checksum sum for given file.

    Parameters
    ----------
    name : str
        file name

    Returns
    -------
    str
        sha256 sum for file
    """
    hash_sha256 = hashlib.sha256()

    with open(name, "rb") as fd:
        for chunk in iter(lambda: fd.read(4096), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


revpi_hat_templates = sorted(glob.glob("./revpi-hat-PR*.json"))


@pytest.mark.parametrize("template", revpi_hat_templates)
def test_filename(template: str) -> None:
    """Check if filename matches content."""
    with open(template, "r") as f:
        template_data = json.loads(f.read())

        product_id = template_data["pid"] + 100000
        product_revision = template_data["prev"]

        filename = os.path.basename(template)
        expected_filename = f"revpi-hat-PR{product_id}R{product_revision:02}.json"

        assert filename == expected_filename, (
            f"Template filename ({filename}) does not match expected "
            f"filename ({expected_filename}) based on the product details"
        )


def test_readme() -> None:
    """Check if README is up to date and complies with the format of the helper script."""
    checksum_before = checksum("README.md")
    subprocess.check_call(["python3", "scripts/update-readme.py"])
    checksum_after = checksum("README.md")

    assert (
        checksum_before == checksum_after
    ), "README was not updated or modified without the update-readme.py script"
