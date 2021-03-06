# %% ==================== Model comparison plots ====================

from scipy.stats import ttest_rel, ttest_ind

X = logp[COMPARISON_MODELS].groupby('wid').mean()
opt = X.OptimalPlus
for alt, x in X.iteritems():
    tst = ttest_rel(x, opt)
    print(f'{alt}: {tst.pvalue:.5f}')


# %% --------
models = [m for m in COMPARISON_MODELS if not m.endswith('Expand')]
pal = [palette[m] for m in models]

plt.figure(figsize=(8,4))
pal = [palette[m] for m in COMPARISON_MODELS]
for i in range(6, len(pal)):
    pal[i] = lg
sns.barplot('variable', 'value', data=pd.melt(logp[top_models]), 
    estimator=lambda x: np.exp(np.mean(x)),
    palette=pal, saturation=1, )
plt.xticks(rotation=35, ha="right")
plt.xlabel('')
plt.ylabel('Geometric Mean\nLikelihood',)
figs.reformat_ticks()
show()


# %% --------
ptotal = logp.groupby(['variance', 'wid']).sum()
X = ptotal[COMPARISON_MODELS]
# X = X.sub(X.Random, axis=0)

sns.barplot('variable', 'value', data=pd.melt(X), 
    estimator=lambda x: np.sum(x) / n_obsq,
    palette=pal, saturation=1, )
show()

# %% --------
from scipy.stats import gstd
L = X.groupby('variance').mean()
Y = X.sub(X.Random, axis=0)
V = Y.groupby('variance').var()
# V = X.groupby('variance').var()

n_obs = len(logp)
obs_per_subj = n_obs / len(X)

# L /= obs_per_subj
# V /= obs_per_subj
S = np.sqrt(V)
print(S)


label = "Foo"
plt.figure(figsize=(8,4))
ax = plt.gca()
pal = [palette[m] for m in COMPARISON_MODELS]
for i in range(6, len(pal)):
    pal[i] = lg


print(L.shape)
x = L.groupby('variance').mean().loc['constant'].loc[COMPARISON_MODELS]
x.plot.bar(color=pal, yerr=S.values[0])


plt.xticks(rotation=35, ha="right")
figs.reformat_ticks()
plt.ylabel(label)

show()




# %% ====================  ====================


def do_if(cond):
    def wrapper(f):
        if cond:
            f()
    return wrapper

@do_if(1 == 1)
def fun():
    print('fun')


# %% --------
%run setup 1
print(pdf.groupby(['click_delay', 'variance']).apply(len))
%run setup 2
print(pdf.groupby(['click_delay', 'variance']).apply(len))
%run setup 3
print(pdf.groupby(['click_delay', 'variance']).apply(len))
%run setup 4
print(len(pdf))





x = np.linspace(0, 20)
y = x + np.random.randn(len(x)) * 0.025 * 5
plt.plot(x, y)
plt.show()

# %% --------
import hashlib
def hash_id(worker_id):
    return 'w' + hashlib.md5(worker_id.encode()).hexdigest()[:7]

wid = hash_id('5f292bd0f94a2428215919a1')


tdf.loc[wid]

30 * 7 - tdf.score.clip(lower=-30).groupby('wid').sum()

# %% --------
trial_bonus = (30 - tdf.score).clip(lower=0) / 1000
trial_bonus.groupby('wid').sum()
tdf.score
tdf.loc[wid]
# %% --------
@figure()
def exp2_big():
    fig, axes = setup_variance_plot(4, label_offset=-0.4)
    for v, ax in zip(VARIANCES, axes[0, :]):
        ax.imshow(task_image(v))
        ax.axis('off')

    plot_second_click(axes[1, :], models=['OptimalPlus', 'BestFirst'])
    plot_pareto(axes[2, :], legend=False, fit_reg=False)
    plot_average_predictive_accuracy(axes[3, :])
    figs.reformat_ticks(yaxis=True, ax=axes[2,0])

# %% ==================== compare cross validation ====================
rand_cv = pd.concat([pd.read_csv(f'model/results/{EXPERIMENT}-randomfolds/mle/{model}-cv.csv')
                     for model in MODELS], sort=False)

fits = fits.join(rand_cv.groupby(['model', 'wid']).test_nll.sum().rename('rand_nll'), on=['model', 'wid'])

# %% --------
g = sns.FacetGrid(row='variance', col='model', data=fits, aspect=1, margin_titles=True)
g.map(sns.scatterplot, 'cv_nll', 'rand_nll')

for ax in g.axes.flat:
    ax.plot([0, 0], [500, 500], c='k')
show()


# %% --------
MODELS = 'BreadthFirst DepthFirst BestFirst Optimal'.split()
fits = load_fits(exp, MODELS, path='mle')
COMPARISON_MODELS
fits = fits.join(pdf[['variance', 'click_delay']], on='wid')
pdf['cost'] = fits.query('model == "Optimal"').set_index('wid').cost.clip(upper=5)

cf = pd.read_json(f'model/results/{exp}/click_features.json').set_index('wid')
res = cf.apply(lambda d: {k: p[d.c] for k, p in d.predictions.items()}, axis=1)
logp = np.log(pd.DataFrame(list(res.values)))[MODELS]
logp.set_index(cf.index, inplace=True)
logp['variance'] = pdf.variance
# %% --------
r = tdf.state_rewards.iloc[0]

tdf['max_possible'] = tdf.state_rewards.apply(lambda r:
    max(sum(r[i:i+5]) for i in range(1, 17, 5))
)


indmax = tdf.groupby('wid').max_possible.mean()
achieved = tdf.groupby('wid').score.mean()
all(achieved <= indmax)

tdf.query('variance == "increasing"').groupby('wid').score.mean()