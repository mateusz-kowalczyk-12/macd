import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def readData(dates, closingPrices):
    dataFile = open("mrc_d.csv", "r")
    next(dataFile)  # skipping the header line

    for dataLine in dataFile:
        splitDataLine = dataLine.split(";")
        # splitDataLine[0] -> date, splitDataLine[4] -> closing price

        dates.append(splitDataLine[0])
        closingPrices.append(float(splitDataLine[4]))

    dataFile.close()


def EMA(N, data, currentDay):
    alpha = 2 / (N + 1)
    EMANumer = 0
    EMADenom = 0

    for i in range(N + 1):
        EMANumer = EMANumer + pow(1 - alpha, i) * data[currentDay - i]
        EMADenom = EMADenom + pow(1 - alpha, i)

    return EMANumer / EMADenom


def MACD(closingPrices):
    MACD = []

    for i in range(26, len(closingPrices)):
        MACD.append(EMA(12, closingPrices, i) - EMA(26, closingPrices, i))

    return MACD


def SIGNAL(MACD):
    SIGNAL = []

    for i in range(9, len(MACD)):
        SIGNAL.append(EMA(9, MACD, i))

    return SIGNAL


def applySimpleStrategy(MACDReduced, SIGNAL, datesReduced, closingPricesReduced, capital, purchaseDatesNumbers, sellDatesNumbers):
    sharesOwned = 0

    for date in range(2, len(datesReduced)):
        if SIGNAL[date - 2] > MACDReduced[date - 2] and SIGNAL[date - 1] <= MACDReduced[date - 1]:
            # purchase
            sharesPurchased = int(capital / closingPricesReduced[date])
            sharesOwned = sharesOwned + sharesPurchased
            capital = capital - sharesPurchased * closingPricesReduced[date]
            purchaseDatesNumbers.append(date)

        elif SIGNAL[date - 2] < MACDReduced[date - 2] and SIGNAL[date - 1] >= MACDReduced[date - 1]:
            # sell
            capital = capital + sharesOwned * closingPricesReduced[date]
            sharesOwned = 0
            sellDatesNumbers.append(date)

    return capital, sharesOwned


def plotData(axData, dates, closingPrices, purchaseDatesNumbers, sellDatesNumbers):
    axData.set_title("Ceny akcji (u góry) oraz wskaźnik MACD (u dołu) dla spółki Mercator Medica S.A. w okresie 20.02.2019-28.12.2022", fontsize=18)
    axData.grid()

    y_padding = 50

    axData.plot(dates, closingPrices, color="#797979", zorder=5)

    x_ticks = [dates[i] for i in range(0, len(dates), 2)]
    axData.set_xticks(x_ticks)
    axData.set_xticklabels(x_ticks, rotation=-45, fontsize=12)
    axData.set_xlim(min(dates), max(dates))

    y_ticks = [i for i in range(int(min(closingPrices)), int(max(closingPrices)) + y_padding, y_padding)]
    axData.set_yticks(y_ticks, fontsize=12)
    axData.set_ylim(int(min(closingPrices)) - y_padding, int(max(closingPrices)) + y_padding)
    axData.set_ylabel("Cena zamknięcia [zł]", fontsize=16)

    closingPricesReduced = closingPrices[26 + 9:]
    purchaseDates = []
    purchasePrices = []
    sellDates = []
    sellPrices = []

    for dateNumber in range(len(purchaseDatesNumbers)):
        purchaseDates.append(dates[35 + purchaseDatesNumbers[dateNumber]])
        purchasePrices.append(closingPricesReduced[purchaseDatesNumbers[dateNumber]])
    for dateNumber in range(len(sellDatesNumbers)):
        sellDates.append(dates[35 + sellDatesNumbers[dateNumber]])
        sellPrices.append(closingPricesReduced[sellDatesNumbers[dateNumber]])

    axData.scatter(purchaseDates, purchasePrices, label="Kupno", color="red", s=20, zorder=10)
    axData.scatter(sellDates, sellPrices, label="Sprzedaż", color="green", s=20, zorder=10)

    axData.legend(fontsize=12)


def plotMACD(axMACD, MACD_reduced, SIGNAL, dates_reduced):
    axMACD.plot(dates_reduced, MACD_reduced, label="MACD", color="#073db8")
    axMACD.plot(dates_reduced, SIGNAL, label="SIGNAL", color="#e4320c")

    y_padding = 10

    x_ticks = [dates_reduced[i] for i in range(0, len(dates_reduced), 20)]
    axMACD.set_xticks(x_ticks)
    axMACD.set_xticklabels(x_ticks, rotation=-45, fontsize=12)
    axMACD.set_xlabel("Data", fontsize=16)

    y_ticks = [i for i in range(int(min(min(MACD_reduced), min(SIGNAL))), int(max(max(MACD_reduced), max(SIGNAL))) + y_padding, y_padding)]
    axMACD.set_yticks(y_ticks)
    axMACD.set_ylim(int(min(min(MACD_reduced), min(SIGNAL))) - y_padding, int(max(max(MACD_reduced), max(SIGNAL))) + y_padding)
    axMACD.set_ylabel("Wartość", fontsize=16)

    axMACD.legend(fontsize=12)

    axMACD.grid()
