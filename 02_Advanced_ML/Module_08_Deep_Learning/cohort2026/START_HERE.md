# Module 8 — Neural networks and deep learning, session plan

Everything is in this folder. The two image datasets (clothing, ~110 MB; curly/straight hair, ~100 MB) are already downloaded and unpacked. Pre-trained Xception weights (~90 MB) download themselves the first time the lecture code runs.

**Homework 8:** platform deadline **Mon 30 Nov**. Lessons Nov 11–16, then peer reviews and Austria; HW8 is the first session back.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw08

The lecture is **TensorFlow/Keras**; the 2026 homework is **PyTorch**. Same ideas (CNN, logits, loss, optimizer, augmentation), different API. The bridge is the PyTorch workshop in [notebooks/pytorch/README.md](notebooks/pytorch/README.md) and the Keras → PyTorch table at the end of `practice/08-deep-learning_commented.ipynb`.

---

## Sessions

**Session 1 — Tue 10 Nov, 08:00. Setup.**
1. PyTorch for HW8 (required). A separate env, so the pinned NumPy doesn't touch `ml-zoomcamp`:
   ```bash
   conda create -n mlzc-torch python=3.11 -y && conda activate mlzc-torch
   pip install torch==2.9.0 torchvision==0.24.0 numpy==2.3.3 Pillow==11.3.0 jupyter matplotlib
   python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)"
   ```
   Not `pip install -r homework/requirements-cpu.txt` on the Mac: see trap 1. Background: [install_pytorch.md](notebooks/pytorch/install_pytorch.md) (written for Linux/NVIDIA; on the Mac only the CPU path applies).
2. TensorFlow, only if you want to run the lecture locally: `conda create -n mlzc-tf python=3.11 -y && conda activate mlzc-tf && pip install tensorflow jupyter matplotlib`. Plain `tensorflow` runs natively on Apple Silicon; skip `tensorflow-metal`. [15-install.md](lessons/15-install.md) is a WSL2/CUDA guide; its last section (free Kaggle/Colab T4 GPU) is the useful part for full-length runs.
3. AWS for Module 9: create the account, turn on MFA for the root user, and in Billing → Budgets create a monthly cost budget (e.g. $5) with an e-mail alert.

**Session 2 — Wed 11 Nov, 08:00.** Read [8.1](lessons/01-fashion-classification.md) → [8.2](lessons/02-tensorflow-keras.md) (~1,770 words). The clothing dataset, TensorFlow vs Keras, an image as a NumPy array. In `practice/`: load and resize one image.

**Session 3 — Wed 11 Nov, 20:00 (long hour).** Read [8.3](lessons/03-pretrained-models.md) → [8.4](lessons/04-conv-neural-nets.md) (~3,910 words). Run pre-trained Xception on one image, `preprocess_input`, `decode_predictions`; then filters, feature maps, dense layers.

**Session 4 — Thu 12 Nov, 08:00.** Read [8.5](lessons/05-transfer-learning.md) (~3,010 words). `ImageDataGenerator`, frozen base + new head, logits and `from_logits=True`, first `fit` (2–3 epochs).

**Session 5 — Fri 13 Nov, 08:00.** Read [8.6](lessons/06-learning-rate.md) → [8.8](lessons/08-more-layers.md) (~3,800 words). The `make_model` factory, learning-rate sweep, `ModelCheckpoint`, an inner dense layer.

**Session 6 — Mon 16 Nov, 08:00.** **The midterm closes tonight: confirm the submission first.** Then read [8.9](lessons/09-dropout.md) → [8.14](lessons/14-explore-more.md) (~4,130 words). Dropout, augmentation (training set only), the 299×299 model, load the best checkpoint and predict.

Nov 17–18: midterm peer reviews. Nov 19–25: Viaggio Austria, no study.

**Session 7 — Thu 26 Nov, 08:00.** HW8 **Q1–Q6** in `homework/Homework8_2026.ipynb`: setup, Q1–Q2, the training loop, baseline run (Q3–Q4), augmented run (Q5–Q6). **Submit** (closes Mon 30 Nov).

> Full-length lecture runs (10–50 epochs, ~15 models) take hours on a laptop CPU. `QUICK_RUN = True` in the commented notebook caps every run at 3 epochs; use Kaggle/Colab for the real numbers.
> Checkpoints are ~85 MB each and the two image folders ~210 MB together: keep `*.keras`, `*.h5`, `notebooks/clothing-dataset-small/`, `homework/data/` and `homework/runs/` out of git.
> If the week collapses: homework isn't required for the certificate. Skip HW8 rather than let it push Module 9.

---

## Six traps in this homework

**1. `requirements-cpu.txt` doesn't install on a Mac.** It pins `torch==2.9.0+cpu` from the PyTorch CPU index: those `+cpu` wheels exist only for Linux and Windows. On macOS install the plain `torch==2.9.0 torchvision==0.24.0` (the Mac wheels are CPU builds already), plus `numpy==2.3.3 Pillow==11.3.0`, as in Session 1.

