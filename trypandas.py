import pandas as pd
import altair as alt

# Örnek veri seti
data = {
    'Tarih': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
    'Fiyat': [100, 102, 98, 105, 110]
}

# DataFrame oluşturma
df = pd.DataFrame(data)

# Altair ile grafik oluşturma
chart = alt.Chart(df).mark_line(point=True).encode(
    x='Tarih:T',
    y='Fiyat:Q'
).properties(title='Hisse Senedi Fiyatı Değişimi')

chart.show()
