import plotly.graph_objects as go
import json
import os

class line:
    def __init__(self, xVals, yVals, stds, label):
        self.xVals = xVals
        self.yVals = yVals
        self.stds = stds
        self.label = label
    def __str__(self):
        return ("[X: "+ str(self.xVals) +"\n Y: "+ str(self.yVals)+"\n STDs: "+ str(self.stds) +"\n label: "+ self.label+"]\n")

class chartConfig:
    def __init__(self, xmin, ymin, xticks, ytick, showSTD, title):
        self.xmin = xmin
        self.ymin = ymin
        self.xtick = xticks
        self.ytick = ytick
        self.showSTD = showSTD
        self.title = title

def draw_plot(lines, config):
    layout = go.Layout(
        xaxis = go.layout.XAxis(
            tickmode = 'linear',
            tick0 = config.xmin,
            dtick = config.xtick
        ),
        yaxis = go.layout.YAxis(
            tickmode = 'linear',
            tick0 = config.ymin,
            dtick = config.ytick
        )
    )
    fig = go.Figure(layout = layout)
    for l in lines:
        fig.add_trace(go.Scatter(x=l.xVals, y=l.yVals,
                                 mode='lines+markers',
                                 name=l.label,
                                 error_y=dict(
                                    type='data', # value of error bar given in data coordinates
                                    array=l.stds,
                                    visible=config.showSTD))
        )
    fig.show(config={'editable': True, 'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian']})


def parse_config():
    with open('configs/config_limited.json') as config_file:
        data = json.load(config_file)
        config = chartConfig(data['xmin'], data['ymin'],data['xtick'],data['ytick'], False, data['title'] )
        xVals = data['xVals']
        lines = []
        for yVal in data['yVals']:
            yVals = []
            stds = []
            ignore = yVal['ignore']
            label = yVal["label"]
            with open(yVal['file']) as yVal_file:
                result_file = json.load(yVal_file)
                for eachLine in result_file:
                    if eachLine['qidvid'] in ignore:
                        continue
                    yVals.append(eachLine["avgRT"] / 1000)
                    stds.append(eachLine["STD"]/ 1000)
            l = line(xVals,yVals,stds, label)
            lines.append(l)
        for ls in lines:
            print(ls)
    return lines, config


if __name__ == '__main__':
    if not os.path.exists("images"):
        os.mkdir("images")
    lines, config = parse_config()
    draw_plot(lines, config)