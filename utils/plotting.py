from core.stack import *
from utils import timeseries

def style_default(ax, title='', xlabel='', ylabel='',
                  legend=True):
    """
    Default plotting style/stuff
    """
    #fig.patch.set_facecolor('white')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if legend:
        ax.legend(loc='best', frameon=False)
    

def plot_equity_curve(cumrets, cumrets_bm, ax=None):
    """
    Plot equity curve
        cumrets = series of strategy cumulative returns
        cumrets_bm = series of benchmark cumulative returns
    """
    if ax is None:
        ax = plt.gca()

    ax.plot(cumrets, label='Equity')
    ax.plot(cumrets_bm, label='Benchmark')

    ax.axhline(0, linestyle='--', color='black', lw=2)

    style_default(ax, title='Equity curve',
                  ylabel='Portfolio value growth (%)')


def plot_rolling_sharpe(returns, nperiods, rfrate, window, ax=None):
    """
    Plot rolling Sharpe ratio
        returns = series of returns
        nperiods = number of returns in a year
        rfrate = risk free rate
        window = number of months in sliding window
    """
    if ax is None:
        ax = plt.gca()

    overall_sharpe = timeseries.sharpe_ratio(returns, nperiods, rfrate)
    rolling_sharpe = timeseries.rolling_sharpe(returns, nperiods,
                                               rfrate, 21*window)

    ax.plot(rolling_sharpe, color='orangered', lw=2, 
            label='Rolling Sharpe')
    
    ax.axhline(overall_sharpe, 
               color='steelblue', linestyle='--', lw=3,
               label='Overall Sharpe')

    ax.axhline(0, color='black', linestyle='-', lw=2)

    style_default(ax, 
                  title='Rolling Sharpe ratio ({} months)'.format(window),
                  ylabel='Sharpe ratio')


def plot_drawdown(cumrets, ax=None):
    """
    Plot drawdown vs time
        cumrets = series of cumulative returns
    """
    if ax is None:
        ax = plt.gca()

    dd = -1 * timeseries.rolling_drawdown(cumrets)

    dd.plot(ax=ax, kind='area', color='coral', alpha=.7)

    style_default(ax, title='Drawdown', 
                      ylabel='Drawdown (%)', legend=False)


def plot_top_drawdowns(cumrets, ntop, ddtype, ax=None):
    """
    Plot top drawdowns by magntidue and duration
        cumrets = series of cumulative returns
        ntop = # top drawdowns to plot
        ret = dictionary of (fig, ax) for
              magnitude and duration plots
    """
    if ax is None:
        ax = plt.gca()

    colors = [plt.get_cmap('rainbow')(i) for i in np.linspace(0, 1, ntop)]

    dd_info, ddd_info = timeseries.sort_drawdowns(cumrets)

    if ddtype == 'magnitude':
        info = dd_info
    elif ddtype == 'duration':
        info = ddd_info

    ax.plot(cumrets)

    for i, (date_start, date_end, dd) in enumerate(info[:ntop]):
        if ddtype == 'magnitude':
            label = '{:.1f}%'.format(dd*100)
        elif ddtype == 'duration':
            label = '{:.0f}'.format(dd)

        ax.fill_between((date_start, date_end),
                        *ax.get_ylim(),
                        alpha=.3, color=colors[ntop-i-1],
                        label=label)

    style_default(ax, 
                  title='Top drawdown periods by {}'.format(ddtype),
                  ylabel='Cumulative net return (%)')


def plot_monthly_returns(returns, ax=None):
    """
    Plot distribution of monthly returns
        returns = series of daily returns 
    """
    if ax is None:
        ax = plt.gca()

    

