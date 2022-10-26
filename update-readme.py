import glob
import json

revpi_hat_templates = sorted(glob.glob('./revpi-hat-PR*.json'))


readme = """# revpi-hat-eeprom-files

Device specific JSON templates for RevPi HAT EEPROM generation

| Device | Product Id | Product Revision | Devicetree Overlay |
| ------ | ---------- | ---------------- | ------------------ |
"""

for template in revpi_hat_templates:
    with open(template, 'r') as f:
        template_data = json.loads(f.read())

        name = template_data["pstr"]
        product_id = template_data["pid"] + 100000
        product_revision = template_data["prev"]
        overlay = template_data["dtstr"]

        pr = f"PR{product_id}R{product_revision:02}"

        readme += f"| [{name }]({template}) | PR{product_id} | R{product_revision:02} | {overlay} |\n"


with open("README.md", "w") as f:
    f.write(readme)
