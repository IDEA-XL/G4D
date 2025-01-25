
# 💡 Guide for Defense (G4D): Dynamic Guidance for Robust and Balanced Defense in Large Language Models


[Weidi Luo†](https://eddyluo1232.github.io/), [Cao He†](https://github.com/CiaoHe), [Yu Wang](https://rain305f.github.io/), [Zijing Liu](https://github.com/zj-liu), [Bin Feng](https://xiaocw11.github.io/), [Yao Yuan](https://yao-lab.github.io/), [Yu Li](https://yu-li.github.io/)

（†:means equal contribution）

[**😀 Arxiv**](https://arxiv.org/abs/2410.17922)

##  🛠️ Requirements and Installation
### Create environment
```python
conda create -n G4D python=3.9
conda activate G4D
pip install -r requirements.txt
```

### Conduct Inference with G4D
```python
#You can find the setting of OpenAI's API or your configured model in prompt_tools.py
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
| Date       | Event    |
|------------|----------|
| **2025/01/22** | 🔥 Congratulations! Our paper is accepted by NAACL 2025 Findings.|
| **2024/10/24** | 🔥 We have released our paper on Arxiv.|
| **2024/10/24** | 🔥 We have released our code on GitHub.|

## 💡 Abstract
With the extensive deployment of Large Language Models (LLMs), ensuring their safety has become increasingly critical. However,existing defense methods often struggle with two key issues: (i) inadequate defense capabilities, particularly in domain-specific scenarios like chemistry, where a lack of specialized knowledge can lead to the generation of harmful responses to malicious queries. (ii) over-
defensiveness, which compromises the general utility and responsiveness of LLMs. To mitigate these issues, we introduce a multi-agents-
based defense framework, Guide for Defense (G4D), which leverages accurate external information to provide an unbiased summary
of user intentions and analytically grounded safety response guidance. Extensive experiments on popular jailbreak attacks and benign datasets show that our G4D can enhance LLM’s robustness against jailbreak attacks on general and domain-specific scenarios without compromising the model’s general functionality.

## ⚡ Framework
An ideal LLM defense system should balance robust security measures with seamless usability, ensuring protection against threats without hindering AI systems’ functionality and user experience. It must accurately identify and analyze malicious intent in queries while offering domain-specific protective guidance. Our defense framework employs an inference-stage mechanism comprising an intent detector, a question paraphraser, and a safety analyzer to produce safety instructions for the victim model,shown as below.
<center style="color:#C0C0C0"> 
    <img src="assets/teaser.png" width="700"/>

## 👻 Dataset Construction
### Chemistry&Biology-Redteam(CB-RedTeam)
According to the Laboratory Chemical Safety Summary (LCSS) (PubChem, 2024) on PubChem and NFPA 704 (Wikipedia contributors, 2024),
We curated a collection of 150 objects across the categories of Bacterial Agents, Biological Toxins, Drugs, Environmental Hazards, Explosive, Radioactive, and Toxic to construct the CB-RedTeam dataset. Except for objects under the Biological Toxins and Bacterial Agent categories, which only have technical names, all other categories include SMILES representations. 

### Chemistry&Biology-Benign (CB-Benign)
According to the Laboratory Chemical Safety Summary (LCSS) (PubChem, 2024) on PubChem and NFPA 704 (Wikipedia contributors, 2024), We selected the chemical formulas and SMILES representations of 60 common, harmless substances usually in daily life to construct the CB-Benign dataset.

## 📑 Citation
```python
@misc{cao2024guidedefenseg4ddynamic,
      title={Guide for Defense (G4D): Dynamic Guidance for Robust and Balanced Defense in Large Language Models}, 
      author={He Cao and Weidi Luo and Yu Wang and Zijing Liu and Bing Feng and Yuan Yao and Yu Li},
      year={2024},
      eprint={2410.17922},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2410.17922}, 
}

```
