# Ecommerce API Wrapper - Python SDK

![Codecov](https://img.shields.io/codecov/c/gh/fuongz/ecommerce-api-wrapper?style=for-the-badge&token=1WV304VPMZ)
[![PyPI - Version](https://img.shields.io/pypi/v/ecommerce-api-wrapper?style=for-the-badge)](https://pypi.org/project/ecommerce-api-wrapper/)

This is an unofficial Python SDK for Popular Ecommerce (Tokopedia, Lazada). The project is still under development.

## E-commerce APIs

- [Tokopedia](https://www.tokopedia.com/) - Indonesian e-commerce company
- [Lazada](https://www.lazada.com/)

## Features

- [x] Search products from Tokopedia and Lazada
- [ ] Get product details from Tokopedia and Lazada
- [ ] Get product reviews from Tokopedia and Lazada
- [ ] Get product categories from Tokopedia and Lazada
- [ ] Get product brands from Tokopedia and Lazada

## Libraries used

This project uses the following libraries:

- [requests](https://requests.readthedocs.io/en/master/) for making HTTP requests
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/) for serializing and deserializing JSON data
- [urllib3](https://urllib3.readthedocs.io/en/latest/) for making secure HTTP requests
- [tqdm](https://tqdm.github.io/) for displaying progress bars

## Installation

You can install the package directly from PyPI using pip:

```bash
pip install ecommerce_api_wrapper
```

## Usage

Here is a simple example of how to use the package:

```python
from ecommerce_api_wrapper import EcommerceApiWrapper

if __name__ == "__main__":
    crawler = EcommerceApiWrapper(
        ecom_type="tokopedia",
    )
    response = crawler.search_products(["samsung"])
    print(response)

    # RESULT:
    #
```

## Development

Project Structure

```text
ecommerce_api_wrapper/
├── src/
│   ├── ecommerce_api_wrapper/
│   │   ├── __init__.py
│   │   ├── __version__.py
│   │   ├── ecommerce_api_wrapper.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── lazada_api_wrapper/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── constants.py
│   │   │   │   ├── lazada.py
│   │   │   │   └── schemas/
│   │   │   └── tokopedia_api_wrapper/
│   │   │       ├── __init__.py
│   │   │       ├── constants.py
│   │   │       ├── tokopedia.py
│   │   │       ├── schemas/
│   │   │       └── utils/
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── faker.py
│   │       └── transform.py
├── tests/
│   └── unit_test.py
├── pyproject.toml
├── README.md
└── LICENSE

```

- The `src/ecommerce_api_wrapper` directory contains the package code.
- Each major provider (Lazada, Tokopedia) resides in its own subpackage under `src/ecommerce_api_wrapper/providers`.
- Utility modules are grouped under `utils`.
- Schemas for each provider are organized in their respective `schemas` folders.
- `src/ecommerce_api_wrapper/__init__.py` allows importing the package.
- `tests` contains test cases.

## License

- This project is licensed under the [MIT License](./LICENSE). See the [LICENSE](./LICENSE) file for details.
