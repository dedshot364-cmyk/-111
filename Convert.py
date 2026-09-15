import pandas as pd
import json

df = pd.read_excel('2_fp.xls')

# Индексы строк с датами для каждого дня недели
dates_rows = [8, 30, 52, 74, 96, 118]

pair_times = {
    1: {"time": "08:30 - 09:50", "name": "1 пара"},
    2: {"time": "10:00 - 11:20", "name": "2 пара"},
    3: {"time": "11:30 - 12:50", "name": "3 пара"},
    4: {"time": "14:20 - 15:40", "name": "4 пара"},
    5: {"time": "15:50 - 17:10", "name": "5 пара"}
}

events = []

for date_row in dates_rows:
    col_dates = {}
    for c in range(4, df.shape[1]):
        val = df.iloc[date_row, c]
        if pd.notna(val):
            d_str = val.strftime('%Y-%m-%d') if hasattr(val, 'strftime') else str(val)[:10]
            col_dates[c] = d_str
            
    pair_offsets = [
        (1, [1, 2, 3]),
        (2, [5, 6, 7]),
        (3, [9, 10, 11]),
        (4, [13, 14, 15]),
        (5, [17, 18, 19])
    ]
    
    for p_num, offsets in pair_offsets:
        time_info = pair_times[p_num]
        for offset in offsets:
            row_idx = date_row + offset
            if row_idx >= len(df): continue
            
            group_val = df.iloc[row_idx, 2]
            if pd.isna(group_val): continue
            
            group_name = str(int(float(group_val))) if isinstance(group_val, (int, float)) else str(group_val).strip()
            
            for col_idx, date_str in col_dates.items():
                cell_val = df.iloc[row_idx, col_idx]
                if pd.notna(cell_val):
                    text = str(cell_val).strip()
                    if text and text != '0' and text != 'nan':
                        events.append({
                            'date': date_str,
                            'pair': p_num,
                            'time': time_info['time'],
                            'group': group_name,
                            'text': text
                        })

with open('schedule.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f"Готово! Извлечено {len(events)} занятий в schedule.json")
