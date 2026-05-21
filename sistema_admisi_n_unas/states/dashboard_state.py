import reflex as rx
from typing import TypedDict


class AreaMetric(TypedDict):
    area: str
    avg_score: float


class SidebarItem(TypedDict):
    label: str
    icon: str
    href: str


class DashboardState(rx.State):
    # Metrics data
    total_applicants: int = 1250
    admitted_count: int = 342
    general_avg: float = 14.5
    top_career: str = "Ingeniería Forestal"

    # Area scores for the bar chart
    area_scores: list[AreaMetric] = [
        {"area": "Matemática", "avg_score": 15.2},
        {"area": "Comunicación", "avg_score": 13.8},
        {"area": "Ciencias Nat.", "avg_score": 14.5},
        {"area": "Cultura Gral.", "avg_score": 12.1},
        {"area": "Psicotécnico", "avg_score": 16.4},
    ]

    # Sidebar state
    sidebar_items: list[SidebarItem] = [
        {"label": "Dashboard", "icon": "layout-dashboard", "href": "/"},
        {"label": "Postulantes", "icon": "users", "href": "/postulantes"},
        {"label": "Inscripción", "icon": "user-plus", "href": "/inscripcion"},
        {"label": "Examen", "icon": "file-pen", "href": "/examen"},
        {"label": "Resultados", "icon": "trophy", "href": "/resultados"},
        {
            "label": "Retroalimentación",
            "icon": "message-square",
            "href": "/retroalimentacion",
        },
    ]

    current_page: str = "Dashboard"

    @rx.event
    def set_page(self, page: str):
        self.current_page = page