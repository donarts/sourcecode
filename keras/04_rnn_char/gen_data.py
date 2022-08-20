import pickle

timed_y_data = """
동해 물과 백두산이 마르고 닳도록
하느님이 보우하사 우리나라 만세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
남산 위에 저 소나무, 철갑을 두른 듯
바람 서리 불변함은 우리 기상일세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
가을 하늘 공활한데 높고 구름 없이
밝은 달은 우리 가슴 일편단심일세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
이 기상과 이 맘으로 충성을 다하여
괴로우나 즐거우나 나라 사랑하세.
무궁화 삼천리 화려 강산
대한 사람, 대한으로 길이 보전하세.
"""

timed_y_data = timed_y_data.strip()
timed_y_data = timed_y_data.replace("\n","")
print(timed_y_data)

time_step_size = 4
x_list = []
y_list = []

for xx in range(len(timed_y_data)-time_step_size):
    x_list.append(timed_y_data[xx:xx+time_step_size])
    y_list.append(timed_y_data[xx+time_step_size])

print(x_list)
print(y_list)

char_vocab = sorted(list(set(timed_y_data)))
vocab_size = len(char_vocab)
print(char_vocab)
print(vocab_size)
char_to_index = dict((char, index) for index, char in enumerate(char_vocab))
print(char_to_index)
index_to_char = {}
for key, value in char_to_index.items():
    index_to_char[value] = key
print(index_to_char)

file = open("x_data.txt", "w", encoding="utf-8")
for data in x_list:
    file.write(data)
    file.write("\n")
file.close()

file = open("y_data.txt", "w", encoding="utf-8")
for data in y_list:
    file.write(data)
    file.write("\n")
file.close()

with open('char_to_index.pickle', 'wb') as fw:
    pickle.dump(char_to_index, fw)
with open('index_to_char.pickle', 'wb') as fw:
    pickle.dump(index_to_char, fw)
