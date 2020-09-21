# %% ==================== MODEL COMPARISON ====================
preds = pd.DataFrame(get_result(VERSION, 'predictions.json')).set_index('wid')
res = preds.apply(lambda d: {k: p[d.c] for k, p in d.predictions.items()}, axis=1)
# logp = np.log(pd.DataFrame(list(res.values)))
# assert not set(MODELS) - set(logp.columns)
logp = np.log(pd.DataFrame(list(res.values)))[MODELS]
logp.set_index(preds.index, inplace=True)
logp['variance'] = pdf.variance
logp = logp.loc[keep]
# logp['Random'] = np.log(preds.p_rand)
assert set(MODELS) < set(logp.columns)

# %% --------

def plot_model_performance(L, label, axes=None):
    if EXPERIMENT == 3:
        return plot_model_performance_exp3(L, label,  axes)
    if EXPERIMENT == 4:
        fig, axes = plt.subplots(1, 1, figsize=(6,4), squeeze=False)
    if axes is None:
        fig, axes = setup_variance_plot()
    for i, v in enumerate(VARIANCES):
        plt.sca(axes.flat[i])
        pal = [palette[m] for m in MODELS]
        L.loc[v].loc[MODELS].plot.barh(color=pal)
        
        plt.xlabel(label)
        if i != 0:
            plt.yticks(())
    figs.reformat_ticks(yaxis=True, ax=axes.flat[0])

# def plot_model_performance_exp3(L, label, axes=None):
#     if axes is None:
#         fig, axes = setup_variance_plot()
    
#     top_models = [m for m in MODELS if not m.endswith('Expand')]
#     bottom_models = [m for m in MODELS if m.endswith('Expand')]
#     # del top_models[0]
#     for i, v in enumerate(VARIANCES):
#         plt.sca(axes.flat[i])

#         for models in [bottom_models, top_models]:
#             pal = [palette[m] for m in models]
#             ax = L.loc[v].loc[models].plot.barh(color=pal)

#         plt.xlabel(label)
#         plt.xlim(0, 0.33)
#         if i == 0:
#             figs.reformat_ticks(yaxis=True)
#         else:
#             plt.yticks(())

def plot_model_performance_exp3(L, label, axes=None):
    if axes is None:
        fig, axes = setup_variance_plot(2, height=3)
    
    top_models = [m for m in MODELS if not m.endswith('Expand')]
    bottom_models = [m for m in MODELS if m.endswith('Expand')]
    model_sets = [top_models, bottom_models] if axes.shape[0] == 2 else [top_models]
    for i, v in enumerate(VARIANCES):
        for j, models in enumerate(model_sets):
            plt.sca(axes[j, i])
            pal = [palette[m] for m in models]
            L.loc[v].loc[models].plot.barh(color=pal)

            plt.xlabel(label)
            plt.xlim(0, 0.33)
            if i == 0:
                figs.reformat_ticks(yaxis=True)
                if j == 1:
                    plt.ylabel('Expansion Bias')
            else:
                plt.yticks(())

@figure()
def plot_average_predictive_accuracy(axes=None):
    plot_model_performance(
        np.exp(logp.groupby(['variance', 'wid']).mean()).groupby('variance').mean(),
        'Predictive Accuracy',
        axes,
    )

# %% --------

show()

# %% --------
top_models = [m for m in MODELS if not m.endswith('Expand')]
bottom_models = [m for m in MODELS if m.endswith('Expand')]

default = L.loc[v].loc[top_models]
expand = L.loc[v].loc[bottom_models]
expand.index = expand.index.str.replace('Expand', '')
bottom_models.insert(0, 'RandomSelection')
dd = pd.DataFrame({'default': default, 'expand': expand}).loc[top_models]
color = [[palette[m] for m in top_models], [palette[m] for m in bottom_models]]
dd.plot.barh(stacked=True, color=color, legend=False)
show()
# %% --------


L.loc[v].loc[models].plot.barh(color=pal)
L

# %% --------

@figure()
def individual_predictive_accuracy():
    models = MODELS
    fig = plt.figure(figsize=(8,4))
    L = np.exp(logp.groupby('wid').mean())
    L = L.loc[keep]

    lm = L.mean().loc[models]
    plt.scatter(lm, lm.index, s=100, color=[palette[m] for m in models]).set_zorder(20)

    sns.stripplot(y='Model', x='value',
        data=pd.melt(L, var_name='Model'),
        order=models,  jitter=False, 
        palette=palette,
        alpha=0.1)

    for wid, row in L.iterrows():
        # c = palette[pdf.click_delay[w]]
        c = 'k'
        plt.plot(row.loc[models], models, color=c, lw=1, alpha=0.1)
    plt.xlabel('Predictive Accuracy')
    plt.ylabel('')
    figs.reformat_ticks(yaxis=True)

# %% --------


# %% --------
    # for i, v in enumerate(VARIANCES):
        # plt.sca(axes[0, i])
        # for model in MODELS:
        #     plot_model(v, model, title=False)
            
        # # g = X.loc[v].groupby('wid'); x = 'n_click'; y = 'term_reward'
        # # plt.errorbar(g[x].mean(), g[y].mean(), yerr=g[y].sem(), xerr=g[x].sem(), 
        # #              label='Human', fmt='.', color='#333333', elinewidth=.5)

        # plt.title(f'{v.title()} Variance')
        # plt.ylabel("Expected Reward")
        # plt.xlabel("Number of Clicks")

        # plt.sca(axes[1, i])
        # L.loc[v].plot.bar(color=[f'C{i}' for i in range(len(MODELS))], rot=30)
        # plt.xlabel('')
        # plt.ylabel("Average Predictive Accuracy")

# %% --------

@figure()
def bbd_individual_likelihood():
    def plot_participants(val, fits, MODELS):
        sns.swarmplot(y='model', x=val, data=fits, order=MODELS,
                      palette=palette)
        for w, d in fits.groupby('wid'):
            # c = palette[pdf.click_delay[w]]
            c = 'k'
            plt.plot(d.set_index('model').loc[MODELS][val], MODELS, color=c, lw=2, alpha=0.5)
        plt.ylabel('')
        plt.xlabel('Log Likelihood')

    X = fits.set_index('variance')

    fig, axes = plt.subplots(len(VARIANCES), 1, figsize=(8,4*len(VARIANCES)))
    for i, v in enumerate(VARIANCES):
        if i != 0:
            plt.legend().remove()
        try:
            plt.sca(axes.flat[i])
        except:
            pass
        plot_participants('cv_nll', X.loc[v], MODELS)
        plt.title(f'{v.title()} Variance')
        if i != len(VARIANCES) - 1:
            plt.xlabel('')

# # %% --------
# @figure()
# def full_likelihood(axes=None):
#     plot_model_performance(
#         -logp.groupby('variance').sum(),
#         'Cross Validated\nNegative Log-Likelihood',
#         axes
#     )

# @figure()
# def geometric_mean_likelihood(axes=None):
#     plot_model_performance(
#         np.exp(logp.groupby('variance').mean()),
#         "Geometric Mean Likelihood",
#         axes
#     )

# # %% --------