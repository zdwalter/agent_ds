---
name: package_manager
description: Package management capabilities using pip (install, uninstall, list, search).
allowed-tools:
  - pip_install
  - pip_uninstall
  - pip_list
  - pip_search
---

# Package Manager Skill

This skill enables the agent to manage Python packages via pip.

## Tools

### pip_install
Install one or more packages using pip.

- `packages`: List of package names (with optional version specifiers).
- `upgrade`: If True, upgrade existing packages (default False).
- `user`: Install to the user site‑directory (default False).

### pip_uninstall
Uninstall packages.

- `packages`: List of package names to remove.
- `yes`: Assume "yes" to confirmation prompts (default True).

### pip_list
List installed packages.

- `outdated`: If True, list only outdated packages (default False).

### pip_search
Search for packages on PyPI.

- `query`: Search term.
- `limit`: Maximum number of results (default 20).

## Dependencies

- pip (already installed with Python)
