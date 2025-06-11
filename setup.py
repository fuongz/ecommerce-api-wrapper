from pathlib import Path

from setuptools import find_packages, setup


about = {}
here = Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

with open(here / "requirements.txt") as fp:
    install_reqs = [r.rstrip() for r in fp.readlines() if not r.startswith("#")]

with open(here / "src/ecommerce_api_wrapper/__version__.py", "r") as f:
    exec(f.read(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="",
    url="https://github.com/fuongz/ecommerce-api-wrapper",
    project_urls={
        "Bug Reports": "https://github.com/fuongz/ecommerce-api-wrapper/issues",
        "Source": "https://github.com/fuongz/ecommerce-api-wrapper",
    },
    license=about["__license__"],
    packages=find_packages("src", exclude=["tests"]),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8, <4",
    install_requires=install_reqs,
)
