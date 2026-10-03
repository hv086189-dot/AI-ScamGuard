import re
from urllib.parse import urlparse


# Common URL-shortening services
SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly"
]


def analyze_url(url):

    indicators = []
    score = 0

    # Remove common trailing punctuation
    url = url.rstrip(".,!?;:")

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    # Remove username/password portion if present
    if "@" in domain:
        domain = domain.split("@")[-1]

    # --------------------------------
    # 1. HTTP instead of HTTPS
    # --------------------------------

    if parsed.scheme == "http":
        score += 10
        indicators.append("uses_http")


    # --------------------------------
    # 2. IP address instead of domain
    # --------------------------------

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, domain):
        score += 20
        indicators.append("ip_address_url")


    # --------------------------------
    # 3. @ symbol
    # --------------------------------

    if "@" in url:
        score += 20
        indicators.append("at_symbol")


    # --------------------------------
    # 4. Very long URL
    # --------------------------------

    if len(url) > 100:
        score += 10
        indicators.append("very_long_url")


    # --------------------------------
    # 5. URL shortener
    # --------------------------------

    if domain in SHORTENERS:
        score += 15
        indicators.append("url_shortener")


    # --------------------------------
    # 6. Too many subdomains
    # --------------------------------

    if not re.match(ip_pattern, domain) and domain.count(".") >= 3:
        score += 10
        indicators.append("many_subdomains")


    # Maximum URL risk score
    score = min(score, 50)

    return {
        "url": url,
        "score": score,
        "indicators": indicators
    }


# --------------------------------
# Test URLs
# --------------------------------

test_urls = [
    "https://google.com",
    "http://192.168.1.10/login",
    "https://bit.ly/example",
    "http://example.com"
]


print("\n===== URL ANALYSIS TEST =====")

for url in test_urls:

    result = analyze_url(url)

    print("\nURL:", url)
    print("Score:", result["score"])
    print("Indicators:", result["indicators"])