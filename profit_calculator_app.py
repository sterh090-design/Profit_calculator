import streamlit as st
import pandas as pd

st.set_page_config(page_title="Калькулятор прибыли", page_icon="💰", layout="centered")

st.title("💰 Калькулятор прибыли")
st.caption("Простой онлайн-калькулятор для помощи в акциях")

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

# # --- Выбор количества ---
# quantity = st.radio(
#     "Выберите количество SKU для расчета прибыли:",
#     ("1 шт", "2 шт")
# )

# --- Выбор SKU ---
sku_type = st.radio(
    "SKU для расчета прибыли:",
    #("Беж247","Слк247",
     ("Бпбеж027","Бполив027","Бпчер027",)
)


# --- Таблица коэффициентов ---
delivery_table = {i: (1, 0.0000) for i in range(1, 30)}
delivery_table.update({
    30: (1.05, 0.0025), 
    31: (1.11, 0.0055), 
    32: (1.16, 0.0080),
    33: (1.23, 0.0115), 
    34: (1.28, 0.0140), 
    35: (1.32, 0.0160), 
    36: (1.36, 0.0180),
    37: (1.40, 0.0200), 
    38: (1.44, 0.0220), 
    39: (1.48, 0.0240), 
    40: (1.51, 0.0255),
    41: (1.54, 0.0270), 
    42: (1.57, 0.0285), 
    43: (1.60, 0.0300), 
    44: (1.63, 0.0315),
    45: (1.66, 0.0330), 
    46: (1.69, 0.0345), 
    47: (1.71, 0.0355), 
    48: (1.73, 0.0365),
    49: (1.75, 0.0375), 
    50: (1.76, 0.0380), 
    51: (1.77, 0.0385), 
    52: (1.774, 0.0387),
    53: (1.78, 0.0390), 
    54: (1.784, 0.0392), 
    55: (1.788, 0.0394), 
    56: (1.79, 0.0395),
    57: (1.792, 0.0396), 
    58: (1.794, 0.0397), 
    59: (1.796, 0.0398), 
    60: (1.798, 0.0399),
})
delivery_table.update({i: (1.8, 0.0400) for i in range(61, 101)})

def calc_profit(price, avg_time, sku_type):
    # --- % Озон ---
    if price < 100:
        ozon_percent = 0.14
    elif price > 299:
        ozon_percent = 0.39
    else:
        ozon_percent = 0.20
    ozon_total = price * ozon_percent


#Считаем логистику
  # --- Логистика (CASE WHEN) ---
    if sku_type in ("Бпбеж027", "Бполив027", "Бпчео027"):
        logistic_baza = 27 if price < 300 else 56
    elif sku_type in ("Беж247", "Слк247"):
        logistic_baza = 27 if price < 300 else 56
    else:
        logistic_baza = 56


# Продукты "Беж247", "Слк247" идут по 2 штуки
    if sku_type in ("Беж247", "Слк247"):
        sku = 45 * 2
    else:
        sku = 45

    # --- Логистика по времени ---
    coef, percent = delivery_table.get(avg_time, (1, 0))
    logistic_total = logistic_baza * coef + price * percent
    
    
    # --- Остальные расходы ---
    last_mile = 3
    acquiring = 3
    reklama_percent = 0.15
    reklama = price * reklama_percent
    cross_dock = 16
    dan_percent = 0.07
    dan = price * dan_percent
    premium = 5.5 

    # --- Итог ---
    total_costs = (
        ozon_total + logistic_total + last_mile + acquiring +
        reklama + cross_dock + sku + dan + premium
    )

    profit = price - total_costs
  
    data = [
        ["% Озон", f"{ozon_percent*100:.0f}%", ozon_total],
        ["Логистика",  f"{logistic_baza} × {coef} + {price} × {percent}", logistic_total],
        ["Последняя миля", "", last_mile],
        ["Эквайринг", "", acquiring],
        ["Реклама", f"{reklama_percent*100:.0f}%", reklama],
        ["Кросс-док", "", cross_dock],
        ["SKU", "", sku],
        ["Ozon Premium", "", premium],
        ["Дань", f"{dan_percent*100:.0f}%", dan],
        ["💰 Общие расходы", "", total_costs],
        ["✅ Прибыль", "", profit],
    ]
    
    df = pd.DataFrame(data, columns=["Статья", "Процент", "Сумма (₽)"])
    df["Сумма (₽)"] = df["Сумма (₽)"].map(lambda x: f"{x:.2f}")
    return df

if st.button("Рассчитать прибыль"):
    if price <= 0:
        st.error("Введите корректную цену продажи")
    else:
        # Получаем таблицу с расходами и прибылью
        df = calc_profit(price, avg_time, sku_type)
        st.table(df)
        
        # Извлекаем прибыль из таблицы
        profit = float(df.loc[df["Статья"] == "✅ Прибыль", "Сумма (₽)"].values[0].replace(",", ""))
        
        # --- Эффекты в зависимости от прибыли ---
        if 20 < profit < 40:
            # 🎉 Салют
            st.balloons()
        elif profit < 0:
            # ⚠️ Мигающее предупреждение с 7 смайлами
            st.markdown(
                """
                <div style="text-align: center;">
                    <h3 style="color:red; animation: blink 1s infinite;">
                        ⚠️ Так не пойдет! Надо работать эффективнее! ⚠️
                    </h3>
                    <p style="font-size:2rem; animation: blink 1s infinite;">😱😱😱😱😱😱😱</p>
                </div>
                <style>
                    @keyframes blink { 50% { opacity: 0; } }
                </style>
                """,
                unsafe_allow_html=True
            )
        elif profit > 40:
            # 💵 Падающие доллары
            st.image("https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif", width=700)
    
    
 




