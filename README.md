

<p align="center">
    <img src="assets/AdaShield_logo.jpg" width="300"/>
<p>
<h2 align="center"> <a href="">Guide for Defense (G4D): Dynamic Guidance for Robust and Balanced
Defense in Large Language Models</a></h2>
<h5 align="center"> If you like our project, please give us a star ⭐ on GitHub for latest update.  </h2>

<h5 align="center">

##  🛠️ Requirements and Installation
### Create environment
```python
conda create -n G4D python=3.9
conda activate G4D
pip install -r requirements.txt
```

### Conduct Inference
You can find the setting of OpenAI's API or your configured model in prompt_tools.py
```python
python main.py --dataset AutoDAN --mode G4D --model_name gpt-4o-mini
python main.py --dataset CB-Benign --mode G4D --model_name gpt-4o-mini
python main.py --dataset MT-bench --mode G4D --model_name gpt-4o-mini
python main.py --dataset Advbench --mode G4D --model_name gpt-4o-mini
python main.py --dataset MMLU-pro --mode G4D --model_name gpt-4o-mini
python main.py --dataset AutoDAN --mode G4D --model_name gpt-4o-mini
python main.py --dataset CB-RedTeam --mode G4D --model_name gpt-4o-mini
```

### Conduct evaluation
```python
python evaluate.py --dataset MMLU-pro --mode G4D --model_name gpt-4o-mini  
python evaluate.py --dataset CB-RedTeam --mode G4D --model_name gpt-4o-mini  
python evaluate.py --dataset CB-Benign --mode G4D --model_name gpt-4o-mini 
```


## 📰 News

## 💡 Abstract
With the extensive deployment of Large Language Models (LLMs), ensuring their safety has become increasingly critical. However,existing defense methods often struggle with two key issues: (i) inadequate defense capabilities, particularly in domain-specific scenarios like chemistry, where a lack of specialized knowledge can lead to the generation of harmful responses to malicious queries. (ii) over-
defensiveness, which compromises the general utility and responsiveness of LLMs. To mitigate these issues, we introduce a multi-agents-
based defense framework, Guide for Defense (G4D), which leverages accurate external information to provide an unbiased summary
of user intentions and analytically grounded safety response guidance. Extensive experiments on popular jailbreak attacks and benign datasets show that our G4D can enhance LLM’s robustness against jailbreak attacks on general and domain-specific scenarios without compromising the model’s general functionality.

## ⚡ Framework
An ideal LLM defense system should balance robust security measures with seamless usability, ensuring protection against threats without hindering AI systems’ functionality and user experience. It must accurately identify and analyze malicious intent in queries while offering domain-specific protective guidance. Our defense framework employs an inference-stage mechanism comprising an intent detector, a question paraphraser, and a safety analyzer to produce safety instructions for the victim model,shown as below.
<center style="color:#C0C0C0"> 
    <img src="assets/teaser.png" width="700"/>

## 📑 Citation
