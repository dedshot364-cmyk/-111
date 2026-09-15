import json
import pandas as pd

df = pd.read_excel('2_fp.xls')

dates_rows = [8, 30, 52, 74, 96, 118]

pair_times = {
    1: '08:30 - 09:50',
    2: '10:00 - 11:20',
    3: '11:30 - 12:50',
    4: '14:20 - 15:40',
    5: '15:50 - 17:10',
}

pair_offsets = [
    (1, [1, 2, 3]),
    (2, [5, 6, 7]),
    (3, [9, 10, 11]),
    (4, [13, 14, 15]),
    (5, [17, 18, 19]),
]

events = []

for date_row in dates_rows:
    col_dates = {}
    for c in range(4, df.shape[1]):
        val = df.iloc[date_row, c]
        if pd.notna(val):
            dt = pd.to_datetime(val, errors='coerce')
            col_dates[c] = (
                dt.strftime('%Y-%m-%d') if pd.notna(dt) else str(val)[:10]
            )

    for p_num, offsets in pair_offsets:
        time_str = pair_times[p_num]
        for offset in offsets:
            row_idx = date_row + offset
            if row_idx >= len(df):
                continue

            group_val = df.iloc[row_idx, 2]
            if pd.isna(group_val):
                continue

            # Приведение групп вида '101.0' или 101 к чистой строке '101'
            try:
                group_name = str(int(float(group_val)))
            except ValueError:
                group_name = str(group_val).strip()

            for col_idx, date_str in col_dates.items():
                cell_val = df.iloc[row_idx, col_idx]
                if pd.notna(cell_val):
                    text = str(cell_val).strip()
                    if text and text not in ('0', 'nan', 'None'):
                        events.append({
                            'date': date_str,
                            'pair': p_num,
                            'time': time_str,
                            'group': group_name,
                            'text': text,
                        })

with open('schedule.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f'Готово! Извлечено {len(events)} занятий в schedule.json')
