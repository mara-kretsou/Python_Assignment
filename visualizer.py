"""Create dynamic Bokeh visualizations for function analysis."""

from bokeh.plotting import figure
from bokeh.palettes import Category10


def create_function_plots(
    training_data,
    ideal_data,
    best_matches,
    final_matches,
    allowed_differences,
    unmatched_tests,
):
    """Create plots for the selected ideal functions.

    Args:
      training_data: DataFrame containing training functions.
      ideal_data: DataFrame containing ideal functions.
      best_matches: Dictionary mapping training to ideal functions.
      final_matches: DataFrame containing matched test points.
      allowed_differences: Dictionary of allowed deviations.
      unmatched_tests: DataFrame containing unmatched test points.

    Returns:
      List of Bokeh figures, one for each training function.
    """
    plots = []

    for training_name, ideal_name in best_matches.items():
        y_min = min(training_data[training_name].min(), ideal_data[ideal_name].min())
        y_max = max(training_data[training_name].max(), ideal_data[ideal_name].max())

        padding = max((y_max - y_min) * 0.1, 1.0)

        plot = figure(
            title=f"Training {training_name} and Ideal {ideal_name}",
            y_range=(y_min - padding, y_max + padding),
        )

        plot.xaxis.axis_label = "x"
        plot.yaxis.axis_label = "y"

        plot.line(
            training_data["x"],
            training_data[training_name],
            legend_label=f"Training {training_name}",
        )

        plot.line(
            ideal_data["x"],
            ideal_data[ideal_name],
            color="red",
            line_dash="dashed",
            legend_label=f"Ideal {ideal_name}",
        )

        tolerance = allowed_differences[ideal_name]

        lower_limit = ideal_data[ideal_name] - tolerance
        upper_limit = ideal_data[ideal_name] + tolerance

        plot.varea(
            x=ideal_data["x"],
            y1=lower_limit,
            y2=upper_limit,
            fill_alpha=0.2,
            color="orange",
            legend_label="Allowed deviation",
        )

        selected_tests = final_matches[final_matches["ideal_function"] == ideal_name]

        plot.scatter(
            selected_tests["x"], selected_tests["y"], legend_label="Matched Test Points"
        )

        plot.scatter(
            unmatched_tests["x"],
            unmatched_tests["y"],
            marker="x",
            color="gray",
            size=7,
            alpha=0.5,
            legend_label="Unmatched Test Points",
        )

        plots.append(plot)

    deviation_plot = figure(title="Deviation of Matched Points")
    deviation_plot.xaxis.axis_label= "Test x-value"
    deviation_plot.yaxis.axis_label= "Absolute Deviation"

    for i, (ideal_name, points) in enumerate(final_matches.groupby("ideal_function")):
        deviation_plot.scatter(
            points["x"],
            points["deviation"],
            color=Category10[10][i%10],
            legend_label=ideal_name,
        )
    
    unmatched_plot = figure(title="Unmatched Test Points")
    unmatched_plot.xaxis.axis_label= "Test x-value"
    unmatched_plot.yaxis.axis_label= "Test y-value"
    unmatched_plot.scatter(unmatched_tests["x"], unmatched_tests["y"])

    plots.extend([deviation_plot, unmatched_plot])

    return plots
