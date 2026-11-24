"""Unit tests for dynamic Bokeh visualizations."""

import pandas as pd
from visualizer import create_function_plots
from bokeh.models.glyphs import VArea

def test_dynamic_function_plot():
    """Check that dynamic Bokeh plots are generated correctly."""
    training = pd.DataFrame({"x": [0, 1, 2], "y1": [ 0, 1, 2]})
    ideal = pd.DataFrame({"x": [0, 1, 2], "y17": [ 0, 1, 2]})

    best_matches = {"y1": "y17"}

    matches = pd.DataFrame({"x": [1], "y": [1],"deviation": [0.0], "ideal_function": ["y17"]})

    allowed = {"y17": 0.5}

    unmatched = pd.DataFrame({"x": [2], "y": [5]})

    plots = create_function_plots(training, ideal, best_matches, matches,allowed,unmatched)

    assert len(plots) == 3
    assert plots[0].title.text == "Training y1 and Ideal y17"

    bands = [
            renderer
            for renderer in plots[0].renderers
            if hasattr(renderer, "glyph")
            and isinstance(renderer.glyph, VArea)
        ]

    assert len(bands) == 1
