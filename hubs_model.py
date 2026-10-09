"""Модель сети хабов: перебор всех конфигураций. Пример на условных данных.
Запуск: python hubs_model.py   (или вставьте в ячейку Google Colab)"""
import math
from itertools import product

HUBS = {  # хранение млн ₽/год, вход из Китая тыс. ₽/т, дни до хаба, сухопутный
    'Владивосток': dict(lat=43.12, lon=131.89, fixed=120, inb=6,  days=12, land=False),
    'Новосибирск': dict(lat=55.03, lon=82.92,  fixed=90,  inb=10, days=12, land=True),
    'Екатеринбург': dict(lat=56.84, lon=60.61, fixed=100, inb=13, days=14, land=True),
    'Москва':       dict(lat=55.75, lon=37.62, fixed=220, inb=18, days=18, land=True),
    'Краснодар':    dict(lat=45.04, lon=38.98, fixed=110, inb=20, days=20, land=True),
}
REGIONS = {  # спрос, тыс. т/год
    'Центр': (55.75, 37.62, 40), 'Северо-Запад': (59.93, 30.34, 18), 'Поволжье': (56.33, 44.0, 14),
    'Юг': (47.22, 39.72, 14), 'Урал': (56.84, 60.61, 10), 'Сибирь': (55.03, 82.92, 8),
    'Дальний Восток': (43.12, 131.89, 6)}
RATE, SPEED, DAY_COST, BORDER_COST, BORDER_DAYS = 0.0035, 600, 0.4, 1.15, 14

def km(a, b):
    r = math.radians
    dl, dn = r(b[0]-a[0]), r(b[1]-a[1])
    h = math.sin(dl/2)**2 + math.cos(r(a[0]))*math.cos(r(b[0]))*math.sin(dn/2)**2
    return round(2*6371*math.asin(math.sqrt(h))*1.3)

def unit_cost(h, reg, tariff_pct=0, border=False):
    d = km((h['lat'], h['lon']), reg[:2])
    inb, days = h['inb']*(1+tariff_pct/100), h['days']
    if border and h['land']:
        inb *= BORDER_COST; days += BORDER_DAYS
    return inb + d*RATE + (days + d/SPEED)*DAY_COST

def total(open_hubs, tariff_pct=0, border=False):
    fixed = sum(HUBS[h]['fixed'] for h in open_hubs)
    delivery = sum(min(unit_cost(HUBS[h], reg, tariff_pct, border) for h in open_hubs)*reg[2]
                   for reg in REGIONS.values())
    return fixed + delivery

def avg_days(open_hubs, tariff_pct=0, border=False):
    """Средний срок до клиента, дней (взвешенный по спросу)."""
    tot = sum(r[2] for r in REGIONS.values()); s = 0
    for reg in REGIONS.values():
        h = min(open_hubs, key=lambda n: unit_cost(HUBS[n], reg, tariff_pct, border))
        hub = HUBS[h]; d = km((hub['lat'], hub['lon']), reg[:2])
        s += (hub['days'] + (BORDER_DAYS if border and hub['land'] else 0) + d/SPEED)*reg[2]
    return s/tot

def best(tariff_pct=0, border=False):
    names = list(HUBS)
    cfgs = [[n for n, f in zip(names, flags) if f] for flags in product([0, 1], repeat=5) if any(flags)]
    return min(((total(c, tariff_pct, border), c) for c in cfgs), key=lambda x: x[0])

if __name__ == '__main__':
    for t, b, name in [(0, False, 'Базовый'), (30, False, 'Тарифы +30%'),
                       (0, True, 'Граница закрыта'), (30, True, 'Тарифы +30% и граница')]:
        cost, cfg = best(t, b)
        moscow = total(['Москва'], t, b)
        print(f'{name:24s} {", ".join(cfg):45s} {cost:7.0f} млн ₽ | всё через Москву {moscow:6.0f} | экономия {1-cost/moscow:.1%} | срок {avg_days(cfg,t,b):.1f} против {avg_days(['Москва'],t,b):.1f} дн.')
