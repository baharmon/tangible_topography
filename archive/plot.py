def write_results(flow_cells, depression_cells, peak_cells, pit_cells, ridge_cells, valley_cells, flow_distance, peak_distance, pit_distance, ridge_distance, valley_distance):
    """plot the percent of cells with depressions and the minumum distance of mean concentrated flow points from the reference for each experiment"""


flow_plot = os.path.join(render, "flow_cells.png")
depression_plot = os.path.join(render, "depression_cells.png")
peak_plot = os.path.join(render, "peak_cells.png")
pit_plot = os.path.join(render, "pit_cells.png")
ridge_plot = os.path.join(render, "ridge_cells.png")
valley_plot = os.path.join(render, "valley_cells.png")

flow_distance_plot = os.path.join(render, "flow_distance.png")
peak_distance_plot = os.path.join(render, "peak_distance.png")
pit_distance_plot = os.path.join(render, "pit_distance.png")
ridge_distance_plot = os.path.join(render, "ridge_distance.png")
valley_distance_plot = os.path.join(render, "valley_distance.png")

# plot flow
plt.figure(frameon=False, figsize=(5, 15), tight_layout=True)
labels = ('Reference', ' Reference', ' Reference', ' Reference', ' Reference', 'Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = flow_cells
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True) # width=0.5
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Percent cells')
# plt.title('Percent of cells with concentrated flow')
plt.savefig(flow_plot, dpi=300, transparent=True)
plt.close()

# plot depressions
plt.figure(frameon=False, figsize=(5, 15), tight_layout=True)
labels = ('Reference', ' Reference', ' Reference', ' Reference', ' Reference', 'Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = depression_cells
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Percent cells')
# plt.title('Percent of cells with depressions for each experiment')
plt.savefig(depression_plot, dpi=300, transparent=True)
plt.close()

# plot peaks
plt.figure(frameon=False, figsize=(5, 15), tight_layout=True)
labels = ('Reference', ' Reference', ' Reference', ' Reference', ' Reference', 'Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = peak_cells
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Percent cells')
# plt.title('Percent of cells with peaks')
plt.savefig(peak_plot, dpi=300, transparent=True)
plt.close()

# plot pits
plt.figure(frameon=False, figsize=(5, 15), tight_layout=True)
labels = ('Reference', ' Reference', ' Reference', ' Reference', ' Reference', 'Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = pit_cells
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Percent cells')
# plt.title('Percent of cells with pits')
plt.savefig(pit_plot, dpi=300, transparent=True)
plt.close()

# plot ridges
plt.figure(frameon=False, figsize=(5, 15), tight_layout=True)
labels = ('Reference', ' Reference', ' Reference', ' Reference', ' Reference', 'Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = ridge_cells
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Percent cells')
# plt.title('Percent of cells with ridges')
plt.savefig(ridge_plot, dpi=300, transparent=True)
plt.close()

# plot valley_cells
plt.figure(frameon=False, figsize=(5, 15), tight_layout=True)
labels = ('Reference', ' Reference', ' Reference', ' Reference', ' Reference', 'Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = valley_cells
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Percent cells')
# plt.title('Percent of cells with valleys')
plt.savefig(valley_plot, dpi=300, transparent=True)
plt.close()

# plot flow distance
plt.figure(frameon=False, figsize=(5, 5), tight_layout=True)
labels = ('Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = flow_distance
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Cumulative distance (ft)')
# plt.title('Sum of minimum distance of concentrated flow from reference')
plt.savefig(flow_distance_plot, dpi=300, transparent=True)
plt.close()

# plot peak distance
plt.figure(frameon=False, figsize=(5, 5), tight_layout=True)
labels = ('Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = peak_distance
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Cumulative distance (ft)')
# plt.title('Sum of minimum distance of peaks from reference')
plt.savefig(peak_distance_plot, dpi=300, transparent=True)
plt.close()

# plot pit distance
plt.figure(frameon=False, figsize=(5, 5), tight_layout=True)
labels = ('Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = pit_distance
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Cumulative distance (ft)')
# plt.title('Sum of minimum distance of pits from reference')
plt.savefig(pit_distance_plot, dpi=300, transparent=True)
plt.close()

# plot ridge distance
plt.figure(frameon=False, figsize=(5, 5), tight_layout=True)
labels = ('Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = ridge_distance
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Cumulative distance (ft)')
# plt.title('Sum of minimum distance of ridge from reference')
plt.savefig(ridge_distance_plot, dpi=300, transparent=True)
plt.close()

# plot valley distance
plt.figure(frameon=False, figsize=(5, 5), tight_layout=True)
labels = ('Digital', 'Analog', 'Augmented', 'Difference', 'Flow')
x = range(len(labels))
y = valley_distance
plt.bar(x, y, color="gray", align='center', alpha=0.5, antialiased=True)
plt.xticks(x, labels)
plt.xlabel('Experiment')
plt.ylabel('Cumulative distance (ft)')
# plt.title('Sum of minimum distance of valleys from reference')
plt.savefig(valley_distance_plot, dpi=300, transparent=True)
plt.close()
