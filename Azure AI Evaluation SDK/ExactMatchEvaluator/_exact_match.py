import os
from typing_extensions import overload, override
from azure.ai.evaluation._evaluators._common import EvaluatorBase
from typing import Dict

class ExactMatchEvaluator(EvaluatorBase):
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

    @override
    def __init__(self):
        super().__init__()

    @override
    async def _do_eval(self, eval_input: Dict) -> Dict[str, float]:
        """Evaluate whether the response matches the ground truth exactly."""
        ground_truth = eval_input["ground_truth"].strip()
        response = eval_input["response"].strip()
        
        score = 1.0 if ground_truth == response else 0.0

        return {
            "exact_match_score": score,
        }

    @overload
    def __call__(self, *, ground_truth: str, response: str):
        """
        Evaluate whether the response matches the ground truth exactly.

        :keyword response: The response to be evaluated.
        :paramtype response: str
        :keyword ground_truth: The ground truth to be compared against.
        :paramtype ground_truth: str
        :return: The exact match score.
        :rtype: Dict[str, float]
        """

    @override
    def __call__(self, *args, **kwargs):
        """Evaluate whether the response matches the ground truth exactly."""
        return super().__call__(*args, **kwargs)
