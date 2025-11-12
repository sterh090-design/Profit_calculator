import streamlit as st
import pandas as pd

st.set_page_config(page_title="Калькулятор прибыли", page_icon="💰", layout="centered")

st.title("💰 Калькулятор прибыли")
st.caption("Простой онлайн-калькулятор по аналогии с Excel")

# === Ввод данных ===
price = st.number_input(
    "Введите цену продажи (₽):", 
    min_value=1.0, 
    step=1.0
)

avg_time = st.number_input(
    "Введите среднее время доставки (ч):", 
    min_value=1,      
    max_value=100,    
    step=1
)

# --- Таблица коэффициентов ---
delivery_table = {
    1: (1, 0.0000), 2: (1, 0.0000), 3: (1, 0.0000), 4: (1, 0.0000),
    5: (1, 0.0000), 6: (1, 0.0000), 7: (1, 0.0000), 8: (1, 0.0000),
    9: (1, 0.0000), 10: (1, 0.0000), 11: (1, 0.0000), 12: (1, 0.0000),
    13: (1, 0.0000), 14: (1, 0.0000), 15: (1, 0.0000), 16: (1, 0.0000),
    17: (1, 0.0000), 18: (1, 0.0000), 19: (1, 0.0000), 20: (1, 0.0000),
    21: (1, 0.0000), 22: (1, 0.0000), 23: (1, 0.0000), 24: (1, 0.0000),
    25: (1, 0.0000), 26: (1, 0.0000), 27: (1, 0.0000), 28: (1, 0.0000),
    29: (1, 0.0000), 30: (1.05, 0.0025), 31: (1.11, 0.0055), 32: (1.16, 0.0080),
    33: (1.23, 0.0115), 34: (1.28, 0.0140), 35: (1.32, 0.0160), 36: (1.36, 0.0180),
    37: (1.40, 0.0200), 38: (1.44, 0.0220), 39: (1.48, 0.0240), 40: (1.51, 0.0255),
    41: (1.54, 0.0270), 42: (1.57, 0.0285), 43: (1.60, 0.0300), 44: (1.63, 0.0315),
    45: (1.66, 0.0330), 46: (1.69, 0.0345), 47: (1.71, 0.0355), 48: (1.73, 0.0365),
    49: (1.75, 0.0375), 50: (1.76, 0.0380), 51: (1.77, 0.0385), 52: (1.774, 0.0387),
    53: (1.78, 0.0390), 54: (1.784, 0.0392), 55: (1.788, 0.0394), 56: (1.79, 0.0395),
    57: (1.792, 0.0396), 58: (1.794, 0.0397), 59: (1.796, 0.0398), 60: (1.798, 0.0399),
}

# добавляем 61–100
delivery_table.update({i: (1.8, 0.0400) for i in range(61, 101)})

def calc_profit(price, avg_time):
    # --- % Озон ---
    if price < 100:
        ozon_percent = 0.14
    elif price > 299:
        ozon_percent = 0.39
    else:
        ozon_percent = 0.20
    ozon_total = price * ozon_percent

    # --- Логистика ---
    coef, percent = delivery_table.get(avg_time, (1, 0))
    logistic_total = 56 * coef + price * percent

    # --- Остальные расходы ---
    last_mile = 2.5
    acquiring = 8.99
    reklama_percent = 0.15
    reklama = price * reklama_percent
    cross_dock = 12
    sku = 47
    dan_percent = 0.07
    dan = price * dan_percent

    # --- Итог ---
    total_costs = (
        ozon_total + logistic_total + last_mile + acquiring +
        reklama + cross_dock + sku + dan
    )
    profit = price - total_costs

    data = [
        ["% Озон", f"{ozon_percent*100:.0f}%", f"{ozon_total:.2f}"],
        ["Логистика", "", f"{logistic_total:.2f}"],
        ["Последняя миля", "", f"{last_mile:.2f}"],
        ["Эквайринг", "", f"{acquiring:.2f}"],
        ["Реклама", f"{reklama_percent*100:.0f}%", f"{reklama:.2f}"],
        ["Кросс-док", "", f"{cross_dock:.2f}"],
        ["SKU", "", f"{sku:.2f}"],
        ["Дань", f"{dan_percent*100:.0f}%", f"{dan:.2f}"],
        ["💰 Общие расходы", "", f"{total_costs:.2f}"],
        ["✅ Прибыль", "", f"{profit:.2f}"],
    ]

    df = pd.DataFrame(data, columns=["Статья", "Процент", "Сумма (₽)"])

    # --- Определяем цвет строки "Прибыль" ---
    last_row_color = "red" if profit < 0 else "yellow" if profit <= 20 else "green"

    # --- Генерируем HTML ---
    html = '<table style="border-collapse: collapse; width: 100%;">'
    html += '<tr><th style="min-width:180px;text-align:left;">Статья</th><th style="min-width:60px;">Процент</th><th style="min-width:80px;">Сумма (₽)</th></tr>'
    for i, row in df.iterrows():
        color = last_row_color if i == 9 else "white"  # только 10-я строка
        html += f'<tr style="background-color:{color};"><td>{row["Статья"]}</td><td>{row["Процент"]}</td><td>{row["Сумма (₽)"]}</td></tr>'
    html += '</table>'

    return html

# === Кнопка расчета ===
if st.button("Рассчитать прибыль"):
    if price <= 0:
        st.error("Введите корректную цену продажи")
    else:
        html_table = calc_profit(price, avg_time)
        st.markdown(html_table, unsafe_allow_html=True)
