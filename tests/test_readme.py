import hashlib
import subprocess


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


def test_readme() -> None:
    """Check if README is up to date and complies with the format of the helper script."""
    checksum_before = checksum("README.md")
    subprocess.check_call(["python3", "scripts/update-readme.py"])
    checksum_after = checksum("README.md")

    assert (
        checksum_before == checksum_after
    ), "README was not updated or modified without the update-readme.py script"
