import glob
import json
import os

import jsonschema
import pytest
import requests

SCHEMA_URL = "https://gitlab.com/revolutionpi/revpi-hat-eeprom/-/raw/master/docs/eep.schema?ref_type=heads"
SCHEMA_FILENAME = "eep.schema"

# List of template files, where test_product_version() is skipped
IGNORE_VERSION_CHECK = []

revpi_hat_templates = sorted(glob.glob("./revpi-hat-PR*.json"))


@pytest.fixture(scope="session")
def schema() -> object:
    """Fetch schema file from repo and return schema object.

    Returns
    -------
    object
        schema object
    """
    req = requests.get(SCHEMA_URL, allow_redirects=True)

    return req.json()


@pytest.mark.parametrize("template", revpi_hat_templates)
class TestJsonFiles:
    def test_filename(self, template: str) -> None:
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

    def test_validate_schema(self, template: str, schema: object) -> None:
        """Test JSON file against schema.

        Parameters
        ----------
        template : str
            json template file name
        schema : str
            schema object
        """
        with open(template, "r") as f:
            template_data = json.loads(f.read())

            try:
                jsonschema.validate(template_data, schema=schema)
            except jsonschema.ValidationError as ve:
                pytest.fail("Validation Error: " + str(ve))

    def test_product_version(self, template: str) -> None:
        """Test JSON file against schema.

        Parameters
        ----------
        template : str
            json template file name
        """
        if template in IGNORE_VERSION_CHECK:
            pytest.skip("Ignore version check for " + template)

        _, pr_rev = template[14:-5].split("R")
        expected_product_version = 100 + int(pr_rev)

        with open(template, "r") as f:
            template_data = json.loads(f.read())

            is_development_version = template_data["eeprom_data_version"] == 0

            if template_data["pver"] != expected_product_version:
                error = (
                    "Product version does not match filename: "
                    + f"pver={template_data['pver']}, expected={expected_product_version}"
                )

                if is_development_version:
                    pytest.skip("Ignored during development: " + error)

                pytest.fail(error)
