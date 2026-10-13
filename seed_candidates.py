import json
import random
from datetime import datetime, timedelta
from backend.api import database, models, auth

def seed_database():
    db = database.SessionLocal()
    try:
        # Create default recruiter if not present
        recruiter = db.query(models.User).filter(models.User.role == models.RoleEnum.recruiter).first()
        if not recruiter:
            recruiter = models.User(
                username="recruiter_admin",
                email="admin@recruitmentcopilot.ai",
                password_hash=auth.get_password_hash("password123"),
                role=models.RoleEnum.recruiter
            )
            db.add(recruiter)
            db.commit()
            db.refresh(recruiter)
            print(f"Created default recruiter: recruiter_admin")

        # Create standard jobs if not present
        job_data = [
            {"title": "Machine Learning Engineer", "department": "AI Research", "experience_required": 2.0, "education_required": "Master's Degree", "required_skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "PyTorch"]},
            {"title": "Java Developer", "department": "Backend Engineering", "experience_required": 3.0, "education_required": "Bachelor's Degree", "required_skills": ["Java", "Spring Boot", "SQL", "Microservices"]},
            {"title": "Data Analyst", "department": "Analytics", "experience_required": 1.0, "education_required": "Bachelor's Degree", "required_skills": ["Python", "SQL", "Data Analysis", "Excel", "Tableau"]},
            {"title": "Python Developer", "department": "Software Engineering", "experience_required": 2.0, "education_required": "Bachelor's Degree", "required_skills": ["Python", "Django", "FastAPI", "PostgreSQL"]},
            {"title": "Software Engineer", "department": "Core Platform", "experience_required": 2.0, "education_required": "Bachelor's Degree", "required_skills": ["Python", "Java", "Docker", "AWS", "Git"]}
        ]

        jobs_map = {}
        for j_info in job_data:
            j = db.query(models.Job).filter(models.Job.title == j_info["title"]).first()
            if not j:
                j = models.Job(
                    title=j_info["title"],
                    department=j_info["department"],
                    experience_required=j_info["experience_required"],
                    education_required=j_info["education_required"],
                    required_skills=j_info["required_skills"],
                    recruiter_id=recruiter.id
                )
                db.add(j)
                db.commit()
                db.refresh(j)
            jobs_map[j_info["title"]] = j.id

        # Raw data records from OCR pages
        candidates_raw = [
            ("Aarav Mehta", "aarav_mehta@example.com", "+91 9000000001", "Hyderabad", "Machine Learning Engineer", 2.0, "B.E Computer Science", ["Python", "SQL", "TensorFlow", "Machine Learning"], "Applied", "Career Portal", 0.96),
            ("Ananya Rao", "ananya_rao@example.com", "+91 9000000002", "Bengaluru", "Java Developer", 6.0, "B.Tech CSE", ["Java", "SQL", "Spring Boot"], "reviewed", "Career Portal", 0.67),
            ("Rohan Sharma", "rohan_sharma@example.com", "+91 9000000003", "Chennai", "Data Analyst", 0.5, "B.E Computer Science", ["Python", "Machine Learning", "Generative AI"], "pending", "Campus", 0.65),
            ("Priya Nair", "priya_nair@example.com", "+91 9000000004", "Pune", "Python Developer", 7.0, "MBA", ["SQL", "Excel", "Generative AI"], "pending", "Direct", 0.87),
            ("Vikram Singh", "vikram_singh@example.com", "+91 9000000005", "Mumbai", "Software Engineer", 0.5, "MBA", ["Python", "AWS Cloud", "Docker"], "reviewed", "Campus", 0.71),
            ("Neha Reddy", "neha_reddy@example.com", "+91 9000000006", "Delhi", "Machine Learning Engineer", 2.0, "MBA", ["Java", "SQL", "AWS Cloud"], "accepted", "Direct", 0.98),
            ("Arjun Kumar", "arjun_kumar@example.com", "+91 9000000007", "Visakhapatnam", "Java Developer", 0.5, "MBA", ["Python", "NLP", "Generative AI"], "pending", "Career Portal", 0.75),
            ("Meera Iyer", "meera_iyer@example.com", "+91 9000000008", "Vijayawada", "Data Analyst", 5.0, "M.Sc Data Science", ["JavaScript", "Java", "Python"], "accepted", "Direct", 0.91),
            ("Rahul Verma", "rahul_verma@example.com", "+91 9000000009", "Hyderabad", "Python Developer", 1.0, "B.E Computer Science", ["Python", "SQL", "AWS Cloud"], "accepted", "Direct", 0.81),
            ("Kavya Patel", "kavya_patel@example.com", "+91 9000000010", "Bengaluru", "Software Engineer", 4.0, "M.Tech AI", ["Python", "PyTorch"], "accepted", "Career Portal", 0.94),
            ("Aditya Das", "aditya_das@example.com", "+91 9000000011", "Chennai", "Machine Learning Engineer", 2.0, "B.E Computer Science", ["Python", "SQL", "Python Data"], "pending", "Career Portal", 0.66),
            ("Sneha Joshi", "sneha_joshi@example.com", "+91 9000000012", "Pune", "Java Developer", 2.0, "MBA", ["Java", "SQL", "Python Data"], "pending", "Campus", 0.66),
            ("Kiran Reddy", "kiran_reddy@example.com", "+91 9000000013", "Mumbai", "Data Analyst", 4.0, "B.Tech CSE", ["Python", "Machine Learning", "Generative AI"], "reviewed", "Direct", 0.90),
            ("Nikhil Rao", "nikhil_rao@example.com", "+91 9000000014", "Delhi", "Python Developer", 3.0, "M.Tech AI", ["SQL", "Excel", "Generative AI"], "accepted", "LinkedIn", 0.72),
            ("Ishita Gupta", "ishita_gupta@example.com", "+91 9000000015", "Visakhapatnam", "Software Engineer", 0.0, "B.E Computer Science", ["Python", "Java Programming"], "reviewed", "Referral", 0.87),
            ("Manish Yadav", "manish_yadav@example.com", "+91 9000000016", "Vijayawada", "Machine Learning Engineer", 4.0, "B.Tech CSE", ["Java", "SQL", "AWS Cloud"], "accepted", "Campus", 0.97),
            ("Divya Menon", "divya_menon@example.com", "+91 9000000017", "Hyderabad", "Java Developer", 3.0, "MBA", ["Python", "NLP", "Java"], "accepted", "LinkedIn", 0.86),
            ("Sanjay Kumar", "sanjay_kumar@example.com", "+91 9000000018", "Bengaluru", "Data Analyst", 0.5, "B.E Computer Science", ["JavaScript", "AWS Cloud"], "reviewed", "Referral", 0.62),
            ("Pooja Shah", "pooja_shah@example.com", "+91 9000000019", "Chennai", "Python Developer", 6.0, "B.E Computer Science", ["Python", "SQL", "Java"], "reviewed", "Career Portal", 0.71),
            ("Harish Babu", "harish_babu@example.com", "+91 9000000020", "Pune", "Software Engineer", 2.0, "MBA", ["Python", "PyTorch"], "reviewed", "Referral", 0.94),
            ("Sarah Johnson", "sarah_johnson@example.com", "(555) 123-4567", "San Francisco, CA", "Machine Learning Engineer", 5.0, "MS Computer Science", ["Python", "Machine Learning", "Data Analysis", "TensorFlow", "SQL", "Project Management"], "accepted", "Direct", 0.97),
            ("Michael Chen", "michael_chen@example.com", "(555) 987-6543", "San Jose, CA", "Software Engineer", 8.0, "BS Software Engineering", ["JavaScript", "React", "Node.js", "Docker", "AWS"], "accepted", "LinkedIn", 0.92)
        ]

        count = 0
        cgpa_list = ["8.8 CGPA", "9.2 CGPA", "8.5 CGPA", "7.9 CGPA", "9.0 CGPA", "8.4 CGPA", "9.5 CGPA", "8.1 CGPA"]
        univ_list = ["IIT Hyderabad", "IISc Bengaluru", "Anna University", "Savitribai Phule Pune University", "Mumbai University", "Delhi Technological University", "BITS Pilani", "JNTU Hyderabad"]
        year_list = ["2022", "2023", "2024", "2021", "2020", "2025"]

        for idx, (name, email, phone, location, target_role, exp, edu, skills, status_str, source, match_score) in enumerate(candidates_raw):
            cgpa_val = cgpa_list[idx % len(cgpa_list)]
            univ_val = univ_list[idx % len(univ_list)]
            year_val = year_list[idx % len(year_list)]

            user = db.query(models.User).filter(models.User.email == email).first()
            if not user:
                username = name.replace(" ", "").lower()
                user = models.User(
                    username=username,
                    email=email,
                    password_hash=auth.get_password_hash("password123"),
                    role=models.RoleEnum.candidate,
                    full_name=name,
                    phone=phone,
                    location=location,
                    highest_degree=edu,
                    university=univ_val,
                    year_of_passing=year_val,
                    cgpa=cgpa_val,
                    skills=skills,
                    projects=[{"title": f"{target_role} Automation Engine", "description": "Designed and deployed real-time processing pipeline.", "tech": skills[:3]}]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            else:
                user.full_name = name
                user.phone = phone
                user.location = location
                user.highest_degree = edu
                user.university = univ_val
                user.year_of_passing = year_val
                user.cgpa = cgpa_val
                user.skills = skills
                user.projects = [{"title": f"{target_role} Automation System", "description": "End-to-end cloud pipeline implementation.", "tech": skills[:3]}]
                db.commit()

            job_id = jobs_map.get(target_role, jobs_map["Software Engineer"])

            status_enum = models.ApplicationStatusEnum.pending
            if status_str.lower() in ["reviewed", "interview", "screened"]:
                status_enum = models.ApplicationStatusEnum.reviewed
            elif status_str.lower() in ["accepted", "shortlisted"]:
                status_enum = models.ApplicationStatusEnum.accepted
            elif status_str.lower() in ["rejected"]:
                status_enum = models.ApplicationStatusEnum.rejected

            app = db.query(models.Application).filter(models.Application.user_id == user.id, models.Application.job_id == job_id).first()
            parsed_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "experience": f"{exp} years",
                "education": [f"{edu} ({univ_val}, {year_val}) — {cgpa_val}"],
                "university": univ_val,
                "year_of_passing": year_val,
                "cgpa": cgpa_val,
                "skills": skills,
                "projects": user.projects
            }

            if not app:
                app = models.Application(
                    user_id=user.id,
                    job_id=job_id,
                    education=f"{edu} • {univ_val}",
                    university=univ_val,
                    year_of_passing=year_val,
                    cgpa=cgpa_val,
                    experience_years=exp,
                    skills=skills,
                    parsed_data=parsed_data,
                    status=status_enum,
                    hiring_score=match_score
                )
                db.add(app)
                db.commit()
                count += 1
            else:
                app.university = univ_val
                app.year_of_passing = year_val
                app.cgpa = cgpa_val
                app.parsed_data = parsed_data
                db.commit()

        print(f"Successfully seeded/updated {len(candidates_raw)} candidate records in database!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
