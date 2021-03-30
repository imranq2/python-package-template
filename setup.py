# noinspection Mypy
from typing import List, Any

from setuptools import setup, find_packages
from os import path, getcwd

# from https://packaging.python.org/tutorials/packaging-projects/

# noinspection SpellCheckingInspection
package_name = "{{cookiecutter.package_name}}"

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    with open(path.join(getcwd(), "VERSION")) as version_file:
        version = version_file.read().strip()
except IOError:
    raise


def fix_setuptools() -> None:
    """Work around bugs in setuptools.

    Some versions of setuptools are broken and raise SandboxViolation for normal
    operations in a virtualenv. We therefore disable the sandbox to avoid these
    issues.
    """
    try:
        from setuptools.sandbox import DirectorySandbox

        # noinspection PyUnusedLocal
        def violation(operation: Any, *args: Any, **_: Any) -> None:
            print("SandboxViolation: %s" % (args,))

        DirectorySandbox._violation = violation
    except ImportError:
        pass


# Fix bugs in setuptools.
fix_setuptools()


def parse_requirements(file: str) -> List[str]:
    with open(file, "r") as fs:
        return [
            r
            for r in fs.read().splitlines()
            if (
                    len(r.strip()) > 0
                    and not r.strip().startswith("#")
                    and not r.strip().startswith("--")
            )
        ]


requirements: List[str] = parse_requirements("requirements.txt")
test_requirements: List[str] = parse_requirements("requirements-test.txt")

# classifiers list is here: https://pypi.org/classifiers/

# create the package setup
setup(
    name=package_name,
    version=version,
    author="{{cookiecutter.author}}",
    author_email="{{cookiecutter.author_email}}",
    description="{{cookiecutter.package_description}}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="{{cookiecutter.package_github_url}}",
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    dependency_links=[],
    include_package_data=True,
    zip_safe=False,
    package_data={"{{cookiecutter.project_slug}}": ["py.typed"]}
)
