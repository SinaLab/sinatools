SinaTools
======================
Open Source Toolkit for Arabic Natural Language Processing and Understanding

SinaTools is a Python-based toolkit designed to facilitate Arabic NLP and NLU. It encompasses various modules tailored to address key tasks, including [Named Entity Recognition (NER)](https://www.jarrar.info/publications/JKG22.pdf), [Word Sense Disambiguation (WSD)](https://www.jarrar.info/publications/JMHK23.pdf), [Semantic Relatedness](https://www.jarrar.info/publications/MJK24.pdf), [Synonymy Extraction](https://www.jarrar.info/publications/MJK24.pdf) and Evaluation, [Lemmatization, Part-of-speech (POS) Tagging, Root Tagging](https://www.jarrar.info/publications/JAH24.pdf), and additional helper utilities such as corpus processing, stripping methods, and [Diacritic-Based Matching of Arabic Words](https://www.jarrar.info/publications/JZAA18.pdf).

SinaTools leverages state-of-the-art models and datasets to enhance the accuracy and efficiency of NLP and NLU tasks in Arabic. Benchmarking results demonstrate that SinaTools outperforms related tools in both accuracy and speed. For instance, the NER module is fine-tuned using the Wojood dataset and a BERT model, supporting flat, nested, and fine-grained entity types. The morphology module implements Alma's lemmatizer, POS tagger, and root tagger, which we built using the Qabas lexicographic database. The WSD is a pipeline of five models. Given a sentence as input, each word is tagged: Lemma, single-word sense, multi-word sense, and NER.  Given a sentence as input, each word is tagged with its: Lemma, single-word sense, multi-word sense, and NER, which we developed using our ArabGlossBERT and Salma datasets. The Semantic Relatedness module utilizes cosine similarity to evaluate the association between sentence pairs. The Synonyms Module employs a sophisticated algorithm to extract synonyms from multilingual dictionaries and thesauri, enhancing the toolkit's capabilities in semantic analysis.

SinaTools aims to democratize Arabic NLU by providing accessible and efficient solutions for a wide range of tasks, catering to both experts and non-experts in the field. Its open-source nature and comprehensive documentation further contribute to its usability and adoption within the Arabic NLP community.

Installation 
--------
To install SinaTools, ensure you are using Python version 3.10.8, then clone the [GitHub](git://github.com/SinaLab/SinaTools) repository or execute the following command:

pip install SinaTools


Installing Models and Data Files
--------
Some modules in SinaTools (e.g., NER, WSD, synonyms, morph) require some data files and fine-tuned BERT models to be downloaded. To download these models, please consult the [DataDownload](https://sina.birzeit.edu/sinatools/documentation/cli_tools/DataDownload/DataDownload.html).

Documentation
--------
For detailed information on utilizing SinaTools, please refer to the [documentation](https://sina.birzeit.edu/sinatools).

Citation
-------
Tymaa Hammouda, Mustafa Jarrar, Mohammed Khalilia: [SinaTools: Open Source Toolkit for Arabic Natural Language Understanding.](http://www.jarrar.info/publications/HJK24.pdf ). In Proceedings of the 2024 AI in Computational Linguistics (ACLing 2024), Procedia Computer Science, Dubai. ELSEVIER.

License
--------
SinaTools is available under the MIT License. See the [LICENSE](https://sina.birzeit.edu/sinatools/documentation/License.html) file for more information.

Reporting Issues
--------
To report any issues or bugs, please contact us at "sina.institute.bzu@gmail.com" or visit [SinaTools Issues](https://github.com/SinaLab/sinatools/issues).

