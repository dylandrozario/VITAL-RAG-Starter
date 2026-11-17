# Evidence to submit

The responses below are transcribed or summarized from the screenshots in this directory. Source support was checked against the fictional files in `knowledge_base`. Retrieved filenames are those displayed in the RAG screenshots; they do not necessarily mean that every listed file answers the question.

## 1. Cancellation

- **Question:** How many hours before an appointment must I cancel?
- **Expected source:** `cancellations.txt`.
- **Retrieved filenames:** `cancellations.txt`, `scheduling.txt`.
- **Without RAG:** The model said it could not answer without more context and asked for clarification. ([Screenshot](Non-RAG-questions-3.png))
- **With RAG:** “You must cancel your appointment at least 18 hours before the scheduled time.” ([Screenshot](RAG-questions-1.png))
- **Supported?** Yes. `cancellations.txt` specifies at least 18 hours. The non-RAG response did not provide the policy.

## 2. Same-day appointments

- **Question:** Can I request a same-day appointment?
- **Expected source:** `scheduling.txt`.
- **Retrieved filenames:** `scheduling.txt`, `portal.txt`.
- **Without RAG:** Not shown in the supplied screenshots.
- **With RAG:** “Yes, you can request a same-day appointment, but it must be available.” ([Screenshot](RAG-questions-1.png))
- **Supported?** Yes. `scheduling.txt` says same-day appointments may be requested subject to availability. A comparison with the non-RAG answer is not available.

## 3. Laboratory results

- **Question:** How are laboratory results communicated?
- **Expected source:** `lab_results.txt`.
- **Retrieved filenames:** `lab_results.txt`, `portal.txt`.
- **Without RAG:** The model listed general possibilities including written reports, email or electronic records, phone calls, in-person consultations, notifications, educational materials, and follow-up appointments. ([Screenshot](Non-RAG-questions-2.png))
- **With RAG:** “Laboratory results are communicated through the secure patient portal.” ([Screenshot](RAG-questions-1.png))
- **Supported?** Yes for the RAG answer: `lab_results.txt` specifies the secure patient portal. The broader non-RAG list contains methods the clinic policy does not establish.

## 4. Free transportation

- **Question:** Does the clinic provide free transportation?
- **Expected source:** None; the supplied policies do not answer this question.
- **Retrieved filenames:** `billing.txt`, `portal.txt`.
- **Without RAG:** The model said it lacked specific information about the clinic and suggested searching online or contacting it. ([Screenshot](Non-RAG-questions-1.png))
- **With RAG:** “I do not have enough information in the provided documents.” ([Screenshot](RAG-questions-2.png))
- **Supported?** The refusal is appropriate because the policies do not establish a transportation benefit. The retrieved files do not answer the question. The RAG screenshot includes the additional prompt text “(The documents do not answer this.)”, so this is not a controlled comparison of identical prompts.

## 5. Unsupported policy

- **Question:** What happens when I ask about an unsupported policy?
- **Expected source:** None of the policy files describes chatbot behavior; the fallback instruction is in `llm.py`.
- **Retrieved filenames:** `lab_results.txt`, `scheduling.txt`.
- **Without RAG:** The model interpreted “unsupported policy” as a software compatibility issue and suggested consulting documentation or support. ([Screenshot](Non-RAG-questions-1.png))
- **With RAG:** The model said the response would be “I do not have enough information in the provided documents.” ([Screenshot](RAG-questions-2.png))
- **Supported?** The policy documents do not describe the chatbot's fallback. The answer reflects the instruction in `llm.py`, not a fact supported by the retrieved documents. It also adds an introduction rather than returning the fallback text exactly as instructed.

## Failure, change, and test outcome

The starter retrieval functions raised `NotImplementedError`, so document loading, retrieval, and context formatting could not work. The change implemented sorted document loading, TF-IDF cosine ranking with positive-score filtering and filename tie-breaking, and source-labelled context; the app now passes that context to the model when RAG is enabled. Tests were also added for ordering, ties, unrelated documents, unknown words, and multiple source headers. After the change, `pytest -q` completed with **9 passed**. The initial test run could not run because pytest was not installed, so a failing pre-change test result was not captured.

A **retrieval failure** occurs when the needed source is missed or irrelevant sources are returned. For example, the transportation screenshot lists billing and portal documents even though neither answers the question; retrieval of a file alone is not evidence that it contains an answer. A **generation failure** occurs when the model gives an unsupported or incorrect answer despite the context it has, or fails an output instruction. The unsupported-policy response illustrates the latter: it includes the fallback wording but does not output the exact prescribed sentence by itself. The passing retrieval tests do not establish that model responses are always supported, and the screenshots do not show a rerun fixing that generation issue.
