import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
import yfinance
import MetaTrader5 as mt5

yfinance.pdr_override()

simbolo = input("Escreva o nome do ativo(US100): ")
start = input("Escreva a data de inicio(a/m/d h:m:s): ")
end = input("Escreva a data de fim(a/m/d h:m:s): ")

start = datetime.strptime(start, "%y/%m/%d %H:%M:%S")
end = datetime.strptime(end, "%y/%m/%d %H:%M:%S")

# Obtendo os dados das ações


if not mt5.initialize():
    print("Falha na inicialização, código de erro =", mt5.last_error())
    mt5.shutdown()
    mt5.initialize()
df = mt5.copy_rates_range(simbolo, mt5.TIMEFRAME_D1, start, end)
df = pd.DataFrame(df)
size = df.size
print(size)
df['time'] = pd.to_datetime(df['time'], unit='s')
df = df.set_index('time')

# Preparando os dados para o modelo de regressão linear
df['time'] = df.index
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d')
df['time'] = df['time'].map(datetime.toordinal)
df = df.reset_index(drop=True)
print(df)


def IA(valor):
    # Definindo variáveis dependentes e independentes
    X = df['close'].values.reshape(-1, 1)
    y = df[valor].values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, train_size=0.75, random_state=7300)

    # Treinando o modelo de regressão linear
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    print(regressor)
    # Fazendo previsões usando o conjunto de teste
    y_pred = regressor.predict(X_test)
    print("Previsao", valor)
    print(str(y_pred))


IA("high")
IA("close")
IA("low")

while True:
    ok = "rodando"
