import glob
import pytest
import json
import os

revpi_hat_templates = sorted(glob.glob("./revpi-hat-PR*.json"))


@pytest.mark.parametrize("template", revpi_hat_templates)
def test_filename(template: str):
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
