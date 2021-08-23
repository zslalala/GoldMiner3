import cufflinks as cf

def HigherDrawing(data):

    cf.set_config_file(offline=True, world_readable=True)
    qf = cf.QuantFig(data, title='图例', legend='top', name='QF',connectgaps=True)

    qf.iplot()