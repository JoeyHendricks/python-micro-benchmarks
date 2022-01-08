<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/QuickPotato/blob/master/images/banner-wide-with-text.jpg"/>
</p>

<!-- TAG LINE -->
<h3 align="center">Profile and test to gain insights into the performance of your beautiful Python code</h3>
<p align="center">
    <a href="https://github.com/JoeyHendricks/QuickPotato">View Demo</a> -
    <a href="https://github.com/JoeyHendricks/QuickPotato/issues">Report Bug</a> -
    <a href="https://github.com/JoeyHendricks/QuickPotato/issues">Request Feature</a>
</p>

<!-- BADGES -->
<div align="center">
<a href="https://github.com/JoeyHendricks/QuickPotato/graphs/contributors"><img src="https://img.shields.io/github/contributors/JoeyHendricks/QuickPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/QuickPotato/network/members"><img src="https://img.shields.io/github/forks/JoeyHendricks/QuickPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/QuickPotato/stargazers"><img src="https://img.shields.io/github/stars/JoeyHendricks/QuickPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/QuickPotato/issues"><img src="https://img.shields.io/github/issues/JoeyHendricks/QuickPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/QuickPotato/blob/master/LICENSE.md"><img src="https://img.shields.io/github/license/JoeyHendricks/QuickPotato?style=for-the-badge"></a>
<a href="https://www.linkedin.com/in/joey-hendricks/"><img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555"></a>
</div>
<br>

<!-- CONTENT -->
## QuickPotato in a nutshell

QuickPotato is a Python library that aims to make it easier to rapidly profile your software and produce powerful 
code visualizations that enables you to quickly investigate where potential performance bottlenecks are hidden.

Also, QuickPotato is trying to provide you with a path to add an automated performance testing angle to 
your regular unit tests or test-driven development test cases allowing you to test your code early in the 
development life cycle in a simple, reliable, and fast way.

## Installation

