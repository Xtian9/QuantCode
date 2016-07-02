from core.stack import *
import utils

def style_default(fig, ax, title='', xlabel='', ylabel='',
                  legend=True):
    """
    Default plotting style/stuff
    """
    fig.patch.set_facecolor('white')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if legend:
        ax.legend(loc='best', frameon=False)
    

def plot_equity_curve(cumrets, cumrets_bm):
    """
    Plot equity curve
        cumrets = series of strategy cumulative returns
        cumrets_bm = series of benchmark cumulative returns
    """
    fig, ax = plt.subplots()

    ax.plot(cumrets, label='Equity')
    ax.plot(cumrets_bm, label='Benchmark')

    ax.axhline(0, linestyle='--', color='black', lw=2)

    style_default(fig, ax, title='Equity curve',
                  ylabel='Portfolio value growth (%)')

    return fig, ax 


def plot_rolling_sharpe(returns, nperiods, rfrate, window):
    """
    Plot rolling Sharpe ratio
        returns = series of returns
        nperiods = number of returns in a year
        rfrate = risk free rate
        window = number of months in sliding window
    """
    fig, ax = plt.subplots()

    overall_sharpe = utils.sharpe_ratio(returns, nperiods, rfrate)
    rolling_sharpe = utils.rolling_sharpe(returns, nperiods,
                                          rfrate, 21*window)

    ax.plot(rolling_sharpe, color='orangered', lw=2, 
            label='Rolling Sharpe')
    
    ax.axhline(overall_sharpe, 
               color='steelblue', linestyle='--', lw=3,
               label='Overall Sharpe')

    ax.axhline(0, color='black', linestyle='-', lw=2)

    style_default(fig, ax, 
                  title='Rolling Sharpe ratio ({} months)'.format(window),
                  ylabel='Sharpe ratio')

    return fig, ax


def plot_drawdown(cumrets):
    """
    Plot drawdown vs time
        cumrets = series of cumulative returns
    """
    fig, ax = plt.subplots()

    dd = -1 * utils.rolling_drawdown(cumrets)

    dd.plot(kind='area', color='coral', alpha=.7)

    style_default(fig, ax, title='Drawdown', 
                           ylabel='Drawdown', legend=False)

    return fig, ax


def plot_top_drawdowns(cumrets, ntop):
    """
    Plot top drawdowns by magntidue and duration
        cumrets = series of cumulative returns
        ntop = # top drawdowns to plot
        ret = dictionary of (fig, ax) for
              magnitude and duration plots
    """
    ret = {}

    colors = [plt.get_cmap('rainbow')(i) for i in np.linspace(0, 1, ntop)]

    dd_info, ddd_info = utils.sort_drawdowns(cumrets)

    for ddtype, info in (('magnitude', dd_info), ('duration', ddd_info)):
        fig, ax = plt.subplots()
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

        style_default(fig, ax, 
                      title='Top drawdown periods by {}'.format(ddtype),
                      ylabel='Cumulative net return (%)')

        ret[ddtype] = (fig, ax)

    return ret

