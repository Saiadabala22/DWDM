"""Chart builders (Plotly + Matplotlib) used by the Visualization and Data Mining pages."""
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETTE = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#14b8a6', '#ec4899', '#64748b', '#84cc16', '#f97316']
_LAYOUT = dict(template='plotly_white', font=dict(family='Inter, sans-serif'), margin=dict(l=20, r=20, t=50, b=20))


def _style(fig, **kw):
    fig.update_layout(**_LAYOUT, **kw)
    return fig


# ---------- exploratory charts ----------
def histogram(df, col, color=None):
    return _style(px.histogram(df, x=col, color=color, nbins=30, color_discrete_sequence=PALETTE, title=f'Distribution of {col}'))


def boxplot(df, col, by=None):
    return _style(px.box(df, y=col, x=by, color=by, points='outliers', color_discrete_sequence=PALETTE, title=f'Box plot of {col}'))


def bar_counts(df, col, top=20):
    vc = df[col].astype(str).value_counts().head(top).rename_axis(col).reset_index(name='Count')
    return _style(px.bar(vc, x=col, y='Count', color=col, color_discrete_sequence=PALETTE, title=f'Top values of {col}'), showlegend=False)


def pie_counts(df, col, top=10):
    vc = df[col].astype(str).value_counts()
    if len(vc) > top:
        vc = pd.concat([vc.head(top), pd.Series({'Other': vc.iloc[top:].sum()})])
    vc = vc.rename_axis(col).reset_index(name='Count')
    return _style(px.pie(vc, names=col, values='Count', hole=.4, color_discrete_sequence=PALETTE, title=f'Share of {col}'))


def correlation_heatmap(df):
    c = df.select_dtypes('number').corr()
    fig = px.imshow(c.round(2), text_auto=True, zmin=-1, zmax=1, color_continuous_scale='RdBu_r', aspect='auto', title='Correlation matrix')
    return _style(fig, height=max(420, 40 * len(c)))


def scatter(df, x, y, color=None):
    return _style(px.scatter(df, x=x, y=y, color=color, opacity=.75, color_discrete_sequence=PALETTE, title=f'{y} vs {x}'))


# ---------- additional exploratory charts ----------
def violin(df, col, by=None):
    return _style(px.violin(df, y=col, x=by, color=by, box=True, points='outliers', color_discrete_sequence=PALETTE, title=f'Violin plot of {col}'))


def density(df, col, by=None):
    return _style(px.histogram(df, x=col, color=by, histnorm='probability density', marginal='rug', nbins=40, opacity=.7,
                               barmode='overlay', color_discrete_sequence=PALETTE, title=f'Density of {col}'))


def grouped_bar(df, cat, group, top=15):
    keep = df[cat].astype(str).value_counts().head(top).index
    d = df[df[cat].astype(str).isin(keep)].assign(**{cat: lambda x: x[cat].astype(str), group: lambda x: x[group].astype(str)})
    d = d.groupby([cat, group]).size().reset_index(name='Count')
    return _style(px.bar(d, x=cat, y='Count', color=group, barmode='group', color_discrete_sequence=PALETTE, title=f'{cat} by {group}'))


def stacked_bar(df, cat, group, top=15):
    keep = df[cat].astype(str).value_counts().head(top).index
    d = df[df[cat].astype(str).isin(keep)].assign(**{cat: lambda x: x[cat].astype(str), group: lambda x: x[group].astype(str)})
    d = d.groupby([cat, group]).size().reset_index(name='Count')
    return _style(px.bar(d, x=cat, y='Count', color=group, barmode='relative', color_discrete_sequence=PALETTE, title=f'{cat} by {group} (stacked)'))


def scatter_matrix(df, cols, color=None):
    return _style(px.scatter_matrix(df, dimensions=cols, color=color, opacity=.7, color_discrete_sequence=PALETTE, title='Scatter matrix'),
                  height=max(500, 170 * len(cols)))


def scatter3d(df, x, y, z, color=None):
    fig = px.scatter_3d(df, x=x, y=y, z=z, color=color, opacity=.8, color_discrete_sequence=PALETTE, title=f'{x} / {y} / {z}')
    fig.update_traces(marker=dict(size=4))
    return _style(fig, height=600)


def line_chart(df, x, y, color=None):
    d = df.sort_values(x)
    return _style(px.line(d, x=x, y=y, color=color, color_discrete_sequence=PALETTE, title=f'{y} over {x}'))


