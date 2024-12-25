# (일본어)웹사이트 글자 사용 분석
import requests
from collections import Counter
from bs4 import BeautifulSoup

# Unicode ranges for grouping by region (examples)
UNICODE_RANGES = {
    "Basic Latin": (0x0000, 0x007F),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    "IPA Extensions": (0x0250, 0x02AF),
    "Spacing Modifier Letters": (0x02B0, 0x02FF),
    "Combining Diacritical Marks": (0x0300, 0x036F),
    "Greek and Coptic": (0x0370, 0x03FF),
    "Cyrillic": (0x0400, 0x04FF),
    "Cyrillic Supplement": (0x0500, 0x052F),
    "Armenian": (0x0530, 0x058F),
    "Hebrew": (0x0590, 0x05FF),
    "Arabic": (0x0600, 0x06FF),
    "Syriac": (0x0700, 0x074F),
    "Thaana": (0x0780, 0x07BF),
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Oriya": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Sinhala": (0x0D80, 0x0DFF),
    "Thai": (0x0E00, 0x0E7F),
    "Lao": (0x0E80, 0x0EFF),
    "Tibetan": (0x0F00, 0x0FFF),
    "Myanmar": (0x1000, 0x109F),
    "Georgian": (0x10A0, 0x10FF),
    "Hangul Jamo": (0x1100, 0x11FF),
    "Ethiopic": (0x1200, 0x137F),
    "Cherokee": (0x13A0, 0x13FF),
    "Unified Canadian Aboriginal Syllabics": (0x1400, 0x167F),
    "Ogham": (0x1680, 0x169F),
    "Runic": (0x16A0, 0x16FF),
    "Khmer": (0x1780, 0x17FF),
    "Mongolian": (0x1800, 0x18AF),
    "Latin Extended Additional": (0x1E00, 0x1EFF),
    "Greek Extended": (0x1F00, 0x1FFF),
    "General Punctuation": (0x2000, 0x206F),
    "Superscripts and Subscripts": (0x2070, 0x209F),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Combining Diacritical Marks for Symbols": (0x20D0, 0x20FF),
    "Letterlike Symbols": (0x2100, 0x214F),
    "Number Forms": (0x2150, 0x218F),
    "Arrows": (0x2190, 0x21FF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "Miscellaneous Technical": (0x2300, 0x23FF),
    "Control Pictures": (0x2400, 0x243F),
    "Optical Character Recognition": (0x2440, 0x245F),
    "Enclosed Alphanumerics": (0x2460, 0x24FF),
    "Box Drawing": (0x2500, 0x257F),
    "Block Elements": (0x2580, 0x259F),
    "Geometric Shapes": (0x25A0, 0x25FF),
    "Miscellaneous Symbols": (0x2600, 0x26FF),
    "Dingbats": (0x2700, 0x27BF),
    "CJK Symbols and Punctuation": (0x3000, 0x303F),
    "Hiragana": (0x3040, 0x309F),
    "Katakana": (0x30A0, 0x30FF),
    "Bopomofo": (0x3100, 0x312F),
    "Hangul Compatibility Jamo": (0x3130, 0x318F),
    "Kanbun": (0x3190, 0x319F),
    "Bopomofo Extended": (0x31A0, 0x31BF),
    "CJK Strokes": (0x31C0, 0x31EF),
    "Katakana Phonetic Extensions": (0x31F0, 0x31FF),
    "Enclosed CJK Letters and Months": (0x3200, 0x32FF),
    "CJK Compatibility": (0x3300, 0x33FF),
    "CJK Unified Ideographs": (0x4E00, 0x9FFF),
    "Hangul Syllables": (0xAC00, 0xD7AF),
    "Private Use Area": (0xE000, 0xF8FF),
    "CJK Compatibility Ideographs": (0xF900, 0xFAFF),
    "Alphabetic Presentation Forms": (0xFB00, 0xFB4F),
    "Arabic Presentation Forms-A": (0xFB50, 0xFDFF),
    "Variation Selectors": (0xFE00, 0xFE0F),
    "Vertical Forms": (0xFE10, 0xFE1F),
    "Combining Half Marks": (0xFE20, 0xFE2F),
    "CJK Compatibility Forms": (0xFE30, 0xFE4F),
    "Small Form Variants": (0xFE50, 0xFE6F),
    "Arabic Presentation Forms-B": (0xFE70, 0xFEFF),
    "Halfwidth and Fullwidth Forms": (0xFF00, 0xFFEF),
    "Specials": (0xFFF0, 0xFFFF)
}

def fetch_webpage_content(url):
    """Fetches the content of a webpage given its URL."""
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text_from_html(html_content):
    """Extracts and returns all text content from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    #return soup.get_text()
    return html_content

def count_unicode_characters(text):
    """Counts the frequency of Unicode characters in a given text."""
    unicode_counts = Counter(text)
    print(unicode_counts)
    return unicode_counts

def analyze_webpages(urls):
    """Analyzes the Unicode character frequency across multiple webpages."""
    total_unicode_counts = Counter()

    for url in urls:
        print(f"Processing {url}...")
        html_content = fetch_webpage_content(url)
        if html_content:
            text = extract_text_from_html(html_content)
            unicode_counts = count_unicode_characters(text)
            total_unicode_counts.update(unicode_counts)

    return total_unicode_counts

if __name__ == "__main__":
    # Example usage
    urls = [
        "https://yahoo.co.jp",
        "https://www.amazon.co.jp",
        "https://rakuten.co.jp",
        "https://google.co.jp",
        "https://ameblo.jp",
        "https://tenki.jp",
        "https://kakuyomu.jp",
        "https://goo.ne.jp",
    ]
    result = analyze_webpages(urls)

    # Sort results by frequency
    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    print("Unicode Character Frequencies:")
    unicode_range_map = {}
    unicode_range_char = {}
    for char, freq in sorted_result:
        find_range = "None"
        # Print readable characters or their Unicode code point
        display_char = char if char.isprintable() else f"U+{ord(char):04X}"
        for name in UNICODE_RANGES:
            start, end = UNICODE_RANGES[name]
            if start <= ord(char) <= end:
                find_range = name
                if unicode_range_map.get(find_range) is None:
                    unicode_range_map[find_range] = 0
                    unicode_range_char[find_range] = []
                unicode_range_map[find_range] += 1
                unicode_range_char[find_range].append(char)
                break
        if find_range is None:
            unicode_range_map[find_range] += 1
        print(f"{display_char}: {freq} : {find_range}")

    print("Summary:")
    for name in UNICODE_RANGES:
        start, end = UNICODE_RANGES[name]
        if unicode_range_map.get(name) == None:
            continue
        print(f"{name}:{start:04X}-{end:04X} : {unicode_range_map.get(name)}")
    if unicode_range_map.get('None') is not None:
        print(f"Known : {unicode_range_map.get('None')}")

    print("Texts:")
    for name in UNICODE_RANGES:
        start, end = UNICODE_RANGES[name]
        if unicode_range_map.get(name) == None:
            continue
        if unicode_range_char[name] is not None:
            print(f"{name}:{start:04X}-{end:04X} : {unicode_range_map.get(name)}")
            print("".join(unicode_range_char[name]))

