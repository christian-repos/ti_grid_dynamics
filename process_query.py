from fastapi import HTTPException
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import RateLimitError  # noqa

from configs import Config

PROMPT_TEMPLATE = ChatPromptTemplate.from_template("""
You are an AI assistant whose main task is to provide clear and concise answers to questions. 
Your answer will mainly be based on the given context, which is as follows:
----------
{ai_context}
----------
With the above context, please answer the following question: {question_for_ai} """)


def generate_response(query: str) -> dict[str, str]:
    db = FAISS.load_local(Config.DB_NAME, Config.VOYAGE_AI_EMBEDDINGS, allow_dangerous_deserialization=True)
    results: list[tuple[Document, float]] = db.similarity_search_with_relevance_scores(query, k=2)
    if len(results) == 0 or results[0][1] < 0.75:
        raise HTTPException(status_code=404, detail="Unable to find matching results.")

    context = f"\n{10 * '-'}\n".join([doc.page_content for doc, _ in results])
    prompt = PROMPT_TEMPLATE.format(ai_context=context, question_for_ai=query)

    try:
        model = ChatOpenAI()
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("source", None) for doc, _ in results]
        return {"Response": response_text, "Learn more from sources": sources}  # noqa
    except RateLimitError as e:
        print(e)
        raise HTTPException(status_code=503, detail="Provided API key exceeded quota.", )


if __name__ == "__main__":
    print(generate_response("What criteria are used to deduplicate a list of ORM-mapped objects?"))
