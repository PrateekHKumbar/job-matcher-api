import re
from typing import Dict, List, Set, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Common engineering and software keywords dictionary
COMMON_TECH_KEYWORDS = {
    # Programming Languages
    "python", "c++", "c", "embedded c", "sql", "javascript", "typescript", "java", "html", "css", "bash", "rust", "go",
    # Frameworks & Libraries
    "fastapi", "flask", "django", "pandas", "numpy", "matplotlib", "scikit-learn", "tensorflow", "pytorch", "react", "node.js",
    # Databases & Cloud
    "sqlite", "postgresql", "mysql", "mongodb", "redis", "docker", "kubernetes", "aws", "gcp", "azure", "git", "github", "linux",
    # Embedded & Hardware
    "esp32", "arduino", "microcontroller", "i2c", "spi", "uart", "pwm", "adc", "freertos", "arm", "pcb", "stm32", "iot", "firmware",
    # Concepts & Methodologies
    "data structures", "algorithms", "oop", "rest api", "crud", "ci/cd", "unit testing", "agile", "debugging", "profiling"
}

def clean_text(text: str) -> str:
    """Preprocess text: lowercase, remove non-alphanumeric except common symbols."""
    text = text.lower()
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'[^\w\s\+\#\-\.\/]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_keywords(text: str) -> Set[str]:
    """Extract known technical keywords present in the text."""
    lowered = text.lower()
    found_keywords = set()
    for kw in COMMON_TECH_KEYWORDS:
        # Match as word boundary or exact phrase
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, lowered):
            found_keywords.add(kw)
    return found_keywords

def analyze_match(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Calculate semantic match score using TF-IDF + Cosine Similarity,
    and perform keyword gap analysis.
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)
    
    if not cleaned_resume or not cleaned_jd:
        return {
            "match_percentage": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "recommendations": ["Please provide both resume text and job description."]
        }
    
    # 1. TF-IDF & Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # 2. Keyword Matching
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)
    
    matched = sorted(list(resume_keywords.intersection(jd_keywords)))
    missing = sorted(list(jd_keywords - resume_keywords))
    
    # 3. Hybrid Score (60% Cosine Similarity + 40% Keyword Coverage)
    if len(jd_keywords) > 0:
        keyword_coverage = len(matched) / len(jd_keywords)
        hybrid_score = (cos_sim * 0.5) + (keyword_coverage * 0.5)
    else:
        hybrid_score = cos_sim
        
    final_percentage = round(min(max(hybrid_score * 100, 5.0), 98.0), 1)
    
    # 4. Actionable Recommendations
    recommendations = []
    if missing:
        top_missing = missing[:5]
        recommendations.append(f"Consider integrating high-priority keywords: {', '.join(top_missing)}.")
    
    if final_percentage >= 75:
        recommendations.append("Strong match! Tailor your project bullet points to directly mirror JD phrasing.")
    elif final_percentage >= 50:
        recommendations.append("Moderate match. Add more relevant tools and quantify your project impacts.")
    else:
        recommendations.append("Low match. Significant technical keyword gap detected between your resume and this JD.")
        
    return {
        "match_percentage": final_percentage,
        "cosine_similarity": round(float(cos_sim) * 100, 1),
        "total_jd_keywords": len(jd_keywords),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "recommendations": recommendations
    }
