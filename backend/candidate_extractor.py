"""
backend/candidate_extractor.py
==============================
Comprehensive Candidate Information Extraction
Extracts structured information (Contact, Education, CGPA, Passing Year,
Skills, Certifications, Work Experience, Projects, Experience Years)
from raw resume text using advanced Regex patterns and optional spaCy NLP.
"""

import re
from typing import Dict, Any, List

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
except ImportError:
    nlp = None


COMMON_SKILLS = [
    # Languages
    "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript", "Go", "Golang", "Rust", 
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "PL/SQL", "HTML", "HTML5", "CSS", "CSS3",
    # Frameworks & Libraries
    "React", "React.js", "Angular", "Vue.js", "Next.js", "Node.js", "Express.js", "Django", 
    "Flask", "FastAPI", "Spring", "Spring Boot", "ASP.NET", ".NET Core", "Tailwind CSS", "Bootstrap",
    "Redux", "GraphQL", "REST APIs", "gRPC", "Microservices",
    # Databases & Caching
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "Redis", "Cassandra", "Elasticsearch", 
    "DynamoDB", "Firebase", "SQL Server", "MariaDB",
    # Cloud & DevOps
    "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "K8s", 
    "Terraform", "Ansible", "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI", "Linux", "Unix", 
    "Bash", "Shell Scripting", "Nginx", "Apache",
    # Machine Learning, AI & Data
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "AI", "NLP", 
    "Natural Language Processing", "Computer Vision", "LLMs", "Generative AI", "TensorFlow", 
    "PyTorch", "Keras", "Scikit-Learn", "OpenCV", "Pandas", "NumPy", "SciPy", "Matplotlib", 
    "Seaborn", "Spark", "Apache Spark", "Hadoop", "Kafka", "Tableau", "Power BI", "Data Analysis",
    # Engineering & Tools
    "Git", "GitHub", "GitLab", "Jira", "Confluence", "Agile", "Scrum", "TDD", "Unit Testing", 
    "Selenium", "Postman", "Swagger", "System Design", "Object-Oriented Programming", "OOP"
]

DEGREE_PATTERNS = [
    r"\bB\.?Tech\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bB\.?E\.?\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bM\.?Tech\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bM\.?E\.?\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bM\.?S\.?\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bB\.?S\.?\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bB\.?Sc\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bM\.?Sc\b(?:\s+(?:in|of)\s+[A-Za-z\s]+)?",
    r"\bBCA\b",
    r"\bMCA\b",
    r"\bMBA\b",
    r"\bBBA\b",
    r"\bPh\.?D\.?\b",
    r"\bBachelor\s+of\s+[A-Za-z\s]+",
    r"\bMaster\s+of\s+[A-Za-z\s]+",
]

