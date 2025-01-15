# Azure_OpenAI_samples

## 🔥New Feature (15-Jan-2025)
### Azure AI Evaluation SDK Code Sample<br>
- This hands-on workshop is tailored for engineers seeking to deepen their understanding of the Azure AI Evaluation SDK. Participants will explore the distinctions between evaluators and simulators through practical code examples. The workshop will guide you in assessing the quality and safety of your generative AI applications using industry-standard metrics. Leveraging Azure AI Evaluation SDK’s built-in evaluators, you will learn how to compare different versions of your applications and select the optimal solution to meet your specific requirements. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20AI%20Evaluation%20SDK/1_quality-evaluators.ipynb">Go to notebook</a>
    > 이 실습 워크샵은 Azure AI 평가 SDK를 이해하고자 하는 엔지니어를 위한 맞춤형 워크샵입니다. 참가자는 실제 코드 예제를 통해 Evaluator와 Simulator의 차이점을 살펴봅니다. 이 워크샵에서는 업계 표준 메트릭을 사용하여 생성 AI 애플리케이션의 품질과 안전성을 평가하는 방법을 안내합니다. Azure AI 평가 SDK의 기본 제공 평가기를 활용하여 다양한 버전의 애플리케이션을 비교하고 특정 요구 사항을 충족하는 최적의 솔루션을 선택하는 방법을 배웁니다. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20AI%20Evaluation%20SDK/1_quality-evaluators.ipynb">Go to notebook</a>

### o1 GA new features Test <br>
- Test the most basic way to use the o1(GA) with Vision model, Structured Output and gradio sample application as your playgournd <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/O1%20MultiModal/1_o1-ga-multi-modal.ipynb">Go to notebook</a>
    > 비전 모델, 구조화된 출력 및 그라디오 샘플 애플리케이션을 플레이그라운드로 사용하여 o1(GA)를 사용하는 가장 기본적인 방법을 테스트해 보세요. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/O1%20MultiModal/1_o1-ga-multi-modal.ipynb">Go to notebook</a>


