import tomllib

def metadata() -> dict:
    with open("pyproject.toml", "rb") as f:
        metadataaaaaaaaaaaaaaaaaaaaaaaaaaaa = tomllib.load(f)["tool"]["handler"]
    return metadataaaaaaaaaaaaaaaaaaaaaaaaaaaa

# METADATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA