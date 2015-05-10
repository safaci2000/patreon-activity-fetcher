#!/usr/bin/env python3
"""
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import argparse
from bokeh.charts import Dot
from activity_fetcher.database import Database
from activity_fetcher.patreon_api import Patreon
from bokeh.plotting import figure, output_file, show


def visualize_example():
    db = Database()
    result = db.retrieve_earnings()
    keys = []
    for key in result:
        keys.append(key)
    output_file("data/revenue.html")
    dots = Dot(
    result, cat=['Pledge Sum', 'Lifetime Pledge Sum'],
    title="Revnue Monthly Breakdown", ylabel='Revenue', legend=True
    )

    show(dots)

def lines_example():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("data/lines.html", title="line plot example")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    show(p)

def main():
    """
    Arge parsing is a bit pointless atm, but might be useful at some point in the future.
    :return:
    """
    parser = argparse.ArgumentParser(description='Patreon Activity Fetcher')
    parser.add_argument('--fetch', dest='fetch', default=False, action='store_true', help='fetch report')
    parser.add_argument('--visualize', dest='visualize', default=False, action='store_true', help='visualize report')
    parser.add_argument('--data-file', dest='data_file', default=None, type=str,
                        action='store', help='Skip API retrieve and treat the specified file as input instead')
    patreon = Patreon()

    args = parser.parse_args()

    if args.fetch:
        data = None
        if args.data_file is not None:
            data = patreon.load_api_data(args.data_file)
        else:
            data = patreon.load_api_data()
        patreon.process_data(data)
    elif args.visualize:
        visualize_example()
    else:
        patreon.cookie_login()


if __name__ == "__main__":
    main()