Install using [pip](https://pip.pypa.io/en/stable/) or download the source code from GitHub.
```bash
pip install QuickPotato
```

## Generating Flame Graphs

[![Example of a Python flame graph](/images/python-code-flame-graph.png "flame graph Python")](
https://github.com/JoeyHendricks/QuickPotato/blob/master/images/python-code-flame-graph.png)

How to interpret the Flame Graphs generated by QuickPotato together with [d3-flame-graph](https://github.com/spiermar/d3-flame-graph):

- Each box is a function in the stack
- The y-axis shows the stack depth the top box shows what was on the CPU.
- The x-axis **does not show time** but spans the population and is ordered alphabetically.
- The width of the box show how long it was on-CPU or was part of an parent function that was on-CPU.

> If you are unfamiliar with Flame Graphs you can best read about them on [Brendan Greg's website](http://www.brendangregg.com/flamegraphs.html).

In the following way you can generate a Python flame graph with QuickPotato:

```python
from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as pt
from QuickPotato.visualizations.visualizations import FlameGraph

# Create a test case
pt.test_case_name = "FlameGraph"

pt.run(
  method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
  arguments=["joey hendricks"],  # <-- Your arguments go here.
  iteration=10,  # <-- The number of times you want to execute this method.
  pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Generate the flame graph visualizations to analyse your code performance.
FlameGraph(pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")
```

> Short notice on an issue that occurred in my code while using QuicPotato
> If QuicPotato cannot find the starting function no Flame Graph will be displayed or a weird one.
> To fix this simply encapsulate youur code under a simple function and profile that.
> I will come with a fix for this soon an example for this can be found [here](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/tests/test_project.py)

## Generating Heatmaps (Beta)

[![Example of a Python heatmap](/images/python-code-performance-heatmap.png "heatmap Python")](
https://github.com/JoeyHendricks/QuickPotato/blob/master/images/python-code-performance-heatmap.png)

How does a by QuickPotato generated D3 heatmap work:

- Every box in the heatmap is a function
- The y-axis is made up of functions ordered by its latency.
- The x-axis spans the amount of sample (one sample is on execution of your code) and is separated into 
  columns of test id's (one test id is one completely executed test).
- The color shows the speeds of the function to more red a box is the more time there was spent.
- All boxes are clickable and will give you information about that particular function.

In the following way you can generate a Python heatmap with QuickPotato:

```python
from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as pt
from QuickPotato.visualizations.visualizations import HeatMap

# Create a test case
pt.test_case_name = "Heatmap"

# Attach the method from which you want to performance test
pt.run(
  method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
  arguments=["joey hendricks"],  # <-- Your arguments go here.
  iteration=10,  # <-- The number of times you want to execute this method.
  pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Generate the heatmap visualizations to analyse your code performance.
HeatMap(pt.test_case_name, test_ids=[pt.current_test_id, pt.previous_test_id]).export("C:\\temp\\")

```
> This D3 visualization is still being tweaked and improved if you encounter any issue with it please open an issue. 
> (Your feedback is appreciated!)

## Generating a CSV file

[![Example of a csv file](/images/csv-example.jpg "csv file")](
https://github.com/JoeyHendricks/QuickPotato/blob/master/images/csv-example.jpg)

You can generate a CSV export in the following way:

```python
from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as pt
from QuickPotato.visualizations.visualizations import CsvFile

# Create a test case
pt.test_case_name = "exporting to csv"

# Attach the method from which you want to performance test
pt.run(
  method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
  arguments=["joey hendricks"],  # <-- Your arguments go here.
  iteration=10,  # <-- The number of times you want to execute this method.
  pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Export the sample into csv file for further analysis
CsvFile(pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")

```

## Generating a Bar Chart

[![Example of a bar chart](/images/python-code-performance-bar-chart.png "a bar chart")](
https://github.com/JoeyHendricks/QuickPotato/blob/master/images/python-code-performance-bar-chart.png)

How to interpret the bar chart generate by QuickPotato:

- each color is method executed in your performance test.
- The graph is ordered by latency from slowest to fastest (This can be disabled.)
- The Y axis is time spent per method.
- The X axis made up out of samples and divided per test id.
- You can exclude a method by clicking the method name in the legend.
  Also, by double clicking a method name you can deselect all other methods.
- On the top right-hand side Plotly's control bar can be found to further interact with the graph.

You can generate a simple interactive bar chart in the following way:

```python
from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as pt
from QuickPotato.visualizations.visualizations import BarChart

# Create a test case
pt.test_case_name = "bar chart"

# Attach the method from which you want to performance test
pt.run(
  method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
  arguments=["joey hendricks"],  # <-- Your arguments go here.
  iteration=10,  # <-- The number of times you want to execute this method.
  pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Generate visualizations to analyse your code.
BarChart(pt.test_case_name, test_ids=[pt.current_test_id, pt.previous_test_id]).export("C:\\temp\\")

```

## Boundary testing

Within QuickPotato, it is possible to create a performance test that validates if your code breaches any 
defined boundary or not. An example of this sort of test can be found in the snippet below:

```python
from QuickPotato import micro_benchmark as pt
from examples.non_intrusive_example_code import FancyCode

# Create a test case
pt.test_case_name = "test_performance"  # <-- Define test case name

# Defining the boundaries
pt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}

# Execute your code in a non-intrusive way
pt.run(
  method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
  arguments=["joey hendricks"],  # <-- Your arguments go here.
  iteration=10,  # <-- The number of times you want to execute this method.
  pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Analyse results for change True if there is no change otherwise False
results = pt.compare()

```

## Regression testing

It is also possible to verify that there is no regression between the current benchmark and a previous baseline.
The method for creating such a test can also be found in the snippet below:

```python
from QuickPotato import micro_benchmark as pt
from QuickPotato._configuration.config import options
from examples.non_intrusive_example_code import FancyCode

# Disabling this setting will filter out untested or failed test-id's out of your baseline selection.
options.enable_policy_to_filter_out_invalid_test_ids = False

# Create a test case
pt.test_case_name = "test_performance"  # <-- Define test case name

# Execute your code in a non-intrusive way
pt.run(
  method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
  arguments=["joey hendricks"],  # <-- Your arguments go here.
  iteration=10,  # <-- The number of times you want to execute this method.
  pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Analyse results for change True if there is no change otherwise False
results = pt.compare()
```

## Integrating with unit testing frameworks

Uplifting basic performance tests into a test framework is easy within QuickPotato and can be achieved 
the following way:

````python
from QuickPotato import micro_benchmark as pt
from QuickPotato._configuration.config import options
from examples.non_intrusive_example_code import *
import unittest


class TestPerformance(unittest.TestCase):

  def setUp(self):
    """
    Disable the selection of failed or untested test results.
    This will make sure QuickPotato will only compare you tests against a valid baseline.
    """
    options.enable_policy_to_filter_out_invalid_test_ids = False

  def tearDown(self):
    """
    Enabling the selection of failed or untested test results.
    We enable this setting after the test so it will not bother you when quick profiling.
    """
    options.enable_policy_to_filter_out_invalid_test_ids = True

  def test_performance_of_method(self):
    """
    Your performance test.
    """
    # Create a test case
    pt.test_case_name = "test_performance"  # <-- Define test case name

    # Defining the boundaries
    pt.max_and_min_boundary_for_average = {"max": 10, "min": 0.001}

    # Execute your code in a non-intrusive way
    pt.run(
      method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
      arguments=["joey hendricks"],  # <-- Your arguments go here.
      iteration=10,  # <-- The number of times you want to execute this method.
      pacing=0  # <-- How much seconds you want to wait between iterations.
    )

    # Pass or fail the performance test
    self.assertTrue(pt.compare())
    self.assertTrue(pt.verify_boundaries())

````

## Coming soon

Some features which I am planning to add to QuickPotato soon:

- Improving the heatmap
- Scatter plot
- Creating a virtual map of your code
- Time Line (Showing from left to right the time spent per action in your code.)

## Learn more about QuickPotato

If you want to learn more about test driven performance testing and want to 
see how this project reached its current state? 
Then I would encourage you to check out the following resources:

- 11/07/2020: [Don’t lose your mind over slow code check your performance sanity.(English)](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 
- 08/10/2020: [My recording about QuickPotato @NeotysPAC 2020. (English)](https://www.youtube.com/watch?v=AWlhalEywEw) 
- 15/12/2020: [Interview about QuickPotato @TestGuild 2020. (English)](https://testguild.com/podcast/performance/p56-joey/)
- 12/01/2020: [An article I wrote for Neotys about my @NeotysPAC 2020 presentation. (English)](https://www.neotys.com/blog/neotyspac-performance-testing-unit-level-joey-hendricks/)

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/dashboard?id=JoeyHendricks_QuickPotato)