**2. Report the CPU run.** Keep `device = torch.device("cpu")` and `num_workers=0`. Don't switch to `mps` (Apple GPU) for the numbers you submit: the grading baseline is the CPU reference. Restart the kernel and run top to bottom before reading off Q3–Q6, or the seed doesn't reproduce the run. 20 epochs take ~10 min on a laptop CPU.

**3. Labels need `labels.float().unsqueeze(1)`.** `ImageFolder` gives a `long` tensor of shape `(20,)`; the model returns `(20, 1)` floats. `BCEWithLogitsLoss` stops with *"Target size ... must be the same as input size"* otherwise. And no sigmoid inside the model: it returns logits, `torch.sigmoid` only for accuracy.

**4. Average per example, not per batch.** 201 evaluation images = 10 batches of 20 plus one batch of **1**. Averaging batch means gives that single image the weight of 20 (on the reference run it moved Q5 by 0.003 and Q6 by 0.006). Sum `loss.item() * images.size(0)`, divide by the number of images.

**5. Q4 is the *population* std.** `np.std(values, ddof=0)`. `pd.Series(values).std()` and `statistics.stdev` use `ddof=1` and give a different number (0.147 vs 0.139 on the reference run).

**6. The augmented phase continues the same model.** Don't re-run the model or optimizer cell: 10 more epochs on the trained model, and only those 10 go into `history_augmented.json`. Its training loader gets its own generator seeded `SEED + 1`, as in `reference_train.py` (pre-filled in the scaffold). Q3–Q6 are free numbers with a tolerance: run `reference_train.py --data-dir data` afterwards as the cross-check.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-fashion-classification.md](lessons/01-fashion-classification.md) | 8.1 Fashion classification | 792 | [video](https://www.youtube.com/watch?v=it1Lu7NmMpw&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-tensorflow-keras.md](lessons/02-tensorflow-keras.md) | 8.2 TensorFlow and Keras | 979 | [video](https://www.youtube.com/watch?v=R6o_CUmoN9Q&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-pretrained-models.md](lessons/03-pretrained-models.md) | 8.3 Pre-trained convolutional neural networks | 1,426 | [video](https://www.youtube.com/watch?v=qGDXEz-cr6M&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-conv-neural-nets.md](lessons/04-conv-neural-nets.md) | 8.4 Convolutional neural networks | 2,480 | [video](https://www.youtube.com/watch?v=BN-fnYzbdc8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-transfer-learning.md](lessons/05-transfer-learning.md) | 8.5 Transfer learning | 3,012 | [video](https://www.youtube.com/watch?v=WKHylqfNmq4&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-learning-rate.md](lessons/06-learning-rate.md) | 8.6 Adjusting the learning rate | 1,592 | [video](https://www.youtube.com/watch?v=2gPmRRGz0Hc&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-checkpointing.md](lessons/07-checkpointing.md) | 8.7 Checkpointing | 1,210 | [video](https://www.youtube.com/watch?v=NRpGUx0o3Ps&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-more-layers.md](lessons/08-more-layers.md) | 8.8 Adding more layers | 994 | [video](https://www.youtube.com/watch?v=bSRRrorvAZs&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [09-dropout.md](lessons/09-dropout.md) | 8.9 Regularization and dropout | 1,210 | [video](https://www.youtube.com/watch?v=74YmhVM6FTM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [10-augmentation.md](lessons/10-augmentation.md) | 8.10 Data augmentation | 865 | [video](https://www.youtube.com/watch?v=aoPfVsS3BDE&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [11-large-model.md](lessons/11-large-model.md) | 8.11 Training a larger model | 872 | [video](https://www.youtube.com/watch?v=_QpDGJwFjYA&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [12-using-model.md](lessons/12-using-model.md) | 8.12 Using the model | 775 | [video](https://www.youtube.com/watch?v=cM1WHKae1wo&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [13-summary.md](lessons/13-summary.md) | 8.13 Summary | 316 | [video](https://www.youtube.com/watch?v=mn0BcXJlRFM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [14-explore-more.md](lessons/14-explore-more.md) | 8.14 Explore more | 91 | — |
| [15-install.md](lessons/15-install.md) | 8.15 Installation of TensorFlow | 832 | — |

~17,446 words ≈ 73 min of reading. Alexey's lecture notebook is in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                         ← this file
├── lessons/                              ← 15 written lessons + images/
├── notebooks/
│   ├── 08-deep-learning-lecture.ipynb    ← Alexey's Keras lecture, untouched
│   ├── clothing-dataset-small/           ← train / validation / test, 10 classes (3,781 images)
│   └── pytorch/                          ← the PyTorch workshop README + install_pytorch.md, verbatim
├── practice/                             ← your practice notebook + the commented walkthrough (reads ../notebooks/clothing-dataset-small)
└── homework/
    ├── Homework8_2026.ipynb              ← scaffold: setup, Q1–Q6, no answers
    ├── homework8_2026.md                 ← the official question text
    ├── data/                             ← train/ (800 + 1 GIF) and test/ (201): curly, straight
    ├── reference_train.py                ← the official reference run (cross-check only)
    ├── requirements-cpu.txt              ← the official pins (Linux/Windows syntax, see trap 1)
    └── dataset_manifest.json             ← archive checksum and image counts
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)
