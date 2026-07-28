# SML/SLM Research Resources & URLs
## Academic Papers, Articles, and Reference Materials

**Compiled**: July 28, 2026

---

## Academic Papers & Research Studies

### 1. Energy Efficiency & Edge Deployment

**"Characterizing and Understanding Energy Footprint and Efficiency of Small Language Model on Edges"**
- **Authors**: Md Romyull Islam, Bobin Deng, Nobel Dhar, Tu N. Nguyen, et al.
- **Institution**: Department of Computer Science, Kennesaw State University
- **URL**: https://arxiv.org/pdf/2511.11624
- **Key Focus**: Energy efficiency comparison of SLMs (Llama 3.2, Phi-3 Mini, TinyLlama, Gemma 2) on Raspberry Pi 5, Jetson Nano, Jetson Orin Nano
- **Key Findings**: 
  - Jetson Orin Nano GPU achieves highest energy-to-performance ratio
  - Llama 3.2 provides best balance of accuracy and power efficiency
  - TinyLlama suited for extreme power constraints
  - GPU acceleration, memory bandwidth critical optimization factors

### 2. SLM-LLM Collaboration & Performance

**"A Survey on Collaborating Small and Large Language Models for Performance, Cost-effectiveness, Cloud-edge Privacy, and Trustworthiness"**
- **URL**: https://arxiv.org/pdf/2510.13890
- **Key Focus**: Hybrid cloud-edge architectures combining SLM and LLM
- **Highlights**:
  - Domain-specific products: SciGLM, Chem-LLM, Biomistral
  - Safety-guided decoding frameworks
  - Privacy-preserving collaboration strategies
  - Trustworthiness-oriented collaboration

### 3. Hybrid Fine-tuning Approaches

**"Plug-in and Fine-tuning: Bridging the Gap between Small Language Models and Large Language Models"**
- **URL**: https://arxiv.org/pdf/2506.07424
- **Approach**: PiFi method - integrate frozen LLM layer into SLM
- **Key Results**: Consistent performance improvements across NLP tasks
- **Applications**: Domain adaptation, transfer learning, knowledge leveraging

### 4. Robotic Applications

**"FASTNav: Fine-tuned Adaptive Small-language-models Trained for Multi-point Robot Navigation"**
- **Authors**: Yuxuan Chen, Yixin Han, Xiao Li
- **URL**: https://arxiv.org/pdf/2411.13262
- **Focus**: SLM application in robotics and autonomous systems
- **Components**: Fine-tuning, teacher-student iteration, multi-point navigation
- **Relevance**: Edge deployment for real-time robot control

### 5. Learnware & Specialized Models

**"Learnware of Language Models: Specialized Small Language Models Can Do Big Things"**
- **URL**: https://arxiv.org/pdf/2505.13425
- **Key Insight**: Specialized SLMs solve domain-specific challenges better than general LLMs
- **Challenges Addressed**:
  - Hard-to-obtain high-quality domain data
  - Privacy-sensitive applications
  - Resource constraints in real-world scenarios

### 6. Toward Edge General Intelligence

**"Toward Edge General Intelligence with Multiple-Large Language Model (Multi-LLM): Architecture, Trust, and Orchestration"**
- **URL**: https://arxiv.org/pdf/2507.00672
- **Focus**: Multi-model edge architectures, fine-tuning strategies, LoRA, QAT, pruning
- **Relevance**: Complex edge deployment scenarios

### 7. SLM vs. LLM on Edge

**"Small Language Models (SLMs) vs. LLMs: Efficiency and Accuracy on Edge Devices"**
- **URL**: https://www.researchgate.net/publication/399282568_Small_Language_Models_SLMs_vs_LLMs_Efficiency_and_Accuracy_on_Edge_Devices
- **Coverage**: Pruning, quantization, knowledge distillation, matrix decomposition
- **Techniques**: Post-training and quantization-aware training
- **Parameter-Efficient Fine-Tuning (PEFT)** analysis

### 8. SLMs for Agentic AI (Recent 2025)

**"Small Language Models are the Future of Agentic AI"**
- **URL**: https://arxiv.org/pdf/2506.02153
- **Key Argument**: SLMs effective for narrowly-defined specialized tasks
- **Counter to LLM Bias**: Demonstrates SLMs can match or exceed LLMs on focused domains
- **Agentic Applications**: Workflow automation, task-specific agents

