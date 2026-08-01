ROADMAP_TOPICS = {
    "python": "Practice Python basics, functions, file handling and small scripts.",
    "sql": "Learn SELECT, JOIN, GROUP BY and create two database practice tasks.",
    "excel": "Revise formulas, pivot tables, charts and basic dashboards.",
    "pandas": "Clean CSV data using Pandas and make summary tables.",
    "power bi": "Build one dashboard using Power BI charts and slicers.",
    "machine learning": "Study supervised learning and train one simple scikit-learn model.",
    "scikit-learn": "Try classification, regression and model evaluation in scikit-learn.",
    "fastapi": "Create a small FastAPI endpoint for model prediction.",
    "docker": "Learn Dockerfile basics and containerize a Python app.",
    "deep learning": "Understand neural networks and train a basic image or text model.",
    "llm": "Learn prompts, embeddings and basic LLM application flow.",
    "rag": "Build a small retrieval augmented generation example using documents.",
    "apis": "Practice calling REST APIs and reading JSON responses.",
    "nlp": "Learn tokenization, text cleaning, TF-IDF and named entity recognition.",
    "transformers": "Study transformer models and try one Hugging Face pipeline.",
    "hugging face": "Use Hugging Face datasets, models and inference pipeline.",
    "opencv": "Practice image reading, resizing, thresholding and object detection basics.",
    "cnn": "Learn convolution layers and train a small image classifier.",
    "yolo": "Try object detection using a pre-trained YOLO model.",
    "git": "Use Git for commits, branches and pushing the project to GitHub.",
    "cloud": "Deploy a small app on Streamlit Cloud, Render or another free service.",
    "mlflow": "Track one ML experiment with metrics and saved model versions.",
}


def create_roadmap(missing_skills):
    if not missing_skills:
        return ["Revise your projects and add measurable outcomes to the resume."]

    # Limit the roadmap to a few weeks so the output remains practical for students.
    roadmap = []
    for week, skill in enumerate(missing_skills[:6], start=1):
        topic = ROADMAP_TOPICS.get(
            skill.lower(), f"Study the basics of {skill} and make one mini project."
        )
        roadmap.append(f"Week {week}: {topic}")

    return roadmap
