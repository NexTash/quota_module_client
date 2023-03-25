from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in quota_module_client/__init__.py
from quota_module_client import __version__ as version

setup(
	name="quota_module_client",
	version=version,
	description="App to Control ERPNEXT Usage",
	author="NexTash",
	author_email="support@nextash.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
