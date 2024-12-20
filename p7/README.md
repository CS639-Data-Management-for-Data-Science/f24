# P7 (12% of grade): Learning about LLMs

Github Classroom Link: https://classroom.github.com/a/Y6ZRDyjN

## :telescope: Overview

This project introduces you to working with LLMs using the HuggingFace API, fine-tuning them on specific data, and visualizing results using Streamlit. You'll complete the assignment in a Google Colab or Kaggle notebook.

Learning objectives:
- Gain hands-on experience with pre-trained LLMs, including text generation, prompt engineering, and 4-bit quantization.
- Fine-tune LLMs using LoRA on domain-specific datasets, tracking and evaluating performance improvements.
- Build and deploy interactive apps with Streamlit.

Before starting, please review the [general project directions](../projects.md).

:warning: Please use Piazza to post (public/private) any questions regarding this project, as e-mails will NOT be answered. If you need to include your code to get help, please make a **private** post.

## :pushpin: Corrections/Clarifications

1. [**Dec 2, 2024**] Added a clarification on submission requirements for those working in a *team*. See [Submission](#outbox_tray-submission) for details.
2. [**Dec 5, 2024**] Added a clarification in case your request for `Llama-3.2-1B-Instruct` HF access is **denied**. See section "[Apply for Llama-3.2-1B-Instruct Acccess on HuggingFace](#step-3-apply-for-llama-32-1b-instruct-acccess-on-huggingface)" for details; and [`Q1.1`](#q11-load-a-4-bit-quantized-llama-32-1b-instruct-model-and-and-its-tokenizer) for an additonal requirement asking you to include a markdown cell with the name and link to the model you used (again, this is only if you are not using `Llama-3.2-1B-Instruct`).
3. [**Dec 6 2024**] Added a note on how to bypass the wandb prompt thrown by `SFTTrainer` during fine-tuning. See last bullet point in [`Q2.2` "Steps to follow"](#q22-fine-tune-the-model-on-course-lecture-transcripts-with-lora) for details. You can ignore this if you like.
4. [**Dec 9 2024**] Added a clarification on what to do in case you see that HF `SFTTrainer` is skipping some epochs during fine-tuning (TLDR: don't worry about it / ignore it / just report whatever many epochs you have). See [`Q2.2` "Steps to follow"](#q22-fine-tune-the-model-on-course-lecture-transcripts-with-lora) for details.

## :hammer_and_wrench: Section 0: Setup

### Step 1: Google Colab or Kaggle

This project **requires** the use of a GPU, and both Google Colab and Kaggle provide free access to GPUs (e.g., NVIDIA Tesla T4). However, GPU resources are **not** guaranteed on Google Colab (it's based on availability). So feel free to use Google Colab if you manage to secure resources, otherwise please use Kaggle.


#### For Google Colab:
1. Sign-in to [Google Colab](https://colab.research.google.com) with your "wisc.edu" ID.
2. Create a new notebook and name it `p7.ipynb`.
3. To enable GPU:
    * In the upper-right of the Colab window, select ▾ (**Additional connection options**).
    * Select **Change runtime type**.
    * Under **Hardware accelerator**, select **T4 GPU**.
4. While you have free access to GPUs, there are usage limits you should be aware of:
    * Sessions may last up to 12 hours, but inactive sessions will be terminated sooner.
    * Resources (e.g., GPU availability) are **not** guaranteed and depend on demand.

#### For Kaggle:
1. Sign-in to [Kaggle]( https://www.kaggle.com/) with your "wisc.edu" ID.
2. On the tab-bar, select on **Code**, and create a new notebook and name it `p7.ipynb`.
3. To enable GPU: **Settings → Accelerator → GPU P100**
4. While you have free access to GPUs, there are usage limits you should be aware of:
    * You have maximum 30 hours/week of GPU access.

**Code to Verify GPU Availability**
```python
import torch
print("GPU available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
```

### Step 2: Setup a HuggingFace Account

You'll be accessing models via HuggingFace's `transformers` library, which requires setting up an account.

**Steps to Set Up**:
1. [HuggingFace](https://huggingface.co) and sign up for a free account.
2. After logging in, navigate to your profile and obtain an API token:
    * Go to your account settings → **Access Tokens**.
    * Click **New Token** and generate a token with the role "read".
3. Store the token securely; you’ll need it for authentication.

**Login in Colab/Kaggle**:
1. Authenticate your HuggingFace account in Colab or Kaggle by running the following code:
```python
from huggingface_hub import login
login()
```
This will prompt you to enter your HuggingFace API token.

### Step 3: Apply for `Llama-3.2-1B-Instruct` Acccess on HuggingFace.
1. Go to https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct. Fill-out and submit the provided form to gain access to the model weights.
    * You can review your request status (pending/accepted) here: https://huggingface.co/settings/gated-repos. It typically takes ~15 minutes.

**If your access request is denied**: Use any of the other fine-tuned variants of the same model family (preferably instruction-tuned). For e.g., one variant is an uncensored version, [`huihui-ai/Llama-3.2-1B-Instruct-abliterated`](https://huggingface.co/huihui-ai/Llama-3.2-1B-Instruct-abliterated).

### Step 4: Install Dependencies

1. Please install the required dependencies by running the following code:
```python
!pip install bitsandbytes>=0.39.0
!pip install --upgrade accelerate transformers datasets peft trl
!pip install streamlit
!npm install -g localtunnel
```

### Step 5: Download Dataset

1. The dataset of lecture transcripts (1.txt, 2.txt, etc.) is provided as a ZIP file. Download and extract the files into your Colab or Kaggle environment using `wget` and `unzip`.

```
!wget https://github.com/CS639-Data-Management-for-Data-Science/f24/raw/main/p7/transcripts.zip
!unzip transcripts.zip -d transcripts/
```

## :blue_book: Section 1: Text Generation with a Pre-Trained LLM

In this section, you will load and run inference (text generation) on a **4-bit quantized version** of [Llama-3.2-1B-Instruct](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/), using HuggingFace [`transformers`](https://huggingface.co/docs/transformers/en/index) and [`bitsandbytes`](https://huggingface.co/docs/transformers/main/en/quantization/bitsandbytes).

### Q1.1: Load a 4-bit quantized `Llama-3.2-1B-Instruct` model and and its tokenizer.

**Steps to follow**:
1. Import the required classes: `AutoTokenizer`, `AutoModelForCausalLM`, and `BitsAndBytesConfig`.
2. Set the model ID to `"meta-llama/Llama-3.2-1B-Instruct"`.
3. Define a configuration for 4-bit quantization using `BitsAndBytesConfig` with the following settings:
    * `load_in_4bit=True`
    * `bnb_4bit_quant_type="nf4"`
    * `bnb_4bit_compute_dtype=torch.float16`
4. Load the tokenizer using `AutoTokenizer.from_pretrained()`.
5. Load the quantized model using `AutoModelForCausalLM.from_pretrained()` with the quantization configuration, and ensure it is moved to the current device (e.g., GPU).
6. If your access request for `Llama-3.2-1B-Instruct` was denied and you used a different model, please include a markdown cell including the name and link to the model.

<details>
<summary>[<b>Optional reading</b>] How do we access pre-trained models from HuggingFace?</summary>

- HuggingFace `transfomers` provides several ways to load pre-trained models depending on the specific task you want to accomplish:
    - `pipeline()`:
        - Quickest way to load a pre-trained model *and* tokenizer for popular tasks like text generation, summarization, etc. It is the most user-friendly, but less customizable than other methods.
    - General [`AutoClasses`](https://huggingface.co/docs/transformers/en/model_doc/auto):
        - `AutoModel.from_pretrained()` and `AutoTokenizer.from_pretrained()` guess and automatically retrieve the relevant model given the name/path to the pretrained weights/vocabulary.
    - Task-Specific [`AutoClasses`](https://huggingface.co/docs/transformers/en/model_doc/auto):
        - `AutoModelForCausalLM`, `AutoModelForSequenceClassification`, etc. perform similarly as `AutoModel`, but retrive task-optimized models (for e.g., `AutoModelForCausalLM` will attach an additional head for casual language modeling).
    - Specific Models and Tokenizers:
        - HuggingFace also provides model and tokenizer classes tied to specific architectures/vocabularies. For e.g, [`LlamaModel.from_pretrained()`](https://huggingface.co/docs/transformers/main/en/model_doc/llama#transformers.LlamaModel), [`LlamaForCausalLM.from_pretrained()`](https://huggingface.co/docs/transformers/main/en/model_doc/llama#transformers.LlamaForCausalLM), [`LlamaTokenizer.from_pretrained()`](https://huggingface.co/docs/transformers/main/en/model_doc/llama#transformers.LlamaTokenizer), etc.
</details>

### Q1.2: Test your quantized model with different prompts (text generation).

Test your quantized `Llama-3.2-1B-Instruct` model by generating text responses to 2-3 different prompts. Ensure at least **one prompt** is related to **UW-Madison**.

**Steps to follow**:
1. Use the tokenizer's `.encode()` method to tokenize the model input (your prompt).
    * Refer to the [`.encode()` documentation](https://huggingface.co/docs/transformers/en/main_classes/tokenizer#transformers.PreTrainedTokenizer.encode).
2. Use the model's `.generate()` method to generate output.
    * Refer to the [`.generate()` documentation](https://huggingface.co/docs/transformers/en/main_classes/text_generation#transformers.GenerationConfig).
    * Feel free to play with the generation settings (e.g., `max_new_tokens=100`)
3. Use the tokenizer's `.decode()` method to convert model output into human-readable text.
    * Refer to the [`.decode()` documentation](https://huggingface.co/docs/transformers/en/main_classes/tokenizer#transformers.PreTrainedTokenizer.decode).
    * Set `skip_special_tokens=True` to remove special tokens from the output.
4. For each prompt, print both the **input prompt** and the **generated output text**.


### Q1.3: Identify a prompt where the model fails and analyze the failure.

- Find a prompt that your quantized `Llama-3.2-1B-Instruct` model fails to answer correctly.
    * Print both the **input prompt** and the **generated output text**.
-  In a markdown cell, write **1-2 reasons** why the model failed for the chosen prompt. Consider factors such as:
    * Lack of relevant training data.
    * Limitations in multi-step reasoning or contextual understanding.

### Q1.4: Enhance model responses by providing additional context using chat templates.

Explore how to improve your model's responses by providing additional context using the [chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating) to create a role-playing agent.

**Steps to follow**:
1. Use your tokenizer's `.apply_chat_template()` method to structure a role-playing prompt. For example (please try to come up with your **own** prompt):
    * Role as a teacher: "You are a knowledgeable science teacher explaining string theory to a 10-year-old."
    * Role as a poet: "You are a skilled poet writing a haiku about quantum computing."
    * Role as a pirate: "You are a pirate who uses 'blistering barnacles' in their conversations frequently, and are currently answering questions about sailing."
2. Pass the resulting formatted prompt to your model using `.generate()`.
3. Decode and print the output as done previously.
4. In a markdown cell, note whether the role-playing prompt got the model to successfully respond in the assumed role/character.

## :green_book: Section 2: Fine-Tuning a Pre-Trained LLM on Course Lecture Transcripts

In this section, you will fine-tune your quantized `Llama-3.2-1B-Instruct` model on the lecture transcripts of this course. The goal is to specialize the model to provide more accurate and context-specific answers related to the course material.

### Q2.1: Test the model before fine-tuning.

**Steps to Follow**:
1. Pick **any** course-specific prompt. For e.g., "Can you summarize the main topics and associated tools used?", "What NoSQL databases are covered in the course?", etc.
2. Use your tokenizer's `.apply_chat_template()` method to assign a specific role to your model:
    ```
    "You are an instructor of CS 639 Data Management for Data Science course at UW-Madison, and are currently answering student questions."
    ```
3. Print both the **input prompt** and the **generated output text**.


### Q2.2 Fine-tune the model on course lecture transcripts with LoRA.

**Steps to follow**:
1. Import the required classes:
    ```python
    from datasets import Dataset

    from peft import LoraConfig
    from transformers import TrainingArguments
    from trl import SFTTrainer
    ```
2. Load and process the dataset.
    * Split the dataset in train and test splits (e.g. 90% train and 10% test).
    * Convert the splits into a HuggingFace `Dataset` object.
3. Tokenize the train and test splits using your tokenizer.
4. Fine-tune the model using `SFTTrainer`. Ensure that both **training loss** and **validation loss** are printed for each epoch.
    * Use the following LoRA configurations (feel free to modify them if you'd like):
        ```python
        lora_config = LoraConfig(
            r=8,
            task_type="CAUSAL_LM",
            target_modules=[
                "q_proj", "o_proj", "k_proj", "v_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
        )
        ```
    * Use the following training arguments (feel free to modify them if you'd like, except `num_train_epochs`):
        ```python
        training_args = TrainingArguments(
            evaluation_strategy="epoch",
            save_strategy="epoch",
            num_train_epochs=10,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=1,
            logging_dir="./logs",
            output_dir="./results",
            save_total_limit=2,
            optim="paged_adamw_8bit"
        )
        ```
    [Optional] In case you would like to by-pass the wandb prompt thrown by `SFTTrainer`, add argument `report_to="none"` in `TrainingArguments`.
    * It is **OK if some of the epochs are auto-skipped by `SFTTrainer`** during fine-tuning. This is related to `gradient_accumulation_steps=4` setting.

### Q2.3: Test the model after fine-tuning.

- Evaluate your fine-tuned model’s performance on the same prompt used in `Q2.1`
    * Print both the **input prompt** and the **generated output text**. 
- In a mark-down cell, note if there is any improvmenents in quality, relevance, or accuracy of response.

## :closed_book: Section 3: Build a "Creative Writing Assistant" Using Streamlit

### Q3: Create the "Creative Writing Assistant" application.

Create an **interactive** "Creative Writing Assistant" app using Streamlit that leverages a pre-trained LLM (`Llama-3.2-1B-Instruct` or `gpt2`) to help users generate creative story ideas for any topic (e.g., "fantasy", "science fiction", etc.). Please take a **screenshot** of your application and save it as `q3.png`.

**Required functionality**:
- The application should allow users to type in any genre/topic (e.g. "fantasy", "science fiction", etc.), and generate story ideas from them.
- The application should leverage either `Llama-3.2-1B-Instruct` (quantized) or `gpt2`.
    * [Optional] Allow users to interactively switch between `Llama-3.2-1B-Instruct` or `gpt2` using a dropdown menu.
- Allow users to interactively adjust **at least** 2 model generation parameters, such as:
    * `Temperature`: Controls creativity/randomness.
    * `Max Length`: Specifies the maximum number of tokens in the output.
    * `Repetition Penalty`: Penalizes repetitive text generation.
    * `Top P`: Controls the cumulative probability for token sampling.
    * etc.

**Tips**:
- Before you begin this section, reset all variables and clear memory using:
    ```python
    %reset -f
    ```
- Since Streamlit apps cannot run natively in Google Colab or Kaggle, you'll have to follow some steps to deploy and access your app:
    1. **Save your app code**: Use the `%%writefile` magic command to save all the app code into a file named `app.py`. Include the following line at the top of the code cell containing your app:
    ```python
    %%writefile app.py
    ```
    2. **Generate a LocalTunnel password**: Run the following command to generate and a LocalTunnel password, and copy it.
    ```shell
    !curl https://loca.lt/mytunnelpassword
    ```
    3. **Launch the app**: Deploy your app by running the following command, which launches Streamlit on port `8501` and exposes it via LocalTunnel:
    ```shell
    !streamlit run app.py & npx localtunnel --port 8501
    ```
    - Once executed, this command will provide a public URL, such as: `https://<random_name>.loca.lt`. Use this link to access your app in a web browser, and use the password from Step 2.


Some helpful resources:
- [Streamlit cheat sheet](https://docs.streamlit.io/develop/quick-reference/cheat-sheet)

## :outbox_tray: Submission

- The structure of the required files for your submissions is as follows:
```
p7-<your_team_name>
|--- README.md (list names and e-mail IDs of team members at the top)
|--- p7.ipynb
|--- q3.png
```
- **If you have more than 1 member in your team**: please include a markdown cell, titled "Contributions", at the *beginning* or *end* of `p7.ipynb` that lists the contributions of each team member. For e.g.:  
```markdown
# Contributions
Jane: Q1.1-1.4, Q2.1-2.3
John: Q3
```

- **Technical issues within 36 hours of the deadline will not be considered as an excuse for late submission.**

### Point breakdown

Breakdown of total 12 points is as follows:
- Section 1: 3.5 points
   * Q1.1: 0.5 point 
   * Q1.2-Q1.4: 1 point each
- Section 2: 4 points
   * Q2.1: 0.5 points
   * Q2.2: 3 points
   * Q2.3: 0.5 points
- Section 3 (Q3): 4.5 points

## :trophy: Testing

Submissions will be **manually** graded.
