#SinaTools

Open Source Toolkit for Arabic Natural Language Processing and Understanding

SinaTools is a Python-based toolkit designed to facilitate Arabic NLP and NLU. It encompasses various modules tailored to address key tasks, including Named Entity Recognition (NER), Word Sense Disambiguation (WSD), Semantic Relatedness, Synonymy Extraction and Evaluation, Lemmatization, Part-of-speech (POS) Tagging, Root Tagging, and additional helper utilities such as corpus processing, stripping methods, and Diacritic-Based Matching of Arabic Words.

SinaTools leverages state-of-the-art models and datasets to enhance the accuracy and efficiency of NLP and NLU tasks in Arabic. Benchmarking results demonstrate that SinaTools outperforms related tools in both accuracy and speed. For instance, the NER module is fine-tuned using the Wojood dataset and a BERT model, supporting flat, nested, and fine-grained entity types. The Semantic Relatedness module utilizes cosine similarity to evaluate the association between sentence pairs, surpassing baselines in the SemEval-2024 Task. Additionally, the Synonyms Module employs a sophisticated algorithm to extract synonyms from multilingual dictionaries and thesauri, enhancing the toolkit's capabilities in semantic analysis.

SinaTools aims to democratize Arabic NLU by providing accessible and efficient solutions for a wide range of tasks, catering to both experts and non-experts in the field. Its open-source nature and comprehensive documentation further contribute to its usability and adoption within the Arabic NLP community.

Installation
Stable Release
To install SinaTools, ensure you are using Python version 3.10.8, then execute the following command:

pip install SinaTools

From Sources
The sources for SinaTools can be downloaded from the GitHub repository.

You can also clone the public repository:

git clone git://github.com/SinaLab/SinaTools
Installing Models and Data Files
Some modules in SinaTools (e.g., NER, WSD) require fine-tuned BERT models and data files. To install these models, please consult Data Download.

Documentation
For detailed information on utilizing SinaTools, please refer to the documentation.

Citation
If you use SinaTools in your research, please cite the following paper:

Tymaa Hammouda, Mustafa Jarrar, Mohammed Khalilia: SinaTools: Open Source Toolkit for Arabic Natural Language Understanding. In Proceedings of the 2024 AI in Computational Linguistics (ACLING 2024), Procedia Computer Science, Dubai. ELSEVIER.

License
SinaTools is available under the MIT License. See the LICENSE file for more information.

Reporting Issues
To report any issues or bugs, please get in touch with us at "ABC@gmail.com" or visit SinaTools Issues.