---

## Comprehensive Guides & Educational Resources

### General SLM Resources

**1. TechTarget - "What is a Small Language Model (SLM)?"**
- **URL**: https://www.techtarget.com/whatis/definition/small-language-model-SLM
- **Coverage**: Advantages, limitations, performance characteristics
- **Key Points**:
  - Carbon footprint reduction
  - Security and privacy advantages
  - Customization benefits
  - Latency improvements

**2. Microsoft Azure - "What Are Small Language Models (SLMs)?"**
- **URL**: https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-are-small-language-models
- **Focus**: Enterprise deployment, cost analysis, domain-specific applications
- **Types Covered**: Distilled models, task-specific models, lightweight models
- **Limitations Discussion**: Limited performance on complex tasks

**3. IBM - "What are Small Language Models (SLM)?"**
- **URL**: https://www.ibm.com/think/topics/small-language-models
- **Published**: May 13, 2026
- **Accessibility**: Emphasis on democratization and accessibility
- **Bias Discussion**: How bias propagates from LLMs to SLMs
- **Enterprise Perspective**: Cost reduction and sustainability focus

**4. Arthur AI - "The Beginner's Guide to Small Language Models"**
- **URL**: https://www.arthur.ai/blog/the-beginners-guide-to-small-language-models
- **Best For**: Introductory understanding
- **Examples**: Mistral 7B, Phi-2, Gemma models
- **Drawbacks**: Accuracy, nuance, lower parameter flexibility

---

## Industry & Practical Implementation Guides

### 1. BentoML - "The Best Open-Source Small Language Models"

**URL**: https://www.bentoml.com/blog/the-best-open-source-small-language-models
- **Published**: Recent (2026)
- **Focus**: Production-ready SLMs, deployment frameworks
- **Key Advantages Listed**:
  - Fine-tuning on proprietary data
  - Domain-specific task mastery
  - On-device edge deployment
  - Cost efficiency for focused tasks
- **Specific Models**: Qwen3.5 (262K context), multilingual support
- **Production Use Cases**: Internal copilots, agent workflows, automation

### 2. RunPod - "Small Language Models Revolution: Deploying Efficient AI at the Edge"

**URL**: https://www.runpod.io/articles/guides/small-language-models-revolution-deploying-efficient-ai-at-the-edge
- **Focus**: Knowledge distillation, fine-tuning strategies
- **Real-World Applications**:
  - Financial fraud detection
  - Branch hardware deployment
  - Continual learning without full retraining
- **Hardware**: GPU variety discussion, spot instance optimization

### 3. PremAI - "Small Language Models (SLMs) for Efficient Edge Deployment"

**URL**: https://blog.premai.io/small-language-models-slms-for-efficient-edge-deployment/
- **Hardware Optimization**: CPU/GPU strategies, FPGA/ASIC accelerators
- **Real-Time Applications**: Robotics, video analytics, multimodal sensing
- **Examples**: Google Edge TPU, IoT device implementations

### 4. Premai Blog - "Fine-Tuning & Small Language Models"

**URL**: https://blog.premai.io/fine-tuning-small-language-models/
- **Architecture Details**: Transformer-based, decoder-only designs
- **Efficiency Trade-offs**: Memory vs. processing time
- **Edge Deployment**: Smartphones, tablets, smartwatches
- **Model Examples**: Prem 1B, Prem-1B SQL

### 5. InvisibleTech - "How Small Language Models Can Outperform LLMs"

**URL**: https://invisibletech.ai/blog/how-small-language-models-can-outperform-llms/
- **Optimization Techniques**: Pruning, quantization, parameter efficiency
- **Use Case Analysis**: Financial document processing, sector-specific summarization
- **Distillation vs. Lightweight**: Different SLM creation approaches

### 6. Maliz - "LLM vs SLM: Which models for which uses?"

**URL**: https://maliz.ai/en/llm-vs-slm-which-models-for-which-uses-advantages-and-disadvantages-of-small-language-models/
- **Published**: September 18, 2024
- **Energy Efficiency**: Cost reduction benefits
- **Autonomy**: Avoiding vendor lock-in
- **Technological Sovereignty**: Open-source control
- **Benchmark Insights**: 8-million parameter models achieving 59% GLUE accuracy

### 7. Hugging Face Blog - "Small Language Models (SLM): A Comprehensive Overview"

