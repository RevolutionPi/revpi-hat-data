import glob
import json
import os

import jsonschema
import pytest
import requests

SCHEMA_URL = "https://gitlab.com/revolutionpi/revpi-hat-eeprom/-/raw/master/docs/eep.schema?ref_type=heads"
SCHEMA_FILENAME = "eep.schema"

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
