import matplotlib.pyplot as plt
from matplotlib import style

def GenerateBarsPlot(Values, XLabelNames, Color, Alpha=1):
    XLabel_Names = []
    i = 0
    for Name in XLabelNames:
        XLabel_Names.append(str(Name) + str(" ") + str('(') + str(Values[i]) + str(')'))
        i += 1
    style.use('dark_background')
    plt.bar([i for i in range(len(Values))], Values, color=Color, alpha=Alpha, edgecolor='white')
    plt.xticks([i for i in range(len(Values))], XLabel_Names)

def GenerateDotsPlot(Values, XLabelName, Color, Alpha=1):
    style.use('dark_background')
    plt.plot(Values, color=Color, alpha=Alpha)
    plt.plot(Values, color=Color, alpha=Alpha-0.10)

def GeneratePlot():
    plt.show()
