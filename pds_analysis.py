# -*- coding: utf-8 -*-

# Imports
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage
import shifterator as sh
from collections import Counter
import plotly.figure_factory as ff
from tabulate import tabulate


# Functions
def get_dict(file):
    dicty = {}
    dict_file = open(file, 'r', encoding = 'utf-8')
    lines = dict_file.readlines()
    dict_file.close()
    for line in lines:
        edit_line = line.rstrip('\n')
        dict_entry = edit_line.split(',')
        dicty[dict_entry[0]] = int(dict_entry[1])
    return dicty

# Get the ousiometer dictionaries for Power, Danger, Structure
dat = pd.read_csv('ousiometry_data.txt', delimiter = '\t')
dat = dat.set_index('word')
power_dict = dat['power'].to_dict()
danger_dict = dat['danger'].to_dict()
structure_dict = dat['structure.1'].to_dict()

# Get Power, Danger, Structure scores for each text downloaded.
def get_pds_data(window, axes, axis, var1, var2, return_df = False):
    pds_dat = []
    for file in os.listdir('dicts'):
        file_title = file.replace('.txt', '')
        file_dict = get_dict('dicts/' + file)
        num_words = sum(file_dict.values())
        if num_words >= 40000:
            p = 0
            d = 0
            s = 0
            num_p = 0
            num_d = 0
            num_s = 0
            for word in file_dict.keys():
                try:
                    if abs(power_dict[word]) > window:
                        p += power_dict[word] * file_dict[word]
                        num_p += file_dict[word]
                    if abs(power_dict[word]) > window:
                        d += danger_dict[word] * file_dict[word]
                        num_d += file_dict[word]
                    if abs(power_dict[word]) > window:
                        s += structure_dict[word] * file_dict[word]
                        num_s += file_dict[word]
                except:
                    pass
            pds_dat.append((file_title, p/num_p, d/num_d, s/num_s))
    
    # Results in data frame
    pds_results = pd.DataFrame(pds_dat)
    pds_results.columns = ['Title', 'Power', 'Danger', 'Structure']
    
    # Plot results
    plt.sca(axes[axis[0],axis[1]])
    plt.scatter(pds_results[var1], pds_results[var2])
    plt.xlabel('{} Score'.format(var1))
    plt.ylabel('{} Score'.format(var2))
    plt.title('Lens = {}'.format(window))
    
    if return_df:
        return pds_results

def get_tv_show_meaning_plot(var1, var2, return_dat = False):
    fig, axes = plt.subplots(4,2,figsize = (8,12))
    fig.tight_layout(h_pad=4,w_pad=3)
    fig.suptitle('TV Show Essential Meaning P-D Space')
    plt.subplots_adjust(top=0.915)
    get_pds_data(0.0, axes, (0,0), var1, var2)
    get_pds_data(0.05, axes, (0,1), var1, var2)
    get_pds_data(0.10, axes, (1,0), var1, var2)
    get_pds_data(0.15, axes, (1,1), var1, var2)
    data = get_pds_data(0.20, axes, (2,0), var1, var2, True)
    get_pds_data(0.25, axes, (2,1), var1, var2)
    get_pds_data(0.30, axes, (3,0), var1, var2)
    get_pds_data(0.35, axes, (3,1), var1, var2)
    plt.savefig('figures/{s1}{s2}'.format(s1=var1,s2=var2), bbox_inches = 'tight')
    plt.show()
    return data
    
data = get_tv_show_meaning_plot('Power', 'Danger', True)
get_tv_show_meaning_plot('Power', 'Structure')
get_tv_show_meaning_plot('Danger', 'Structure')


def get_clustering_plots(data, var1, var2, num_clusters, save_fig = False, return_data = False):
    X = pd.DataFrame(data)
    X.columns = ['Title','Power','Danger','Structure']
    X = X[['Power','Danger','Structure']]
    kmeans = KMeans(n_clusters = num_clusters, random_state = 0).fit(X)
    kmeans.labels_
    kmeans.cluster_centers_
    for i in range(num_clusters):
        X_dat = []
        Y_dat = []
        for index, label in enumerate(kmeans.labels_):
            if label == i:
                X_dat.append(X[var1][index])
                Y_dat.append(X[var2][index])
        plt.scatter(X_dat, Y_dat)
    plt.xlabel('{} Scores'.format(var1))
    plt.ylabel('{} Scores'.format(var2))
    plt.title('Kmeans Scatter Plot: {s1} and {s2}'.format(s1=var1,s2=var2))
    plt.legend(['Group ' + str(x) for x in range(num_clusters)])
    if save_fig:
        plt.savefig('figures/kmeans{s1}{s2}{s3}cluster'.format(s1=var1,s2=var2,s3=num_clusters), bbox_inches = 'tight')
        plt.show()
    if return_data:
        return X, kmeans.labels_

get_clustering_plots(data,'Power','Danger',3)
get_clustering_plots(data,'Power','Danger',4)
get_clustering_plots(data,'Power','Danger',5)
get_clustering_plots(data,'Power','Danger',6) # Seems like a reasonable number of clusters
get_clustering_plots(data,'Power','Danger',7)
get_clustering_plots(data,'Power','Danger',8)
get_clustering_plots(data,'Power','Danger',9)

combs = [['Power','Danger'],['Power','Structure'],['Danger','Structure']]
fig, axes = plt.subplots(3,1,figsize = (12,12))
fig.tight_layout(h_pad=4,w_pad=3)
fig.suptitle('Kmeans Clustering: 6 Clusters')
plt.subplots_adjust(top=0.915)
for i in range(3):
    plt.sca(axes[i])
    if i < 2:
        get_clustering_plots(data, combs[i][0], combs[i][1], 6)
    else:
        X, labels = get_clustering_plots(data,combs[i][0],combs[i][1],6,return_data=True)
