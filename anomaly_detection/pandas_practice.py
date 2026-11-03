import pandas as pd
from log_parse import parse_line


entries = []
with open("access_sample.log", encoding="utf-8") as log_file:
    for line in log_file:
        entry = parse_line(line)
        if entry is not None:  # 깨진 줄은 빼고 담아요.
            entries.append(entry)

df = pd.DataFrame(entries)  # 읽은 로그를 표로 만들어요.

print(pd.DataFrame(entries))

print("--- 로그 첫 5개 ---")
print(df.head())

print("\n--- IP별 요청 횟수 ---")
print(df["ip"].value_counts())

