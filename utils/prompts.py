from langchain_core.prompts import ChatPromptTemplate


def get_rag_prompt():
    """
    Prompt for Retrieval-Augmented Generation.
    """

    return ChatPromptTemplate.from_template(
        """
You are ClinicalDoc AI, an intelligent medical document assistant.

Your task is to answer the user's question ONLY using the provided context.

Instructions:

- Do not use outside knowledge.
- If the answer is not present in the context, say:
  "I could not find the answer in the uploaded document."
- Keep answers factual and concise.
- Quote medicine names, dosages, lab values, and diagnoses exactly as written.
- Mention the page number whenever possible.
- Never hallucinate.

Context:
{context}

Question:
{question}

Answer:
"""
    )


def get_multi_query_prompt():
    """
    Prompt for Multi Query Generation.
    """

    return ChatPromptTemplate.from_template(
        """
You are an expert medical search assistant.

Generate {count} different search queries for the user's question.

Rules:

- Preserve medical terminology.
- Cover different search perspectives.
- Avoid duplicate queries.
- Return one query per line.
- Do not number the queries.

Question:
{question}
"""
    )


def get_summary_prompt():
    """
    Prompt for Medical Document Summarization.
    """

    return ChatPromptTemplate.from_template(
        """
Summarize the following medical document.

Include:

- Chief Complaint
- Diagnosis
- Medications
- Lab Findings
- Treatment Plan
- Follow-up Recommendations

Document:

{context}

Summary:
"""
    )


def get_entity_extraction_prompt():
    """
    Prompt for Clinical Entity Extraction.
    """

    return ChatPromptTemplate.from_template(
        """
Extract the following clinical entities from the medical text.

Return JSON.

Fields:

- Diseases
- Symptoms
- Medications
- Dosages
- Procedures
- Lab Tests
- Vital Signs

Medical Text:

{context}
"""
    )