
def get_unicode_ranges(text):
    """
    Returns a list of Unicode ranges (in hexadecimal) or individual code points used in the input text.
    """
    code_points = sorted(ord(char) for char in set(text))
    ranges = []

    # Group consecutive code points into ranges
    start = code_points[0]
    end = code_points[0]

    for i in range(1, len(code_points)):
        if code_points[i] == end + 1:
            # Extend the current range
            end = code_points[i]
        else:
            # Finalize the current range
            if start == end:
                ranges.append(f"{start:04X}")
            else:
                ranges.append(f"{start:04X}-{end:04X}")
            # Start a new range
            start = end = code_points[i]

    # Finalize the last range
    if start == end:
        ranges.append(f"{start:04X}")
    else:
        ranges.append(f"{start:04X}-{end:04X}")

    return ranges
# Test the function
if __name__ == "__main__":
    #text = input("Enter text: ")
    text = r'''
AddTranslation("Set the sales mode. In this state, cards are sold without warning, and cards in the deck are not sold.", "Set the sales mode. In this state, cards are sold without warning, and cards in the deck are not sold.", "판매 모드를 설정를 합니다. 이 상태에서는 경고 없이 카드가 판매되며, 덱에 있는 카드는 판매가 되지 않습니다.", "販売モードを設定します。この状態では、警告なしでカードが販売され、デッキ内のカードは販売されません。");
    '''
    unicode_ranges = get_unicode_ranges(text)

    print("\nUnicode Ranges Used:")
    print(",".join(unicode_ranges))