def parallel_coordinates(df, cols, color):
    d = df[cols + [color]].dropna().copy()
    if not pd.api.types.is_numeric_dtype(d[color]):
        d[color] = d[color].astype('category').cat.codes
    return _style(px.parallel_coordinates(d, dimensions=cols, color=color, color_continuous_scale='Viridis', title='Parallel coordinates'))


def missing_values(df):
    m = df.isna().sum().rename_axis('Column').reset_index(name='Missing')
    m['Percent'] = (m['Missing'] / max(len(df), 1) * 100).round(2)
    return _style(px.bar(m, x='Column', y='Percent', text='Missing', color_discrete_sequence=[PALETTE[3]], title='Missing values per column (%)'))


def summary_bar(df, cat, num, agg='mean', top=20):
    d = df.groupby(df[cat].astype(str))[num].agg(agg).sort_values(ascending=False).head(top).reset_index()
    d.columns = [cat, f'{agg}({num})']
    return _style(px.bar(d, x=cat, y=d.columns[1], color=cat, color_discrete_sequence=PALETTE, title=f'{agg.title()} of {num} by {cat}'), showlegend=False)


# ---------- mining result charts ----------
def confusion_heatmap(cm, classes):
    classes = [str(c) for c in classes]
    fig = px.imshow(cm, x=classes, y=classes, text_auto=True, color_continuous_scale='Blues', aspect='auto',
                    labels=dict(x='Predicted', y='Actual', color='Count'), title='Confusion matrix')
    return _style(fig)


def importance_bar(imp, top=15):
    d = imp.head(top).iloc[::-1]
    return _style(px.bar(d, x='Importance', y='Feature', orientation='h', color_discrete_sequence=[PALETTE[0]], title='Feature importance'),
                  height=max(300, 28 * len(d) + 100))


def metrics_bar(m):
    d = pd.DataFrame({'Metric': [k for k in ['Accuracy', 'Precision', 'Recall', 'F1', 'Kappa', 'AUC'] if m.get(k) is not None]})
    d['Score'] = [m[k] for k in d['Metric']]
    fig = px.bar(d, x='Metric', y='Score', text=d['Score'].round(3), color_discrete_sequence=[PALETTE[1]], title='Model metrics')
    fig.update_yaxes(range=[min(0, d['Score'].min()), 1])
    return _style(fig)


def cluster_scatter(p, labels):
    d = pd.DataFrame({'PC1': p[:, 0], 'PC2': p[:, 1], 'Cluster': pd.Series(labels).astype(str)})
    return _style(px.scatter(d, x='PC1', y='PC2', color='Cluster', opacity=.8, color_discrete_sequence=PALETTE, title='k-Means clusters (PCA projection)'))


def elbow_chart(e):
    fig = go.Figure(go.Scatter(x=e['K'], y=e['SSE'], mode='lines+markers', line=dict(color=PALETTE[0]), name='SSE'))
    fig.update_layout(title='Elbow method (SSE vs K)', xaxis_title='K', yaxis_title='SSE', xaxis=dict(dtick=1))
    return _style(fig)


def rules_scatter(rules):
    r = rules.copy()
    r['rule'] = r['antecedents'].map(lambda s: ', '.join(map(str, s))) + '  →  ' + r['consequents'].map(lambda s: ', '.join(map(str, s)))
    fig = px.scatter(r, x='support', y='confidence', size='lift', color='lift', hover_name='rule',
                     color_continuous_scale='Viridis', title='Association rules (size & colour = lift)')
    return _style(fig)


# ---------- decision tree diagrams ----------
def _pretty(name, thr):
    """Return (node text, left-edge label, right-edge label). One-hot features are named 'col = value'."""
    if ' = ' in name and abs(thr - 0.5) < 1e-9:
        return f'{name}?', 'No', 'Yes'
    return f'{name} ≤ {thr:.3g}', 'Yes', 'No'


def _layout(t, max_depth):
    """Leaf-ordered tidy layout: returns dict id -> (x, y) and edges."""
    pos, edges = {}, []
    counter = [0]

    def walk(i, d):
        l, r = t.children_left[i], t.children_right[i]
        if l == r or (max_depth is not None and d >= max_depth):
            pos[i] = (counter[0], -d)
            counter[0] += 1
            return pos[i][0]
        xl = walk(l, d + 1)
        xr = walk(r, d + 1)
        pos[i] = ((pos[l][0] + pos[r][0]) / 2, -d)
        edges.append((i, l, 'L'))
        edges.append((i, r, 'R'))
        return pos[i][0]

    walk(0, 0)
    return pos, edges


