class TokopediaConstants:
    GRAPHQL_URL = "https://gql.tokopedia.com/graphql"
    REFERER = "https://www.tokopedia.com/"
    TIMEOUT = 3
    READ_TIMEOUT = 5
    MAX_RETRY = 10
    MAX_PAGE = 2
    SLEEP_TIME = 10

    HEADERS = {
        "sec-ch-ua-platform": "macOS",
        "sec-ch-ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
        "x-price-center": "true",
        "sec-ch-ua-mobile": "?0",
        "accept": "*/*",
        "content-type": "application/json",
        "x-version": "bc9586e",
        "x-source": "tokopedia-lite",
        "x-dark-mode": "false",
        "tkpd-userid": "",
        "x-device": "desktop-0.0",
        "DNT": "1",
        "x-tkpd-lite-service": "zeus",
    }

    PATH_SEARCH_PRODUCTS = "SearchProductV5Query"
