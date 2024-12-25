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
    if unicode_range_char["CJK Unified Ideographs"] is not None:
        print("CJK Unified Ideographs Text")
        print("".join(unicode_range_char["CJK Unified Ideographs"]))


#Summary:
#Basic Latin:0000-007F : 98
#Latin-1 Supplement:0080-00FF : 3
#General Punctuation:2000-206F : 6
#Letterlike Symbols:2100-214F : 1
#Number Forms:2150-218F : 1
#Arrows:2190-21FF : 1
#Mathematical Operators:2200-22FF : 1
#Enclosed Alphanumerics:2460-24FF : 1
#Box Drawing:2500-257F : 1
#Block Elements:2580-259F : 1
#Geometric Shapes:25A0-25FF : 1
#Miscellaneous Symbols:2600-26FF : 4
#Dingbats:2700-27BF : 2
#CJK Symbols and Punctuation:3000-303F : 18
#Hiragana:3040-309F : 76
#Katakana:30A0-30FF : 81
#CJK Unified Ideographs:4E00-9FFF : 1383
#Variation Selectors:FE00-FE0F : 1
#Halfwidth and Fullwidth Forms:FF00-FFEF : 36
#Specials:FFF0-FFFF : 1
#CJK Unified Ideographs Text
#天日新年気楽報月時話品中見晴人更一連用曇世情界最生載作地間大小説公料開無予画子知本転分雪事方結代場会意検覧注異完県全像雨定女記出前関愛物選入合文上国家器済現索商特集始有約象電水式通行金東魔俺市実恋力産者能円買目表高今使所書美取利車北外手山週得自読探役法登動以社信保海機様規投悪別主名録死具計運士設題安心土強化田険感風解識要発花庫星二族版道体配容明後食対応介性次移納変部線語正総送歴示着加空放込夫稿冬除節創学台来験季貴洗雲伝嬢王師売都業店理広販超平回指好編原野止葉初協直朝図銀比度近音紹極不受的提言島震論横降税問籍旅暮較積口評戦神冷字万落点夜長令毎便遷内波布香収酒男和災木募真頃省元休短告住員術教白防数育炊切他況末急値向光競各達寝芸活決賞専私破終下購務立付域限試周組津去過阪撃累夢件輸藤価資充期何謝京味装婚反型福門催率温賀氏断思束必証退貯観宅額優雑医失剤多飯供熱占童視申求底粉戸村宮岡続帰夏良町衛寒身史参虚双鮮効府将番券馬損太当位辺房健調速屋児想確企流在由徹区奇詩可染司訴境客引命座費南履焼再工濯鍋蔵郵違念持石策幸春満河了少症測存華乙億殺未須展恵百条号掲割削薬菓経届紅顔輪科改写漫歌眠増髪十戻西雷路四川重松成先幼馴霊亡詳委格井洋待獲誌康護敗追覚豊奈富三球団技職聴認願個素婦渡親麗千剣相豪火影兵佐監友駆八幕議刑僕害宇遺角塚声故端尋独揃融施倍靴財類援消古飾民宿簡単適歳贈局面案針善塾泣油羽港圧救両振返疲息基紫邪暖那響荒城張政陽冒謙堅努滅裏同黒属呼緑勝復讐志判譚居罪宙巨軍谷駅標館校忘背株概採級迷半量沢貨腕択挙菜梅果飲印仕室掛敷修快頭倒処甘第歩睡義趣岩夕闘服霜畿算側並旧聖領考爵陰固避勇七否徒園焦突奪導姫浜娘織痛摘庁交賠償査袋準昇瑠免項宝括閉際酎肌我米種酸玩習凍舗典置抱材備究絵暗停請欲却歯静豆進綺猛暑團希常談警差飛散潟鹿九州沖縄崩形彼畜肥禁才秀許執拒非劇幻英雄詰紀笑御君勤含虎労営堀犯俳寿還治兆推環犬継討責窓湾祭筋湿抜鑑勢鏡精魚製茶赤柔軟掃箱即軽管祝猫帯植喫就映託街係簿徴枚媛倉伊坂郎脳浴液深院嬉妊娠躍残剛彩芽隈右辻貰斗晶尽青黄砂傘艇釣桜枠札幌釧仙覇甲陸低氷秋玉崎細旦板奴頑敵伏舞怪状態折余裕鋼章仲跡孤系鬱久抗争色純騎魅被謀紡壊賭囚獄昔練嫁誰既垢支脇功隊似絶補共浩蛍辞押減炎驚湘奨斎授諮涙聞秒挑扇眼肉乳炭耗仏弁扱乗紙枕講仮奏制航等泊透審任稼鹸塩革磨清浄草湊圭吾樹薄宰鼻酔粧包丁奮暴走栄献射至森茨梨鳥曜隷站唱禍祓伯舟匿慢又誘拐筆蒼歪碧悩騒拾母俗浮翌働幹衰巻錬難模勉察駄萌頼召喚麻囲芯遭晨伽鬼逢若課賊武博宵瞳咲略描滝苦逐媒妖暁鈴浪訓籠船皇兄溺妹竿埋構漢袖襟寺忠帝句棚遼騙隣堂狼巡興嗜替滑承輝敦彦擢到沈黙捜因困荷鉄列般琴漏整撮病寂曲権暫濃攻傑打搭縮昨丹与永贅訳旬叶狙該恐守寄宏帽兼穀麺惣漬干泡壇筒膳厨操泳畳照壁毛農建築研鉢造飼衣冠葬刷骨董煙吹弦票療払拠複肢望顧促及訪延洒貼酬揺養滴乾燥覆昼伴沿央埼栃群岐阜滋根徳熊偽侍棄姿赦卯瑛珠瘴狂紛律嘘卜涼泉孫刻弟杯途珍謎邂逅怒餅餠浅序盤席妙芳闇粋憧誠瀬莉乃林妄椎秘遇酷馨露毒柊彰鉱脱鋸鎚怖励槍醒負普刀尉冥榮程毘沙艦蔑皆輩虹喜朗嶺諦裸副燃梢絡澤誤致克逆蛮軒尾怠惰塔歓迎俊哉爽契佳誕浦悠霧著微慶携呈貸均靖綿肺訟控衝拡惑預械候飽輔愕踏緯菅五毅鎮烈吉李首緊厚債泰倫衆咳諭逮捕塗仰例早威嚇血芦接触官遥畑庭招賑璧源弾潤萎騰跳悲斉芝慎匠架益汚換旨勧激絞頂
