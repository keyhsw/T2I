---
license: mit
tags:
- generated_from_trainer
model-index:
- name: prompt-extend
  results: []
---
[![Generic badge](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/daspartho/prompt-extend)

# Prompt Extend

Text generation model for generating suitable style cues given the main idea for a prompt.

It is a GPT-2 model trained on [dataset](https://huggingface.co/datasets/daspartho/stable-diffusion-prompts) of stable diffusion prompts.

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 128
- eval_batch_size: 256
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 5
- mixed_precision_training: Native AMP

### Training results

| Training Loss | Epoch | Step  | Validation Loss |
|:-------------:|:-----:|:-----:|:---------------:|
| 3.7436        | 1.0   | 12796 | 2.5429          |
| 2.3292        | 2.0   | 25592 | 2.0711          |
| 1.9439        | 3.0   | 38388 | 1.8447          |
| 1.7059        | 4.0   | 51184 | 1.7325          |
| 1.5775        | 5.0   | 63980 | 1.7110          |


### Framework versions

- Transformers 4.24.0
- Pytorch 1.13.0+cu117
- Datasets 2.7.1
- Tokenizers 0.13.2
