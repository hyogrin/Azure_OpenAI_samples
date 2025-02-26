# Azure_OpenAI_samples
## Azure AI Evaluation SDK Code Sample<br>
- This hands-on workshop is tailored for engineers seeking to deepen their understanding of the Azure AI Evaluation SDK. Participants will explore the distinctions between evaluators and simulators through practical code examples. The workshop will guide you in assessing the quality and safety of your generative AI applications using industry-standard metrics. Leveraging Azure AI Evaluation SDK’s built-in evaluators, you will learn how to compare different versions of your applications and select the optimal solution to meet your specific requirements. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20AI%20Evaluation%20SDK/1_quality-evaluators.ipynb">Go to notebook</a>
    > 이 실습 워크샵은 Azure AI 평가 SDK를 이해하고자 하는 엔지니어를 위한 맞춤형 워크샵입니다. 참가자는 실제 코드 예제를 통해 Evaluator와 Simulator의 차이점을 살펴봅니다. 이 워크샵에서는 업계 표준 메트릭을 사용하여 생성 AI 애플리케이션의 품질과 안전성을 평가하는 방법을 안내합니다. Azure AI 평가 SDK의 기본 제공 평가기를 활용하여 다양한 버전의 애플리케이션을 비교하고 특정 요구 사항을 충족하는 최적의 솔루션을 선택하는 방법을 배웁니다. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20AI%20Evaluation%20SDK/1_quality-evaluators.ipynb">Go to notebook</a>

## Requirements
Before starting, you should meet the following requirements:
- [Access to Azure OpenAI Service](https://go.microsoft.com/fwlink/?linkid=2222006)
- [Azure AI Foundry getting started](https://int.ai.azure.com/explore/gettingstarted): Create a project

# Azure Evaluation SDK
To thoroughly assess the performance of your generative AI application when applied to a substantial dataset, you can evaluate a Generative AI application in your development environment with the Azure AI evaluation SDK. 


| Category                                | Evaluator class                                                                                                                           |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Performance and quality (AI-assisted)   | GroundednessEvaluator, GroundednessProEvaluator, RetrievalEvaluator, RelevanceEvaluator, CoherenceEvaluator, FluencyEvaluator, SimilarityEvaluator |
| Performance and quality (NLP)           | F1ScoreEvaluator, RougeScoreEvaluator, GleuScoreEvaluator, BleuScoreEvaluator, MeteorScoreEvaluator                                       |
| Risk and safety (AI-assisted)           | ViolenceEvaluator, SexualEvaluator, SelfHarmEvaluator, HateUnfairnessEvaluator, IndirectAttackEvaluator, ProtectedMaterialEvaluator        |
| Composite                               | QAEvaluator, ContentSafetyEvaluator                                                                                                       |

### Performance and Quality Evaluators

#### AI-assisted Evaluators:
GroundednessEvaluator: Assesses the accuracy of responses based on provided context.
GroundednessProEvaluator: Similar to GroundednessEvaluator but uses Azure AI Content Safety.
RetrievalEvaluator: Evaluates the effectiveness of retrieval-augmented generation.
RelevanceEvaluator: Measures how relevant the response is to the query.
CoherenceEvaluator: Checks the logical flow and consistency of the response.
FluencyEvaluator: Evaluates the grammatical correctness and naturalness of the response.
SimilarityEvaluator: Measures the similarity between generated responses and ground truth.

#### NLP Evaluators:
F1ScoreEvaluator: Calculates the F1 score for precision and recall.
RougeScoreEvaluator: Measures overlap with reference texts using ROUGE metrics.
GleuScoreEvaluator: Evaluates using GLEU score.
BleuScoreEvaluator: Uses BLEU score for evaluating machine translations.
MeteorScoreEvaluator: Measures using METEOR score.


### Risk and Safety Evaluators
#### AI-assisted Evaluators:
ViolenceEvaluator: Detects violent content.
SexualEvaluator: Identifies sexually explicit content.
SelfHarmEvaluator: Detects content related to self-harm.
HateUnfairnessEvaluator: Identifies hate speech and unfair content.
IndirectAttackEvaluator: Evaluates vulnerability to indirect attack jailbreaks.
ProtectedMaterialEvaluator: Detects protected material.

#### Composite Evaluators:
QAEvaluator: Combines multiple quality evaluators for comprehensive assessment.
ContentSafetyEvaluator: Combines multiple safety evaluators for overall safety assessment.


## 🥇Other Resources

- Azure AI evaluation samples - https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/evaluate



## Author
Date of creation: 15-Jan-2025<br>
Updated: 15-Jan-2025<br>
<br>
Hyo Choi | hyo.choi@microsoft.com | https://www.linkedin.com/in/hyogrin/ 
