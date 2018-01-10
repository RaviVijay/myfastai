import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


"""
Hierarchical Bar Chart of a column of DataFrame. 
Example: Compare DynPower,LeakPower, TotalPower of different Tags in one chart. 
         By Grouping DynPower,LeakPower, TotalPower of each Tag together
"""
def bar_hier_multiindex(df, column):
    df[column].unstack().plot(kind='bar')


"""
Example : Track Total Power across Tags in a Line Chart
"""
def factor_plot_less_confused(DF, col_to_plot, index_of_plot_list, col_to_use_as_tag):
    fg = seaborn.factorplot(x=col_to_use_as_tag, y=col_to_plot,  
                            col=index_of_plot_list, data=DF)
    fg.set_xlabels(rotation=90)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%s'))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    plt.show()

