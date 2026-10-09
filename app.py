"""Прототип с двумя кнопками. Запуск: streamlit run app.py
Пример на условных данных."""
import streamlit as st
from hubs_model import best, total, HUBS

st.set_page_config(page_title='Конфигуратор сети хабов', layout='centered')
st.title('Конфигуратор сети хабов')
st.caption('Пример на условных данных. Числа показывают работу метода, а не итог по реальной компании.')
tariff = st.slider('Рост тарифов на плечо из Китая, %', 0, 100, 0, 5)

c1, c2 = st.columns(2)
if c1.button('Рассчитать сеть', type='primary'):
    cost, cfg = best(tariff, False)
    st.metric('Лучшая сеть', ', '.join(cfg))
    st.metric('Затраты, млн ₽/год', f'{cost:,.0f}'.replace(',', ' '))
    st.write(f'Схема «всё через Москву»: {total(["Москва"], tariff, False):,.0f} млн ₽/год'.replace(',', ' '))
if c2.button('Стресс-тест'):
    base_cost, base_cfg = best(0, False)
    rows = []
    for name, t, b in [('Базовый', 0, False), (f'Тарифы +{max(tariff,30)}%', max(tariff, 30), False),
                       ('Граница закрыта', 0, True), ('Тарифы и граница', max(tariff, 30), True)]:
        cost, cfg = best(t, b)
        rows.append({'Сценарий': name, 'Лучшая сеть': ', '.join(cfg),
                     'Старая сеть, млн ₽': round(total(base_cfg, t, b)),
                     'Пересмотр, млн ₽': round(cost)})
    st.table(rows)
