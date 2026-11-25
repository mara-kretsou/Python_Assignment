"""Maps test points to ideal function using allowed deviations."""

import pandas as pd
from calculations import is_mapping_allowed, select_closest_matches
import numpy as np


class PointMapper:
    """Maps test points to the selected ideal functions."""

    def __init__(self, ideal_data):
        """Initialize the mapper with the ideal function data."""
        self.ideal_data = ideal_data

    def map_points(self, test_data, allowed_differences):
        """Match test points to ideal functions within allowed deviations."""
        matched_tests = []
        for test_number in range(len(test_data)):
            test_point = test_data.iloc[test_number]
            test_x = test_point["x"]
            test_y = test_point["y"]
            for ideal_name in allowed_differences:
                matching_rows = self.ideal_data.loc[
                    np.isclose(self.ideal_data["x"], test_x, rtol=0, atol=1e-8)
                ]
                if matching_rows.empty:
                    raise ValueError(f"No ideal data found for x={test_x}")
                matching_value = matching_rows[ideal_name].iloc[0]
                deviation = abs(test_y - matching_value)
                if is_mapping_allowed(deviation, allowed_differences[ideal_name]):
                    matched_tests.append(
                        [test_number, test_x, test_y, ideal_name, deviation]
                    )
        matches_table = pd.DataFrame(
            matched_tests,
            columns=["test_row_id", "x", "y", "ideal_function", "deviation"],
        )
        final_matches = select_closest_matches(matches_table)
        return final_matches

    def find_unmatched_points(self, test_data, final_matches):
        """Find test points that have not been matched."""
        indexed_tests = test_data.reset_index(drop=True)

        unmatched_mask = ~indexed_tests.index.isin(final_matches["test_row_id"])

        return indexed_tests.loc[unmatched_mask].copy()
