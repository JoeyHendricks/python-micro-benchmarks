from ..statistical.verification import check_max_boundary, check_min_boundary, check_letter_rank_boundary
from ..benchmarking.result_interpreters import ProfilerStatisticsInterpreter
from ..statistical.heuristics import StatisticalDistanceTest
from ..benchmarking.code_instrumentation import Profiler
from ..statistical.measurements import Statistics
from .._database.collection import Crud
from multiprocessing import Process
from datetime import datetime
import warnings
import string
import random
import time


class MicroBenchmark(Crud):

    LETTER_RANK_DECISION_MATRIX = [

        {"wasserstein_boundary": 0.030, "kolmogorov_smirnov_boundary": 0.300, "rank": "S"},
        {"wasserstein_boundary": 0.060, "kolmogorov_smirnov_boundary": 0.500, "rank": "A"},
        {"wasserstein_boundary": 0.100, "kolmogorov_smirnov_boundary": 0.700, "rank": "B"},
        {"wasserstein_boundary": 0.125, "kolmogorov_smirnov_boundary": 0.800, "rank": "C"},
        {"wasserstein_boundary": 0.150, "kolmogorov_smirnov_boundary": 1.000, "rank": "D"},
        {"wasserstein_boundary": 0.200, "kolmogorov_smirnov_boundary": 1.200, "rank": "E"},
        {"wasserstein_boundary": 0.250, "kolmogorov_smirnov_boundary": 1.400, "rank": "F"},

    ]

    def __init__(self):
        super(MicroBenchmark, self).__init__()

    def _execute_code_under_test(self, method: object, arguments=None, iteration=1, pacing=0) -> None:
        """

        :return:
        """
        # Iterations per test
        for _ in range(0, iteration):

            # Pacing in between actions.
            time.sleep(pacing)

            # Random ID.
            sample_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            # Run method and profile it
            pf = Profiler()
            if arguments is None:
                pf.profile_method_under_test(method)
            else:
                pf.profile_method_under_test(method, *arguments)

            # Wrangle data into format and upload it to _database
            ProfilerStatisticsInterpreter(
                performance_statistics=pf.performance_statistics,
                total_response_time=pf.total_response_time,
                connection_url=self.database_connection_url,
                test_case_name=self.test_case_name,
                test_id=self.current_test_id,
                method_name=method.__name__,
                sample_id=sample_id
            )

    @property
    def benchmark_statistics(self) -> Statistics:
        """
        All of the performance measurements that are collected by the benchmark.

        Returns
        -------
            A statistical object that contains all benchmark measurements.
        """
        response_times = self.select_benchmark_profiled_method_cumulative_latency(
            url=self.database_connection_url,
            tcn=self.test_case_name,
            test_id=self.current_test_id
        )
        return Statistics(
            measurements=response_times
        )

    @property
    def baseline_statistics(self) -> Statistics:
        """
        All of the performance measurements that are collected by the baseline.

        Returns
        -------
            A statistical object that contains all baseline measurements.
        """
        response_times = self.select_benchmark_profiled_method_cumulative_latency(
            url=self.database_connection_url,
            tcn=self.test_case_name,
            test_id=self.previous_test_id
        )
        return Statistics(
            measurements=response_times
        )

    @property
    def distance_statistics(self) -> StatisticalDistanceTest:
        """

        :return:
        """
        return StatisticalDistanceTest(
            population_a=self.baseline_statistics.raw_data,
            population_b=self.benchmark_statistics.raw_data,
            letter_rank_matrix=self.LETTER_RANK_DECISION_MATRIX
        )

    @property
    def test_case_name(self) -> str:
        """

        :return:
        """
        if "test_case_name" in self.__dict__:

            return self.__dict__["test_case_name"]

        else:
            return "default"

    @property
    def current_test_id(self) -> float or None:
        """

        :return:
        """
        if "current_test_id" in self.__dict__:

            return self.__dict__["current_test_id"]

        else:
            return None

    @property
    def previous_test_id(self) -> float or None:
        """

        :return:
        """
        if "previous_test_id" in self.__dict__:

            return self.__dict__["previous_test_id"]

        else:
            return None

    @current_test_id.setter
    def current_test_id(self, value):
        """

        """
        self.__dict__["current_test_id"] = value

    @previous_test_id.setter
    def previous_test_id(self, value):
        """

        """
        self.__dict__["previous_test_id"] = value

    @property
    def database_connection_url(self) -> str:
        """

        :return:
        """
        if "database_connection_url" not in self.__dict__:
            return self._create_default_db_url()

        else:
            return self.__dict__["database_connection_url"]

    @test_case_name.setter
    def test_case_name(self, value: str) -> None:
        """
        Will update the test case name with the provided value.
        When the test case name is changed by a performance unit test.
        The following automatic action will be performed:

            - Create the necessary tables in target _database.
            - Find the previous test id
            - Generate the current test id

        :param value: The new test case name defined by the user.
        """
        # create tables in database where benchmark needs to save statistics.
        self._verify_and_create_relevant_tables_in_database(
            url=self.database_connection_url,
            tcn=value
        )
        self.__dict__["test_case_name"] = value

        # reset the performance test identifying variables.
        benchmarks = self.select_benchmarks_with_statistics(
            url=self.database_connection_url,
            tcn=value,
            number=1
        )
        self.previous_test_id = benchmarks[0] if len(benchmarks) > 0 else None
        self.current_test_id = datetime.now().timestamp()

    @database_connection_url.setter
    def database_connection_url(self, value: str) -> None:
        """

        :param value:
        :return:
        """
        self.__dict__['database_connection_url'] = value

    @staticmethod
    def verify_boundaries(boundaries: list) -> bool or None:
        """

        :return:
        """
        results = []
        for boundary in boundaries:
            results.append(
                {
                    "boundary_name": boundary["name"],
                    "value": boundary["value"],
                    "minimum_boundary": boundary["minimum"],
                    "maximum_boundary": boundary["maximum"],
                    "minimum_verification_results": check_min_boundary(
                        boundary["value"],
                        boundary["minimum"]
                    ),
                    "maximum_verification_results": check_max_boundary(
                        boundary["value"],
                        boundary["maximum"]
                    ),
                }
            )

        if len(results) == 0:
            warnings.warn("Warning no test have been executed against the benchmark")
            return None

        elif False in results:
            return False

        else:
            return True

    def compare_benchmark(self, minimum_letter_rank: str, minimum_score: float) -> dict:
        """

        :return:
        """
        self.rank = self.distance_statistics.rank
        self.score = self.distance_statistics.score
        return {
            "rank": check_letter_rank_boundary(minimum_letter_rank, self.rank),
            "score": check_min_boundary(self.score, minimum_score)
        }

    def run(self, method, arguments=None, iteration=1, pacing=0, processes=0):
        """

        :param method:
        :param arguments:
        :param iteration:
        :param pacing:
        :param processes:
        :return:
        """
        if __name__ == "__main__" and processes > 0:
            for _ in range(0, processes):
                Process(
                    name=f"worker-{_}",
                    target=self._execute_code_under_test,
                    kwargs={
                        "method": method,
                        "arguments": arguments,
                        "iteration": iteration,
                        "pacing": pacing
                    }
                ).start()

        else:
            self._execute_code_under_test(
                method,
                arguments,
                iteration,
                pacing,
            )