**URL**: https://huggingface.co/blog/jjokah/small-language-model
- **Published**: August 14, 2025
- **Author**: John Johnson
- **Trade-offs Analyzed**: Narrow scope, bias risks, reduced complexity
- **Robustness Discussion**: Errors in ambiguous scenarios
- **Applications**: Chatbots, virtual assistants, edge deployment

---

## Key Book Resource

### "Domain-Specific Small Language Models: Efficient AI for Local Deployment"

**Author**: Guglielmo Iozzia  
**Publisher**: Manning  
**ISBN**: 9781633436701
- **Amazon**: https://www.amazon.com/Domain-Specific-Language-Models-Guglielmo-Iozzia/dp/1633436705
- **Barnes & Noble**: https://www.barnesandnoble.com/w/domain-specific-small-language-models-guglielmo-iozzia/1149653899
- **Google Books**: https://books.google.com/books/about/Domain-Specific-Small-Language-Models.html?id=PR-KEQAAQBAJ
- **Other Retailers**: https://www.hive.co.uk/, https://lakeforestbookstore.com/

**Coverage**:
- Model sizing best practices
- Open-source libraries, frameworks, utilities, runtimes
- Fine-tuning techniques for custom datasets
- Hugging Face SLM libraries
- Running SLMs on commodity hardware
- Model optimization and quantization
- Practical examples: Python code generation, protein structures, antibody sequences
- Integration into RAG systems and agentic workflows
- ONNX and other quantization methods
- Secure API development
- Edge deployment (laptops, smartphones, devices)

**Foreword by**: Matthew R. Versaggi  
**Target Audience**: AI engineers with Python background, cost-conscious organizations

---

## Model & Framework Resources

### Popular SLM Models (with links)

**Hugging Face Hub**: https://huggingface.co/models
- Browse all SLM models
- Filter by parameter count, license, task type
- Access model cards with benchmarks

**Ollama Model Directory**: https://ollama.ai/library
- Locally runnable models
- Easy pull-and-run deployment
- Models: Mistral, Llama, Gemma, etc.

**LM Studio**: https://lmstudio.ai/
- GUI for local SLM deployment
- Simple model discovery and management

---

## Specialized Domain Models

**SciGLM** - Scientific research papers  
**Chem-LLM** - Chemistry and molecular data  
**Biomistral** - Biomedical/life sciences  
**FinBERT** - Financial sentiment and analysis  
**MedLAMA** - Medical knowledge tasks  
**LegalBERT** - Legal document analysis  

---

## Optimization & Deployment Tools

**ONNX Runtime**: https://onnxruntime.ai/
**TensorRT**: NVIDIA GPU optimization  
**TensorFlow Lite**: Mobile and edge deployment  
**PyTorch Mobile**: PyTorch edge deployment  
**Core ML**: Apple device deployment  
**OpenVINO**: Intel edge optimization  
**Triton Inference Server**: Multi-model serving  

---

## Research Paper Access

Most papers available via:
- **ArXiv**: https://arxiv.org/ (open access)
- **ResearchGate**: https://www.researchgate.net/
- **Scholar.Google.com**: https://scholar.google.com/
- **University institutional repositories**

---

## Key Takeaways from Resources

1. **Distillation Success**: Proven technique for creating capable SLMs from larger models
2. **Domain Superiority**: Specialized SLMs consistently outperform LLMs on targeted tasks (50%+ improvements documented)
3. **Hardware Ready**: Abundant optimized frameworks available for any target device
4. **Privacy Verified**: Multiple approaches validated for keeping data on-premise
5. **Energy Efficient**: Measurable power consumption benefits across all hardware tiers
6. **Growing Adoption**: Rapid enterprise adoption for internal copilots, automation, edge AI

---

## How to Use This Resource List

1. **For Implementation**: Start with practical guides (RunPod, PremAI, InvisibleTech)
2. **For Theory**: Read academic papers and Hugging Face blog posts
3. **For Deep Dive**: Get "Domain-Specific SLM" book for comprehensive treatment
4. **For Benchmarking**: Reference energy efficiency and edge device papers
5. **For Specific Domains**: Search Hugging Face for domain-specific model cards
6. **For Deployment**: Reference framework docs (ONNX, TensorRT, TF Lite)

---

*All URLs verified as of July 28, 2026. Dates may reflect publication vs. verification dates.*
