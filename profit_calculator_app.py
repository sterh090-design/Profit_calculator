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

# --- Выбор количества ---
quantity = st.radio(
    "Выберите количество SKU для расчета прибыли:",
    ("1 шт", "2 шт")
)

# --- Выбор количества ---
quantity2 = st.radio(
    "Выберите количество SKU для расчета прибыли:",
    ("1 шт", "2 шт")
)


# --- Таблица коэффициентов ---
delivery_table = {i: (1, 0.0000) for i in range(1, 30)}
delivery_table.update({
    30: (1.05, 0.0025), 31: (1.11, 0.0055), 32: (1.16, 0.0080),
    33: (1.23, 0.0115), 34: (1.28, 0.0140), 35: (1.32, 0.0160), 36: (1.36, 0.0180),
    37: (1.40, 0.0200), 38: (1.44, 0.0220), 39: (1.48, 0.0240), 40: (1.51, 0.0255),
    41: (1.54, 0.0270), 42: (1.57, 0.0285), 43: (1.60, 0.0300), 44: (1.63, 0.0315),
    45: (1.66, 0.0330), 46: (1.69, 0.0345), 47: (1.71, 0.0355), 48: (1.73, 0.0365),
    49: (1.75, 0.0375), 50: (1.76, 0.0380), 51: (1.77, 0.0385), 52: (1.774, 0.0387),
    53: (1.78, 0.0390), 54: (1.784, 0.0392), 55: (1.788, 0.0394), 56: (1.79, 0.0395),
    57: (1.792, 0.0396), 58: (1.794, 0.0397), 59: (1.796, 0.0398), 60: (1.798, 0.0399),
})
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
    profit2 = price - total_costs - sku

    data = [
        ["% Озон", f"{ozon_percent*100:.0f}%", ozon_total],
        ["Логистика", "", logistic_total],
        ["Последняя миля", "", last_mile],
        ["Эквайринг", "", acquiring],
        ["Реклама", f"{reklama_percent*100:.0f}%", reklama],
        ["Кросс-док", "", cross_dock],
        ["SKU", "", sku],
        ["Дань", f"{dan_percent*100:.0f}%", dan],
        ["💰 Общие расходы", "", total_costs],
        ["✅ Прибыль", "", profit if quantity == "1 шт" else profit2],
    ]
    
    df = pd.DataFrame(data, columns=["Статья", "Процент", "Сумма (₽)"])
    df["Сумма (₽)"] = df["Сумма (₽)"].map(lambda x: f"{x:.2f}")
    return df

# === Кнопка расчёта ===
if st.button("Рассчитать прибыль"):
    if price <= 0:
        st.error("Введите корректную цену продажи")
    else:
        df = calc_profit(price, avg_time)
        st.table(df)