def interactive_tree(model, feature_names, class_names, max_depth=None):
    """Plotly decision-tree diagram: hover any node for samples, class counts, impurity."""
    t = model.tree_
    class_names = [str(c) for c in class_names]
    pos, edges = _layout(t, max_depth)
    shown = set(pos)
    cls_idx = {c: i for i, c in enumerate(class_names)}
    fig = go.Figure()
    # edges
    labels_x, labels_y, labels_t = [], [], []
    for a, b, side in edges:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', line=dict(color='#94a3b8', width=1.5), hoverinfo='skip', showlegend=False))
        _, ll, rl = _pretty(feature_names[t.feature[a]], t.threshold[a])
        labels_x.append((x0 + x1) / 2); labels_y.append((y0 + y1) / 2); labels_t.append(ll if side == 'L' else rl)
    fig.add_trace(go.Scatter(x=labels_x, y=labels_y, mode='text', text=labels_t, textfont=dict(size=10, color='#475569'), hoverinfo='skip', showlegend=False))
    # nodes grouped by predicted class so the legend works
    by_cls = {}
    for i in shown:
        counts = t.value[i][0]
        k = int(np.argmax(counts))
        by_cls.setdefault(k, []).append(i)
    for k, ids in sorted(by_cls.items()):
        xs, ys, txt, hover, sizes = [], [], [], [], []
        for i in ids:
            is_leaf = t.children_left[i] == t.children_right[i]
            cut = (not is_leaf) and max_depth is not None and -pos[i][1] >= max_depth
            counts = t.value[i][0]
            total = counts.sum()
            dist = '<br>'.join(f'{class_names[j]}: {counts[j]/total:.0%}' for j in np.argsort(-counts)[:6] if counts[j] > 0)
            if is_leaf:
                label, kind = class_names[k], 'leaf'
            elif cut:
                label, kind = class_names[k] + ' …', 'truncated'
            else:
                label, kind = _pretty(feature_names[t.feature[i]], t.threshold[i])[0], 'split'
            xs.append(pos[i][0]); ys.append(pos[i][1]); txt.append(label)
            sizes.append(14 + 26 * np.sqrt(t.n_node_samples[i] / t.n_node_samples[0]))
            fig.add_annotation(x=pos[i][0], y=pos[i][1], text=label, showarrow=False, yshift=-(sizes[-1] / 2 + 11), font=dict(size=11, color='#0f172a'),
                               bgcolor='rgba(255,255,255,0.92)', borderpad=2, bordercolor='#e2e8f0' if kind != 'leaf' else PALETTE[k % len(PALETTE)])
            hover.append(f'<b>{label}</b><br>{kind} · samples: {t.n_node_samples[i]}<br>impurity: {t.impurity[i]:.3f}<br>{dist}')
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='markers',
                                 marker=dict(size=sizes, color=PALETTE[k % len(PALETTE)], opacity=1, line=dict(color='white', width=2)),
                                 hovertext=hover, hoverinfo='text', name=f'Predicts {class_names[k]}'))
    depth = max(-p[1] for p in pos.values())
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(title='Decision tree (hover a node for details; marker size = samples)', height=max(480, 150 * (depth + 1) + 120),
                      hovermode='closest', legend=dict(orientation='h', y=-0.05))
    return _style(fig)


def static_tree_png(model, feature_names, class_names, max_depth=None, dpi=130):
    """Publication-style Matplotlib tree (sklearn.plot_tree). Returns (figure, png_bytes)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from sklearn.tree import plot_tree
    depth = model.get_depth() if max_depth is None else min(max_depth, model.get_depth())
    leaves = min(model.get_n_leaves(), 2 ** depth)
    fig, ax = plt.subplots(figsize=(min(60, max(10, 1.9 * leaves)), min(30, max(5, 2.4 * (depth + 1)))))
    plot_tree(model, feature_names=feature_names, class_names=[str(c) for c in class_names], filled=True, rounded=True,
              max_depth=max_depth, fontsize=10, ax=ax, impurity=True, proportion=False)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    return fig, buf.getvalue()