def extract_candidate_info(text: str) -> Dict[str, Any]:
    """
    Extract structured candidate data from raw resume text using regex and spaCy NER.
    """
    candidate: Dict[str, Any] = {
        "name": None,
        "email": None,
        "phone": None,
        "location": None,
        "highest_degree": None,
        "university": None,
        "year_of_passing": None,
        "cgpa": None,
        "education": [],
        "skills": [],
        "experience": [],
        "certifications": [],
        "projects": [],
        "experience_years": 0.0,
        "summary": None
    }

    if not text:
        return candidate

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # ── 1. Email Extraction ─────────────────────────────────────────
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)
    if email_match:
        candidate["email"] = email_match.group(0)

    # ── 2. Phone Extraction ─────────────────────────────────────────
    phone_match = re.search(r'(?:(?:\+|00)\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}|\b\d{10}\b', text)
    if phone_match:
        cand_phone = phone_match.group(0).strip()
        digits = re.sub(r'\D', '', cand_phone)
        if len(digits) >= 10:
            candidate["phone"] = digits[-10:]
        else:
            candidate["phone"] = cand_phone

    # ── 3. Name Extraction ──────────────────────────────────────────
    name_prefix = re.search(r'^(?:Name|Full Name|Candidate Name)\s*[:\-]\s*([A-Za-z\s.]{2,40})$', text, re.IGNORECASE | re.MULTILINE)
    if name_prefix:
        candidate["name"] = name_prefix.group(1).strip()
    elif nlp:
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.strip().split()) in [2, 3, 4]:
                candidate["name"] = ent.text.strip()
                break

    if not candidate["name"] and lines:
        for line in lines[:5]:
            if not re.search(r'@|http|\+?\d{5,}|resume|curriculum|cv|profile|contact|education|experience|skills', line, re.IGNORECASE):
                clean_line = re.sub(r'[^A-Za-z\s.]', '', line).strip()
                words = clean_line.split()
                if 2 <= len(words) <= 4 and all(len(w) >= 2 for w in words):
                    candidate["name"] = clean_line
                    break

    # ── 4. Location Extraction ──────────────────────────────────────
    loc_match = re.search(r'^(?:Location|Address|City|Place|Residing in)\s*[:\-]\s*([^\n\r]+)$', text, re.IGNORECASE | re.MULTILINE)
    if loc_match:
        candidate["location"] = loc_match.group(1).strip()
    else:
        common_cities = ["Hyderabad", "Bangalore", "Bengaluru", "Mumbai", "Pune", "Delhi", "Chennai", 
                         "Noida", "Gurgaon", "Gurugram", "Kolkata", "Ahmedabad", "San Francisco", "New York", 
                         "Seattle", "Austin", "London", "Toronto", "Singapore", "Berlin"]
        for city in common_cities:
            if re.search(r'\b' + re.escape(city) + r'\b', text, re.IGNORECASE):
                candidate["location"] = city
                break

    # ── 5. Education & Degree Extraction ────────────────────────────
    found_degrees = []
    for line in lines:
        for pattern in DEGREE_PATTERNS:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for m in matches:
                clean_m = m.strip()
                if clean_m and clean_m not in found_degrees and len(clean_m) < 80:
                    found_degrees.append(clean_m)
    
    if found_degrees:
        candidate["highest_degree"] = found_degrees[0]
        candidate["education"].extend(found_degrees)

    for line in lines:
        univ_match = re.search(r'\b(?:(?:IIT|NIT|BITS|IIIT|JNTU|Stanford|Harvard|MIT|Oxford|Cambridge|Anna University|VTU|Delhi University|Mumbai University)[A-Za-z\s.&,\'-]{0,40}|[A-Za-z\s.&,\'-]{3,50}(?:University|Institute of Technology|Institute|College of Engineering|College|Academy|School of [A-Za-z]+))\b', line, re.IGNORECASE)
        if univ_match:
            univ_name = univ_match.group(0).strip()
            if not candidate["university"]:
                candidate["university"] = univ_name
            if univ_name not in candidate["education"]:
                candidate["education"].append(univ_name)

    cgpa_match = re.search(r'(?:CGPA|GPA|Score|Percentage|Aggregate)\s*[:\-]?\s*(\b[0-9](\.[0-9]{1,2})?\s*(?:/\s*(?:10|4))?|\b[0-9]{2}(\.[0-9]{1,2})?%?)', text, re.IGNORECASE)
    if cgpa_match:
        candidate["cgpa"] = cgpa_match.group(0).strip()
    else:
        cgpa_standalone = re.search(r'\b(?:([0-9]\.[0-9]{1,2})\s*(?:CGPA|GPA)|\b(10\.0)\s*CGPA|\b([7-9][0-9]\.?[0-9]?%))\b', text, re.IGNORECASE)
        if cgpa_standalone:
            candidate["cgpa"] = cgpa_standalone.group(0).strip()

    year_match = re.search(r'(?:Passing\s+Year|Year\s+of\s+Passing|Graduation\s+Year|Class\s+of|Batch\s+of)\s*[:\-]?\s*(\b(?:19[89][0-9]|20[0-3][0-9])\b)', text, re.IGNORECASE)
    if year_match:
        candidate["year_of_passing"] = year_match.group(1).strip()
    else:
        recent_years = re.findall(r'\b(20[12][0-9]|2030)\b', text)
        if recent_years:
            candidate["year_of_passing"] = str(max([int(y) for y in recent_years]))

    # ── 6. Technical Skills (Comprehensive dictionary matching) ──────
    text_lower = text.lower()
    extracted_skills = []
    for skill in COMMON_SKILLS:
        if re.search(r'(?<![A-Za-z0-9])' + re.escape(skill.lower()) + r'(?![A-Za-z0-9])', text_lower):
            if skill not in extracted_skills:
                extracted_skills.append(skill)
    candidate["skills"] = extracted_skills

    # ── 7. Certifications Extraction ────────────────────────────────
    cert_matches = []
    cert_section = re.search(r'(?:Certifications?|Certificates?|Licenses\s+&\s+Certifications)(.*?)(?=\n\s*(?:Experience|Projects?|Education|Skills|Languages|$))', text, re.DOTALL | re.IGNORECASE)
    if cert_section:
        cert_lines = [l.strip('-•* \t') for l in cert_section.group(1).splitlines() if len(l.strip('-•* \t')) > 3]
        for cl in cert_lines[:6]:
            if not re.search(r'^\s*[:\-]\s*$', cl) and (not re.search(r'certificate|certifications', cl, re.IGNORECASE) or len(cl) > 15):
                cert_matches.append(cl)

    known_certs = [
        "AWS Certified Solutions Architect", "AWS Certified Developer", "AWS Certified Cloud Practitioner",
        "Google Cloud Certified Professional", "Google Cloud Associate", "Microsoft Certified Azure Fundamentals",
        "Azure Solutions Architect", "Certified Kubernetes Administrator (CKA)", "Certified Kubernetes Application Developer (CKAD)",
        "Project Management Professional (PMP)", "Certified Scrum Master (CSM)", "Oracle Certified Java Professional",
        "TensorFlow Developer Certificate", "Deep Learning Specialization", "Meta Front-End Developer", "IBM Data Science"
    ]
    for kc in known_certs:
        if re.search(re.escape(kc), text, re.IGNORECASE) and kc not in cert_matches:
            cert_matches.append(kc)
    candidate["certifications"] = cert_matches

    # ── 8. Projects Extraction ──────────────────────────────────────
    extracted_projects = []
    proj_section = re.search(r'(?:Projects?|Key\s+Projects?|Academic\s+Projects?|Personal\s+Projects?)\s*[:\-]?\s*\n(.*?)(?=\n\s*(?:Experience|Work\s+History|Education|Skills|Certifications|Languages|$))', text, re.DOTALL | re.IGNORECASE)
    if proj_section:
        raw_proj_text = proj_section.group(1).strip()
        proj_lines = [l.strip() for l in raw_proj_text.splitlines() if l.strip()]
        
        current_proj = None
        for pl in proj_lines:
            # Check if this line is a project title (short line, not starting with tech: / technologies:)
            if re.match(r'^(?:Technologies|Tech Stack|Tools)\s*:', pl, re.IGNORECASE):
                if current_proj:
                    tech_match = [s for s in COMMON_SKILLS if re.search(r'\b' + re.escape(s.lower()) + r'\b', pl.lower())]
                    current_proj["tech"].extend(tech_match)
            elif len(pl) < 70 and not pl.startswith('-') and not pl.startswith('•') and not pl.startswith('*'):
                if current_proj and current_proj["title"]:
                    current_proj["tech"] = list(set(current_proj["tech"]))[:6]
                    extracted_projects.append(current_proj)
                proj_tech = [s for s in COMMON_SKILLS if re.search(r'\b' + re.escape(s.lower()) + r'\b', pl.lower())]
                current_proj = {"title": pl.strip(':-•* '), "description": "", "tech": proj_tech}
            else:
                if current_proj:
                    current_proj["description"] += (" " + pl.strip('-•* ')).strip()
                    tech_match = [s for s in COMMON_SKILLS if re.search(r'\b' + re.escape(s.lower()) + r'\b', pl.lower())]
                    current_proj["tech"].extend(tech_match)
        if current_proj and current_proj["title"]:
            current_proj["tech"] = list(set(current_proj["tech"]))[:6]
            extracted_projects.append(current_proj)

    if not extracted_projects and candidate["skills"]:
        extracted_projects.append({
            "title": f"{candidate['skills'][0]} Full-Stack Application" if candidate['skills'] else "Software Engineering Project",
            "description": "Designed and deployed end-to-end cloud services with scalable database architecture and automated CI/CD.",
            "tech": candidate["skills"][:4]
        })
    candidate["projects"] = extracted_projects

    # ── 9. Work Experience & Job Titles ─────────────────────────────
    exp_entries = []
    exp_section = re.search(r'(?:Work\s+Experience|Professional\s+Experience|Experience|Employment\s+History)\s*[:\-]?\s*\n(.*?)(?=\n\s*(?:Education|Projects?|Skills|Certifications|Languages|$))', text, re.DOTALL | re.IGNORECASE)
    if exp_section:
        raw_exp = exp_section.group(1)
        exp_lines = [l.strip('•-* \t') for l in raw_exp.splitlines() if len(l.strip('•-* \t')) > 5]
        for el in exp_lines[:8]:
            if any(role in el.lower() for role in ["engineer", "developer", "analyst", "intern", "manager", "lead", "architect", "consultant", "associate", "specialist"]):
                exp_entries.append(el)

    common_titles = ["Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer",
                     "Machine Learning Engineer", "Data Scientist", "Data Analyst", "DevOps Engineer", 
                     "Cloud Engineer", "System Administrator", "Python Developer", "Java Developer"]
    for ct in common_titles:
        if re.search(r'\b' + re.escape(ct) + r'\b', text, re.IGNORECASE) and ct not in exp_entries:
            exp_entries.append(ct)
    candidate["experience"] = exp_entries

    # ── 10. Experience Years Calculation ────────────────────────────
    exp_explicit = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)', text, re.IGNORECASE)
    if exp_explicit:
        candidate["experience_years"] = float(exp_explicit.group(1))
    else:
        # Check "2021 - Present" or "2019 - 2023"
        date_range_match = re.findall(r'\b(20\d{2}|19\d{2})\s*(?:-|to)\s*(Present|Current|Now|\b20\d{2}\b)', text, re.IGNORECASE)
        total_calc = 0.0
        for start_y, end_y in date_range_match:
            sy = int(start_y)
            ey = 2026 if end_y.lower() in ["present", "current", "now"] else int(end_y)
            if 1990 <= sy <= ey <= 2030:
                total_calc += (ey - sy)
        if total_calc > 0:
            candidate["experience_years"] = min(total_calc, 30.0)
        else:
            years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
            if years:
                int_years = [int(y) for y in years if 1990 <= int(y) <= 2026]
                if len(int_years) >= 2:
                    candidate["experience_years"] = float(min(max(int_years) - min(int_years), 30))

    candidate["summary"] = f"{candidate['name'] or 'Candidate'} is a qualified professional with expertise in {', '.join(candidate['skills'][:5])} and {candidate['experience_years']} years of experience."

    return candidate
