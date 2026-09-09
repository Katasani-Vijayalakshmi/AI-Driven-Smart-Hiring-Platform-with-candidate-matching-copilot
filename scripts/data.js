// ============================================================
//  AI RECRUITMENT COPILOT — MOCK DATA (Part 1)
// ============================================================

const MOCK = {

  stats: {
    dashboard: [
      { id: 'resumes',    label: 'Resumes Processed', value: 1247, delta: '+18%', up: true,  accent: 'rgba(99,102,241,0.15)' },
      { id: 'postings',   label: 'Active Job Postings', value: 42,   delta: '+8%',  up: true,  accent: 'rgba(6,182,212,0.15)' },
      { id: 'interviews', label: 'Interviews Scheduled', value: 156,  delta: '+24%', up: true,  accent: 'rgba(168,85,247,0.15)' },
      { id: 'hire-rate',  label: 'Hiring Success Rate', value: '89%', delta: '+5%',  up: true,  accent: 'rgba(16,185,129,0.15)' },
    ],
    parsing: [
      { id: 'processed',  label: 'Resumes Processed',  value: 247 },
      { id: 'accuracy',   label: 'Extraction Accuracy', value: '97%' },
      { id: 'profiles',   label: 'Profiles Created',    value: 235 },
    ],
  },

  pipeline: [
    { stage: 'Applied',    count: 1247, color: 'linear-gradient(180deg,#6366f1,#4f46e5)', height: 160 },
    { stage: 'Screened',   count: 782,  color: 'linear-gradient(180deg,#06b6d4,#0891b2)', height: 100 },
    { stage: 'Interviewed',count: 318,  color: 'linear-gradient(180deg,#a855f7,#9333ea)', height: 70  },
    { stage: 'Offered',    count: 94,   color: 'linear-gradient(180deg,#f59e0b,#d97706)', height: 42  },
    { stage: 'Hired',      count: 47,   color: 'linear-gradient(180deg,#10b981,#059669)', height: 24  },
  ],

  activities: [
    { icon: 'upload',  color: 'rgba(99,102,241,0.15)',  text: '<strong>Sarah Johnson</strong> resume uploaded and parsed — 97% match for Senior ML Engineer', time: '2 min ago' },
    { icon: 'user',    color: 'rgba(16,185,129,0.15)',  text: '<strong>Michael Chen</strong> profile created — 8 years experience in Full Stack Development', time: '14 min ago' },
    { icon: 'job',     color: 'rgba(6,182,212,0.15)',   text: 'New job posting <strong>Data Scientist III</strong> published — 23 required skills analyzed', time: '38 min ago' },
    { icon: 'match',   color: 'rgba(168,85,247,0.15)',  text: '<strong>Emily Rodriguez</strong> matched to <strong>Product Manager</strong> with 78% compatibility', time: '1 hr ago' },
    { icon: 'alert',   color: 'rgba(245,158,11,0.15)',  text: 'Batch processing complete — <strong>52 resumes</strong> parsed in 3.2 minutes', time: '2 hr ago' },
  ],

  candidates: [
    {
      id: 'c001', name: 'Sarah Johnson', initials: 'SJ',
      color: 'linear-gradient(135deg,#6366f1,#a855f7)',
      title: 'Senior Machine Learning Engineer', location: 'San Francisco, CA',
      email: 'sarah.j@example.com', phone: '+1 (555) 123-4567',
      experience: '5 years', education: 'MS Computer Science — Stanford',
      score: 92, scoreClass: 'high',
      skills: ['Python','TensorFlow','ML','NLP','Kubernetes','Docker','AWS'],
      skillColors: ['','','cyan','cyan','purple','purple',''],
      certifications: ['AWS Solutions Architect', 'TensorFlow Developer Certified'],
      summary: 'Experienced ML engineer specializing in NLP and computer vision. Built production ML pipelines serving 10M+ users at scale.',
      status: 'Processed',
      experience_list: [
        { role: 'Senior ML Engineer', company: 'OpenAI', period: '2022–Present', desc: 'Led development of large-scale language model fine-tuning pipelines. Improved inference latency by 40%.' },
        { role: 'ML Engineer', company: 'Google Brain', period: '2020–2022', desc: 'Contributed to TensorFlow core library. Developed AutoML feature extraction modules.' },
      ]
    },
    {
      id: 'c002', name: 'Michael Chen', initials: 'MC',
      color: 'linear-gradient(135deg,#06b6d4,#0891b2)',
      title: 'Full Stack Developer', location: 'Austin, TX',
      email: 'michael.c@example.com', phone: '+1 (555) 987-6543',
      experience: '8 years', education: 'BS Computer Engineering — UT Austin',
      score: 78, scoreClass: 'medium',
      skills: ['JavaScript','React','Node.js','PostgreSQL','Redis','GraphQL'],
      skillColors: ['','','cyan','cyan','purple','purple'],
      certifications: ['AWS Cloud Practitioner', 'MongoDB Developer'],
      summary: 'Full-stack engineer with deep expertise in React ecosystems and microservices architecture. Delivered 15+ enterprise applications.',
      status: 'Processed',
      experience_list: [
        { role: 'Senior Full Stack Developer', company: 'Stripe', period: '2019–Present', desc: 'Built payment orchestration UIs handling $2B+ transactions annually. Led team of 6 engineers.' },
        { role: 'Frontend Engineer', company: 'Airbnb', period: '2016–2019', desc: 'Developed React component library used across 40+ product teams. Reduced page load by 35%.' },
      ]
    },
    {
      id: 'c003', name: 'Emily Rodriguez', initials: 'ER',
      color: 'linear-gradient(135deg,#a855f7,#7c3aed)',
      title: 'Data Scientist', location: 'New York, NY',
      email: 'emily.r@example.com', phone: '+1 (555) 234-5678',
      experience: '4 years', education: 'MS Data Science — Columbia',
      score: 85, scoreClass: 'high',
      skills: ['Python','R','Statistics','Spark','Tableau','SQL','Scikit-learn'],
      skillColors: ['','cyan','cyan','','','','purple'],
      certifications: ['Google Data Analytics', 'Databricks Certified'],
      summary: 'Data scientist with expertise in predictive modeling and statistical analysis. Published 3 peer-reviewed papers in ML conference.',
      status: 'Processed',
      experience_list: [
        { role: 'Data Scientist', company: 'Netflix', period: '2021–Present', desc: 'Developed recommendation algorithms improving engagement by 22%. A/B tested 40+ model variants.' },
        { role: 'Data Analyst', company: 'McKinsey', period: '2020–2021', desc: 'Statistical analysis and reporting for Fortune 500 clients in healthcare and finance sectors.' },
      ]
    },
    {
      id: 'c004', name: 'James Carter', initials: 'JC',
      color: 'linear-gradient(135deg,#f59e0b,#d97706)',
      title: 'DevOps Engineer', location: 'Seattle, WA',
      email: 'james.c@example.com', phone: '+1 (555) 345-6789',
      experience: '6 years', education: 'BS Information Technology — UW',
      score: 65, scoreClass: 'medium',
      skills: ['Kubernetes','Docker','Terraform','AWS','CI/CD','Ansible'],
      skillColors: ['purple','purple','','','cyan',''],
      certifications: ['CKA (Kubernetes Admin)', 'AWS DevOps Engineer Professional'],
      summary: 'Experienced DevOps engineer specializing in cloud infrastructure and platform engineering. Reduced deployment time from hours to minutes.',
      status: 'Processed',
      experience_list: [
        { role: 'Senior DevOps Engineer', company: 'Microsoft Azure', period: '2021–Present', desc: 'Managed Kubernetes clusters serving 500k+ daily requests. Implemented GitOps workflows.' },
        { role: 'Cloud Engineer', company: 'Salesforce', period: '2018–2021', desc: 'Built Terraform infrastructure modules adopted by 200+ engineering teams globally.' },
      ]
    },
    {
      id: 'c005', name: 'Priya Patel', initials: 'PP',
      color: 'linear-gradient(135deg,#10b981,#059669)',
      title: 'Product Manager', location: 'Chicago, IL',
      email: 'priya.p@example.com', phone: '+1 (555) 456-7890',
      experience: '7 years', education: 'MBA — Kellogg School of Management',
      score: 71, scoreClass: 'medium',
      skills: ['Roadmapping','JIRA','SQL','A/B Testing','User Research','OKRs'],
      skillColors: ['cyan','','','cyan','purple',''],
      certifications: ['Certified Scrum Product Owner', 'Google PM Certificate'],
      summary: 'Strategic product manager with track record of launching 0→1 products. Led cross-functional teams of 20+ across design, engineering, and data.',
      status: 'Under Review',
      experience_list: [
        { role: 'Senior Product Manager', company: 'Figma', period: '2020–Present', desc: 'Owned collaboration product suite. Grew DAU from 500k to 4M+. Led FigJam launch.' },
        { role: 'Product Manager', company: 'HubSpot', period: '2017–2020', desc: 'Managed CRM integrations roadmap. Delivered 12 features with average NPS of 72.' },
      ]
    },
    {
      id: 'c006', name: 'Alex Kim', initials: 'AK',
      color: 'linear-gradient(135deg,#f43f5e,#e11d48)',
      title: 'Cybersecurity Analyst', location: 'Remote',
      email: 'alex.k@example.com', phone: '+1 (555) 567-8901',
      experience: '5 years', education: 'BS Cybersecurity — Carnegie Mellon',
      score: 88, scoreClass: 'high',
      skills: ['Penetration Testing','SIEM','Zero Trust','Python','Incident Response'],
      skillColors: ['','','cyan','','purple'],
      certifications: ['CISSP', 'CEH (Certified Ethical Hacker)', 'CompTIA Security+'],
      summary: 'Cybersecurity specialist in red team operations and threat intelligence. Uncovered 3 critical zero-day vulnerabilities in enterprise software.',
      status: 'Processed',
      experience_list: [
        { role: 'Security Engineer', company: 'CrowdStrike', period: '2021–Present', desc: 'Lead red team exercises for Fortune 100 clients. Developed threat detection playbooks.' },
        { role: 'Security Analyst', company: 'Palo Alto Networks', period: '2019–2021', desc: 'SOC operations — triaged 200+ alerts daily. Reduced MTTR by 60%.' },
      ]
    },
  ],

  jobs: [
    {
      id: 'j001', role: 'Senior Machine Learning Engineer', company: 'TechCorp AI', department: 'R&D',
      type: 'Full-time', level: 'Senior', location: 'San Francisco, CA (Hybrid)',
      salary: '$180K–$240K', applicants: 142,
      description: 'We are looking for an exceptional ML engineer to lead development of our next-generation AI products. You will work closely with research and product teams to bring cutting-edge models to production at scale.',
      mustHave: ['5+ years ML experience', 'Python (TensorFlow/PyTorch)', 'MLOps & CI/CD for ML', 'Distributed training', 'Cloud platforms (AWS/GCP)'],
      preferred: ['PhD in ML or related field', 'LLM fine-tuning experience', 'Kubernetes & Docker', 'Published research papers'],
      niceToHave: ['Rust or C++ for performance', 'Open-source contributions', 'Startup experience'],
      requiredSkills: ['Python','TensorFlow','PyTorch','Kubernetes','Docker','AWS','MLflow','LLMs'],
      aiInsight: 'This role demands deep production ML experience. Candidates should prioritize demonstrating deployed model scale and latency optimization. NLP/LLM experience significantly differentiates candidates.',
      postedDays: 3,
    },
    {
      id: 'j002', role: 'Full Stack Engineer (React/Node)', company: 'StartupXYZ', department: 'Engineering',
      type: 'Full-time', level: 'Mid', location: 'Remote (US)',
      salary: '$130K–$170K', applicants: 87,
      description: 'Join our fast-growing startup to build the next generation of SaaS tools. You\'ll own features end-to-end, from database schema to user interface.',
      mustHave: ['3+ years React experience', 'Node.js + REST/GraphQL', 'PostgreSQL or MySQL', 'CI/CD pipelines', 'TypeScript'],
      preferred: ['Next.js', 'Redis caching', 'Microservices architecture', 'AWS experience'],
      niceToHave: ['Mobile development (React Native)', 'Open source contributions'],
      requiredSkills: ['React','Node.js','TypeScript','PostgreSQL','GraphQL','AWS','Docker'],
      aiInsight: 'Ideal candidates combine strong frontend intuition with solid backend architecture skills. TypeScript proficiency and GraphQL experience are key differentiators for this role.',
      postedDays: 7,
    },
    {
      id: 'j003', role: 'Data Scientist — Recommendations', company: 'RetailGiant', department: 'Data & Analytics',
      type: 'Full-time', level: 'Mid–Senior', location: 'New York, NY',
      salary: '$140K–$190K', applicants: 203,
      description: 'Drive personalization at scale for our e-commerce platform. You will design, implement, and evaluate recommendation systems that serve 50M+ customers.',
      mustHave: ['4+ years Data Science', 'Python (Scikit-learn/XGBoost)', 'SQL & big data (Spark)', 'A/B testing frameworks', 'Statistics fundamentals'],
      preferred: ['Deep learning (PyTorch/Keras)', 'Recommendation system algorithms', 'Databricks', 'Real-time feature stores'],
      niceToHave: ['NLP for search relevance', 'Customer segmentation at scale'],
      requiredSkills: ['Python','Scikit-learn','SQL','Spark','A/B Testing','Statistics','Recommendation Systems'],
      aiInsight: 'Strong statistical foundation combined with scalable engineering is the primary requirement. Candidates with proven A/B testing methodology and large-scale recommendation system experience are prioritized.',
      postedDays: 12,
    },
    {
      id: 'j004', role: 'DevOps / Platform Engineer', company: 'CloudBase', department: 'Platform',
      type: 'Full-time', level: 'Senior', location: 'Seattle, WA',
      salary: '$150K–$200K', applicants: 58,
      description: 'Build and maintain the infrastructure that powers our globally distributed SaaS platform. You will lead cloud architecture decisions and platform reliability.',
      mustHave: ['Kubernetes (CKA preferred)', 'Terraform IaC', 'AWS or GCP expert level', 'CI/CD (GitHub Actions/ArgoCD)', 'Observability (Prometheus/Grafana)'],
      preferred: ['Platform engineering concepts', 'GitOps workflows', 'Security hardening', 'Cost optimization'],
      niceToHave: ['Go or Rust', 'eBPF / service mesh', 'Chaos engineering'],
      requiredSkills: ['Kubernetes','Terraform','AWS','Docker','CI/CD','Prometheus','ArgoCD','Helm'],
      aiInsight: 'Platform engineering maturity is key. Look for candidates who have designed self-service developer platforms, not just managed infrastructure. GitOps experience and SRE mindset are strong positives.',
      postedDays: 5,
    },
  ],

  avatarColors: [
    'linear-gradient(135deg,#6366f1,#a855f7)',
    'linear-gradient(135deg,#06b6d4,#0891b2)',
    'linear-gradient(135deg,#10b981,#059669)',
    'linear-gradient(135deg,#f59e0b,#d97706)',
    'linear-gradient(135deg,#f43f5e,#e11d48)',
    'linear-gradient(135deg,#a855f7,#7c3aed)',
  ],

};
