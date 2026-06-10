import gradio as gr
from query import ask
from retrieval import search

def handle_query(question):
    answer = ask(question)

    results = search(question, k=5)

    sources = []

    # ChromaDB safe extraction
    if isinstance(results, dict) and "documents" in results:
        sources = results["documents"][0]  # list of texts

    else:
        # fallback if search returns different format
        for r in results:
            if isinstance(r, str):
                sources.append(r)
            elif isinstance(r, dict) and "document" in r:
                sources.append(r["document"])

    return answer, "\n\n".join(sources)

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🎓 Professor RAG System</h1>")

    inp = gr.Textbox(label="❓ Your question")

    btn = gr.Button("🚀 Ask")

    answer_box = gr.Textbox(label="💡 Answer", lines=8)
    sources_box = gr.Textbox(label="📚 Sources", lines=8)

    btn.click(handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, sources_box])

demo.launch()