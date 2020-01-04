# A series of vertically faceted line plots or density curves, but with somewhat overlapping y-axes.
# First of all, changing the form of the distribution plots from histograms to kernel density estimates (KDE).
# Second, we need to facet the levels by rows so that they're all stacked up on top of one another.

group_means = df.groupby(['many_cat_var']).mean()
group_order = group_means.sort_values(['num_var'], ascending = False).index

g = sb.FacetGrid(data = df, row = 'many_cat_var', size = 0.75, aspect = 7,
                 row_order = group_order)
g.map(sb.kdeplot, 'num_var', shade = True)
g.set_titles('{row_name}')

# `FacetGrid` and `set_titles`change "col" to "row", also removing "col_wrap".
# The "size" and "aspect" dimensions have also been adjusted for the large vertical stacking of facets.
# The `map` function changes to kdeplot and removes "bins", adding the "shade" parameter in its place.


group_means = df.groupby(['many_cat_var']).mean()
group_order = group_means.sort_values(['num_var'], ascending = False).index

# adjust the spacing of subplots with gridspec_kws
g = sb.FacetGrid(data = df, row = 'many_cat_var', size = 0.5, aspect = 12,
                 row_order = group_order, gridspec_kws = {'hspace' : -0.2})
g.map(sb.kdeplot, 'num_var', shade = True)

# remove the y-axes
g.set(yticks=[])
g.despine(left=True)

g.set_titles('{row_name}')

# By setting "hspec" to a negative value, the subplot axes bounds will overlap vertically.
# I'll add some code on the FacetGrid object to remove the y-axis through the despine method and remove the ticks through the set method.

# The individual subplots now overlap, but we've still got a problem: the backgrounds of the subplots are opaque, thus obscuring all but the tops of all of the individual group distributions, with the exception of the lowest. In addition, the individual subplot titles overlap the other distributions with some ambiguity: these should be moved elsewhere in the individual plots. The revised code and plot look like this:

group_means = df.groupby(['many_cat_var']).mean()
group_order = group_means.sort_values(['num_var'], ascending = False).index

g = sb.FacetGrid(data = df, row = 'many_cat_var', size = 0.5, aspect = 12,
                 row_order = group_order, gridspec_kws = {'hspace' : -0.2})
g.map(sb.kdeplot, 'num_var', shade = True)

g.set(yticks=[])
g.despine(left=True)

# set the transparency of each subplot to full
g.map(lambda **kwargs: plt.gca().patch.set_alpha(0))

# remove subplot titles and write in new labels
def label_text(x, **kwargs):
    plt.text(4, 0.02, x.iloc[0], ha = 'center', va = 'bottom')
g.map(label_text, 'many_cat_var')
g.set_xlabels('num_var')
g.set_titles('')

# We make clever use of the FacetGrid object's map function to perform the plot modifications. Previously, you've seen map used where the first argument is a plotting function, the following arguments are positional variable strings, and any additional arguments are keyword arguments for the plotting function. In actuality, you can set any function as the first argument, which will be applied to each facet. To apply the transparency using map, I set up an anonymous lambda function that gets the current Axes (gca), selects its background (patch), and sets its transparency to full.

# As for the second map argument, it sends a pandas Series to the function specified by the first argument. This Series is filtered to include only the column specified by the second map argument, with only the rows appropriate for each facet. In this case, I exploit the fact that the 'many_cat_var' column is filled with copies of the categorical feature string to specify the text string, with hardcoded positional values appropriate to the plot. (map also sends a few general keyword arguments like 'color' automatically to the specified function, hence the need for **kwargs to capture them despite not specifying any myself.) One downside to this approach is that the x-axis labels get replaced with 'many_cat_var' after the map call, thus requiring the addition of a set_xlabels function call to reset the string.
