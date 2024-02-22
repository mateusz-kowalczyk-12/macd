import Functions as Fun
import matplotlib.pyplot as plt

dates = []
closingPrices = []

Fun.readData(dates, closingPrices)

MACD = Fun.MACD(closingPrices)
SIGNAL = Fun.SIGNAL(MACD)

fig, (axData, axMACD) = plt.subplots(nrows=2, ncols=1, sharex="col")
fig.set_size_inches(18, 16)
fig.subplots_adjust(hspace=0, left=0.04, right=0.96, top=0.97, bottom=0.13)

plt.setp(axMACD.xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")
plt.setp(axData.xaxis.get_majorticklabels(), ha="left", rotation_mode="anchor")

startingCapital = 1000.0
purchaseDatesNumbers = []
sellDatesNumbers = []
finalCapital, finalStocks = Fun.applySimpleStrategy(MACD[9:], SIGNAL, dates[26 + 9:], closingPrices[26 + 9:], startingCapital, purchaseDatesNumbers, sellDatesNumbers)

print("Kapitał początkowy: ", end="")
print(startingCapital, end=" j.\n")
print("Kapitał końcowy: ", end="")
print(round(finalCapital, 2), end=" j. oraz ")
print(finalStocks, end=" akcji wartych w sumie ")
print(round(finalStocks * closingPrices[len(closingPrices) - 1], 2), end=" j., a więc łączny kapitał o wartości ")
print(round(finalCapital + finalStocks * closingPrices[len(closingPrices) - 1], 2), end=" j.\n")

Fun.plotData(axData, dates, closingPrices, purchaseDatesNumbers, sellDatesNumbers)
Fun.plotMACD(axMACD, MACD[9:], SIGNAL, dates[26 + 9:])

plt.show()