plt.savefig('figures/kmeans6cluster', bbox_inches = 'tight')
plt.show()

# Let's do some hierarchical clustering to validate num_clusters choice
X = pd.DataFrame(data)
X.columns = ['Title','Power','Danger','Structure']
X = X[['Power','Danger','Structure']]
links = linkage(X, method = 'ward')

# Plot dendrogram
dgram = dendrogram(links)
plt.title('Hierarchical Method: Dendrogram')
plt.ylabel('Euclidean distance')
plt.gca().axes.get_xaxis().set_visible(False)
plt.savefig('figures/dendogram', bbox_inches = 'tight')
plt.show()


# Lets create word shifts between aggregated group corpuses
counters = [Counter(), Counter(), Counter(), Counter(), Counter(), Counter()]
for i, title in enumerate(data['Title']):
    group = labels[i]
    tv_show_dict = get_dict('dicts/' + title + '.txt')
    counters[group].update(tv_show_dict)

# Word shifts for Groups 3 and 4
power_shift_34 = sh.WeightedAvgShift(type2freq_1 = counters[3],
                                        type2freq_2 = counters[4], 
                                        type2score_1 = power_dict,
                                        reference_value = 'average',
                                        stop_lens=[(-.2,.2)],
                                        handle_missing_scores = 'exclude')
danger_shift_34 = sh.WeightedAvgShift(type2freq_1 = counters[3],
                                        type2freq_2 = counters[4], 
                                        type2score_1 = danger_dict,
                                        reference_value = 'average',
                                        stop_lens=[(-.2,.2)],
                                        handle_missing_scores = 'exclude')
structure_shift_34 = sh.WeightedAvgShift(type2freq_1 = counters[3],
                                        type2freq_2 = counters[4], 
                                        type2score_1 = structure_dict,
                                        reference_value = 'average',
                                        stop_lens=[(-.2,.2)],
                                        handle_missing_scores = 'exclude')

fig, axes = plt.subplots(1,3,figsize = (12,12))
fig.tight_layout(h_pad=4,w_pad=10)
fig.suptitle('Group 3 and Group 4 Word Shifts')
plt.subplots_adjust(top=0.915)
power_shift_34.get_shift_graph(detailed=True, system_names=['Group 3', 'Group 4'], cumulative_inset=False, text_size_inset=False, ax = axes[0])
danger_shift_34.get_shift_graph(detailed=True, system_names=['Group 3', 'Group 4'], cumulative_inset=False, text_size_inset=False, ax = axes[1])
structure_shift_34.get_shift_graph(detailed=True, system_names=['Group 3', 'Group 4'], cumulative_inset=False, text_size_inset=False, ax = axes[2])
plt.sca(axes[0])
plt.title('Power Word Shift')
plt.sca(axes[1])
plt.title('Danger Word Shift')
plt.sca(axes[2])
plt.title('Structure Word Shift')
plt.savefig('figures/wordshifts34', bbox_inches = 'tight')
plt.show()
    
# Word shifts for Groups 0 and 5
power_shift_05 = sh.WeightedAvgShift(type2freq_1 = counters[0],
                                        type2freq_2 = counters[5], 
                                        type2score_1 = power_dict,
                                        reference_value = 'average',
                                        stop_lens=[(-.2,.2)],
                                        handle_missing_scores = 'exclude')
danger_shift_05 = sh.WeightedAvgShift(type2freq_1 = counters[0],
                                        type2freq_2 = counters[5], 
                                        type2score_1 = danger_dict,
                                        reference_value = 'average',
                                        stop_lens=[(-.2,.2)],
                                        handle_missing_scores = 'exclude')
structure_shift_05 = sh.WeightedAvgShift(type2freq_1 = counters[0],
                                        type2freq_2 = counters[5], 
                                        type2score_1 = structure_dict,
                                        reference_value = 'average',
                                        stop_lens=[(-.2,.2)],
                                        handle_missing_scores = 'exclude')

fig, axes = plt.subplots(1,3,figsize = (12,12))
fig.tight_layout(h_pad=4,w_pad=10)
fig.suptitle('Group 0 and Group 5 Word Shifts')
plt.subplots_adjust(top=0.915)
power_shift_05.get_shift_graph(detailed=True, system_names=['Group 0', 'Group 5'], cumulative_inset=False, text_size_inset=False, ax = axes[0])
danger_shift_05.get_shift_graph(detailed=True, system_names=['Group 0', 'Group 5'], cumulative_inset=False, text_size_inset=False, ax = axes[1])
structure_shift_05.get_shift_graph(detailed=True, system_names=['Group 0', 'Group 5'], cumulative_inset=False, text_size_inset=False, ax = axes[2])
plt.sca(axes[0])
plt.title('Power Word Shift')
plt.sca(axes[1])
plt.title('Danger Word Shift')
plt.sca(axes[2])
plt.title('Structure Word Shift')
plt.savefig('figures/wordshifts05', bbox_inches = 'tight')
plt.show()

# Make table
data['Group'] = labels
data = data.set_index('Title')
data = data.sort_values(by = 'Group')
#tab_fig = ff.create_table(data)
#tab_fig.show()
#tab_fig.write_image('figures/table.png')

tab = tabulate(data, headers = data.columns, tablefmt='latex')
print(tab)


        
        