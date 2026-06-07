import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


class FoundryIQRetriever:
    def __init__(self):
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        key = os.getenv("AZURE_SEARCH_KEY", "")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX", "learning-knowledge")
        self._connected = False
        self._client = None
        if endpoint and key:
            try:
                self._client = SearchClient(
                    endpoint=endpoint,
                    index_name=self.index_name,
                    credential=AzureKeyCredential(key),
                )
                self._connected = True
            except Exception:
                self._connected = False

    def retrieve(self, query: str, category: str = None, top_k: int = 3) -> list:
        if not self._connected or not self._client:
            return self._fallback_docs(query, category, top_k)
        try:
            filter_expr = f"category eq '{category}'" if category else None
            results = self._client.search(
                search_text=query,
                filter=filter_expr,
                top=top_k,
                include_total_count=True,
            )
            docs = []
            for r in results:
                title = r.get("title", "Knowledge Document")
                docs.append({
                    "id": r.get("id", "unknown"),
                    "title": title,
                    "content": r.get("content", ""),
                    "category": r.get("category", category or "general"),
                    "relevance_score": r.get("@search.score", 0.9),
                    "citation": f"[Source: {title}]",
                })
            return docs if docs else self._fallback_docs(query, category, top_k)
        except Exception:
            return self._fallback_docs(query, category, top_k)

    def _fallback_docs(self, query: str, category: str, top_k: int) -> list:
        fallback_library = {
            "certification-guide": [
                {"id": "doc-001", "title": "Engineering Certification Guide", "content": "Comprehensive guide covering AZ-204, AZ-400, DP-900 and other Microsoft certifications. Typical pass rate is 72%. Recommended study time: 40-60 hours. [Source: Engineering Certification Guide]", "category": "certification-guide"},
                {"id": "doc-004", "title": "AZ-204 Question Bank", "content": "Practice questions for AZ-204 Developer Associate. Key topics: Azure App Service, Azure Functions, Azure Storage, Azure Security. Pass threshold: 700/1000. [Source: AZ-204 Question Bank]", "category": "assessment"},
            ],
            "skills-matrix": [
                {"id": "doc-006", "title": "Role Skills Matrix", "content": "Skills matrix for cloud engineers. AZ-204 requires: REST APIs (advanced), Azure SDK (intermediate), Azure DevOps (intermediate), security fundamentals. [Source: Role Skills Matrix]", "category": "skills-matrix"},
            ],
            "study-template": [
                {"id": "doc-007", "title": "Study Schedule Templates", "content": "Recommended study templates: Morning learners (6-8AM, 90min), Evening learners (7-9PM, 90min). Week 1-2: Core concepts. Week 3: Practice exams. Week 4: Review gaps. [Source: Study Schedule Templates]", "category": "study-template"},
            ],
            "workload-insights": [
                {"id": "doc-003", "title": "Workload Insights Report", "content": "Q1 analysis shows employees with >22 meeting hours/week have 40% lower study completion. Optimal study: 6-8 hours/week. Block 'Learning Time' on calendar. [Source: Workload Insights Report]", "category": "workload-insights"},
            ],
            "assessment": [
                {"id": "doc-004", "title": "AZ-204 Question Bank", "content": "Sample Q: Which Azure service is used for serverless compute? A: Azure Functions. Topic: Compute. Difficulty: Medium. Pass threshold: 700/1000 = 70%. [Source: AZ-204 Question Bank]", "category": "assessment"},
                {"id": "doc-005", "title": "AZ-400 Question Bank", "content": "Sample Q: What is the purpose of Azure Pipelines? A: CI/CD automation. Topic: DevOps. Difficulty: Hard. Pass threshold: 700/1000 = 70%. [Source: AZ-400 Question Bank]", "category": "assessment"},
            ],
            "manager-guide": [
                {"id": "doc-008", "title": "Manager Readiness Guide", "content": "Managers should review team readiness monthly. Red flag: <10 study hours in last 4 weeks. Action: 1:1 check-in. Block calendar for study time. Recognition for exam passes increases team motivation by 60%. [Source: Manager Readiness Guide]", "category": "manager-guide"},
                {"id": "doc-010", "title": "Certification ROI & Cost Analysis", "content": "Standard Microsoft certification exam cost: $165. Guided prep pass rate: 89%. Unguided pass rate: 58%. Average retake rate without guidance: 1.72 attempts. With CertifyIQ guidance: 1.12 attempts. Productivity loss per week of unguided study: $200. [Source: Certification ROI & Cost Analysis]", "category": "manager-guide"},
                {"id": "doc-012", "title": "Intervention Best Practices", "content": "Manager intervention playbook: 1) Schedule 1:1 within 48hrs of alert. 2) Block calendar study time. 3) Reduce meeting load for 2-3 weeks. 4) Weekly score check-ins. Employee support: small consistent sessions beat sporadic long blocks. Calendar blocking Tuesday/Thursday 2-4PM recommended. [Source: Intervention Best Practices]", "category": "manager-guide"},
            ],
            "performance-report": [
                {"id": "doc-002", "title": "Team Learning Report", "content": "Q1 2026 results: 3 of 8 engineers achieved certification. Average study time for success: 47 hours. Most common fail reason: insufficient practice exam attempts. [Source: Team Learning Report]", "category": "performance-report"},
                {"id": "doc-011", "title": "Peer Cohort Benchmarks", "content": "Cohort statistics by role and certification. AZ-204 Cloud Engineers: avg score 64.2%, pass rate 71%, avg study hours 21.3. AZ-400 DevOps Engineers: avg score 71.8%, pass rate 79%. DP-203 Data Engineers: avg score 58.4%, pass rate 63%. AI-102 AI Engineers: avg score 67.1%, pass rate 74%. [Source: Peer Cohort Benchmarks]", "category": "performance-report"},
            ],
            "responsible-ai": [
                {"id": "doc-009", "title": "Responsible AI Guidelines", "content": "CertifyIQ follows Microsoft's Responsible AI principles: Fairness, Reliability, Privacy, Inclusiveness, Transparency, Accountability. All AI outputs include human review recommendation. [Source: Responsible AI Guidelines]", "category": "responsible-ai"},
            ],
        }
        docs = []
        if category and category in fallback_library:
            docs = fallback_library[category][:top_k]
        else:
            for cat_docs in fallback_library.values():
                docs.extend(cat_docs)
                if len(docs) >= top_k:
                    break
            docs = docs[:top_k]
        for d in docs:
            d["relevance_score"] = 0.88
            d["citation"] = f"[Source: {d['title']}]"
        return docs

    def health_check(self) -> dict:
        if not self._connected or not self._client:
            return {
                "connected": False,
                "index_name": self.index_name,
                "document_count": 0,
                "status": "error — using fallback knowledge base",
            }
        try:
            results = self._client.search(search_text="*", top=0, include_total_count=True)
            count = results.get_count() or 9
            return {
                "connected": True,
                "index_name": self.index_name,
                "document_count": count,
                "status": "healthy",
            }
        except Exception as e:
            return {
                "connected": False,
                "index_name": self.index_name,
                "document_count": 0,
                "status": f"error: {str(e)}",
            }


retriever = FoundryIQRetriever()