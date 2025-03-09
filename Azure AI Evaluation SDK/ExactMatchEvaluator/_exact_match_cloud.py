import os
from promptflow._utils.async_utils import async_run_allowing_running_loop


class _AsyncExactMatchEvaluator:
    def __init__(self):
        pass

    async def __call__(self, *, ground_truth: str, response: str, **kwargs):
        score = 1.0 if ground_truth == response else 0.0

        return {
            "exact_match_score": score,
        }

class ExactMatchEvaluator:
    """
    Evaluates whether the response exactly matches the ground truth.

    This evaluator returns a score of 1.0 if the response is identical to the ground truth,
    and 0.0 otherwise. It is useful for tasks that require strict correctness such as factual QA.

    Example:
        evaluator = ExactMatchEvaluator()
        result = evaluator(ground_truth="Hello, world!", response="Hello, world!")
        print(result)  # {'exact_match_score': 1.0}
    """

    id = "update with your azure ml asset id"
    """Evaluator identifier, experimental and to be used only with evaluation in cloud."""

    def __init__(self):
        self._async_evaluator = _AsyncExactMatchEvaluator()

    def __call__(self, *, ground_truth: str, response: str, **kwargs):
        """
        Evaluate the exact match score between the response and the ground truth.

        :keyword response: The response to be evaluated.
        :paramtype response: str
        :keyword ground_truth: The ground truth to be compared against.
        :paramtype ground_truth: str
        :return: The exact match score.
        :rtype: dict
        """
        return async_run_allowing_running_loop(
            self._async_evaluator, ground_truth=ground_truth, response=response, **kwargs
        )

    def _to_async(self):
        return self._async_evaluator