## 🔥New Feature (23-Dec-2024)
### Azure Custom Speech <br>
- Added Audio Data Augmentation using [Audiomentations](https://github.com/iver56/audiomentations). Audiomentations supports both mono and stereo audio and integrates seamlessly with common audio processing workflows. It's lightweight, efficient, and helps simulate real-world audio conditions for better generalization in models.

Please do not forget to install the audiomentations package. Install with `pip install audiomentations` or see `requirements.txt`.

## 🔥New Feature (05-Dec-2024)
### Azure Custom Speech for multi-language<br>
- Refactored to make it easier to test custom models for a given language by adding language-specific settings. Added a function to the 3_evaluate_custom_model notebook to retrieve detailed WER information from the notebook based on whether there are insertions, substitutions, or deletions.  <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20Custom%20Speech/3_evaluate_custom_model.ipynb">Go to notebook</a>
    > 언어별 설정을 추가하면 간단히 해당 언어에 맞는 커스텀 모델을 테스트해볼 수 있도록 리펙토링했습니다. insertion, substitution, deletion 여부에 따라 상세한 WER정보를 노트북에서 조회하는 함수를 3_evaluate_custom_model 노트북에 추가했습니다. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20Custom%20Speech/3_evaluate_custom_model.ipynb">Go to notebook</a>

## 🔥New content (11-Nov-2024)
### Azure Custom Speech E2E Training with Python<br>
- Azure AI Speech is a managed service that provides speech capabilities such as speech-to-text, text-to-speech, voice translation, and speaker recognition. In this lab, you will learn the entire end-to-end process of training a custom speech-to-text (STT) model optimised for a specific language and use case based on synthetic data. You can practice generating synthetic text data (phi3.5), converting generated text files to audio files (text-to-speech), training(speech-to-text), evaluating, and deploying custom AI speech models based on synthetic text/audio files. In addition to generating synthetic data, you can also upload the speech data you use in the field to a specific folder and upload it to the storage account with simple notebook code to proceed with dataset creation, training, and evaluation.  If you're looking to train custom speech models with different types of datasets to improve your word error rate (WER), this Python SDK and REST API-based handson makes it easy to automate your end-to-end model training and evaluation pipeline and scale your transformations.  
<a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20Custom%20Speech/0_text_data_generation.ipynb">Go to notebook</a>
    > Azure AI Speech는 음성 텍스트 변환, 텍스트 음성 변환, 음성 번역, 화자 인식과 같은 음성 기능을 제공하는 관리형 서비스입니다. 본 핸즈온에서는 특정 언어와 유스케이스에 최적화된 Custom STT(Speech To Text)모델 학습의 End2End 전체과정을 합성데이터(Syntethic data)기반으로 실습합니다. 합성 텍스트 데이터 생성(phi3.5), 생성된 텍스트파일을 오디오파일로 변환 (Text to Speech), 합성 텍스트/오디오파일 기반의 Custom AI Speech 모델 학습(Speech to Text), 평가, 배포를 Python SDK와 REST API기반으로 실습해볼 수 있습니다. 합성데이터를 생성하는 것 외에도 현장에서 활용하고 있는 음성데이터를 특정 폴더에 업로드하면 간단한 노트북 코드로 Storage Account에 업로드 및 데이터셋 생성, 학습 및 평가 과정을 진행해볼 수도 있습니다. WER(단어 오류율)을 개선하기 위해 다양한 유형의 데이터셋으로 맞춤형 음성 모델을 학습시키려는 경우, Python SDK 및 REST API기반의 본 핸즈온을 활용하여 엔드투엔드 모델 학습 및 평가 파이프라인을 쉽게 자동화하고 변형을 확장할 수 있습니다. 
 <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Azure%20Custom%20Speech/0_text_data_generation.ipynb">Go to notebook</a>

## 🔥New content (30-Oct-2024)
### Promptflow with Python SDK<br>
- This hands-on workshop is designed to help engineers who have difficulty developing UI-based Promptflow in Azure ML Studio, AI Studio, and VS Code. Based on the Python Promptflow SDK, you will learn how to develop and run chat, flows with context, phi3 model integration deployed serverlessly, evaluation flows, and filter inappropriate prompts using content safety. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Promptflow%20with%20Python%20SDK/1_promptflow_with_code.ipynb">Go to notebook</a>
    > 이 핸즈온 워크샵은 Azure ML Studio, AI Studio, VS Code에서 Promptflow를 ui기반으로 개발하는데 어려움을 느끼는 엔지니어들을 지원하고자 개발되었습니다. Python Promptflow SDK를 기반으로 chat, context가 포함된 flow, serverless로 배포한 phi3모델 연동, evaluation flow 개발 및 실행 방법과 부적절한 prompt를 content safety을 활용해 filtering하는 실습을 담고 있습니다.  <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/Promptflow%20with%20Python%20SDK/1_promptflow_with_code.ipynb">Go to notebook</a>

## 🔥New content (15-Oct-2024)
### AI Search Code Sample with AOAI<br>
- Based on the current version of the Azure AI Search Python client library, azure-search-documents==11.6.0b4. This code sample demonstrates various code patterns to implement AI search using Azure OpenAI and Azure AI Search to create indexes, vector search, change search algorithms, cross-field search, multi-vector search, filtering, hybrid, and reranking. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/AI%20Search%20Code%20Sample%20with%20AOAI/AI%20Search%20Query%20Patterns.ipynb">Go to notebook</a>
    > 현재 Azure AI Search Python client library 최신 버전인 azure-search-documents==11.6.0b4를 바탕으로 작성되었습니다. 이 코드 샘플은 Azure OpenAI와 Azure AI Search를 사용하여 인덱스 생성, vector search, 검색 알고리즘 변경, Cross-Field검색, Multi-Vector검색, filtering, Hybrid, Reranking을 활용한 AI 검색을 구현하는 다양한 코드 패턴을 보여줍니다. <a href="https://github.com/hyogrin/Azure_OpenAI_samples/blob/main/AI%20Search%20Code%20Sample%20with%20AOAI/AI%20Search%20Query%20Patterns.ipynb">Go to notebook</a>

## 🥇Other Resources

### Azure OpenAI pricing
- https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/

### Diagam of a search scoring workflow
- https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking#diagram-of-a-search-scoring-workflow 



## Author
Date of creation: 15-Oct-2024<br>
Updated: 11-Nov-2024<br>
<br>
Hyo Choi | hyo.choi@microsoft.com | https://www.linkedin.com/in/hyogrin/ 