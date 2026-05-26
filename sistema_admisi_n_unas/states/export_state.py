"""Export state for data export functionality."""
import reflex as rx
from typing import List, Dict, Any
from sistema_admisi_n_unas.reports import export_to_csv, generate_postulantes_report, generate_resultados_report, generate_stats_report
from sistema_admisi_n_unas.utils.csv_loader import cargar_postulantes


class ExportState(rx.State):
    """State for managing data exports."""

    # Export status
    exporting: bool = False
    export_message: str = ""
    last_export_path: str = ""

    # Progress tracking
    export_progress: float = 0.0

    @rx.event
    def export_postulantes_csv(self):
        """Export postulants to CSV."""
        self.exporting = True
        self.export_progress = 0.0
        self.export_message = "Exportando postulantes..."

        try:
            postulantes = cargar_postulantes()
            self.export_progress = 50.0

            if not postulantes:
                self.exporting = False
                self.export_message = "No hay datos para exportar"
                return

            filepath = export_to_csv(postulantes, "postulantes")
            self.export_progress = 100.0
            self.last_export_path = filepath
            self.export_message = f"Exportación exitosa: {filepath.split('/')[-1]}"

            # Trigger download
            return rx.download(url=filepath, filename=filepath.split("/")[-1])

        except Exception as e:
            self.exporting = False
            self.export_message = f"Error: {str(e)}"
        finally:
            self.exporting = False

    @rx.event
    def generate_postulantes_pdf(self):
        """Generate PDF report for postulants."""
        self.exporting = True
        self.export_message = "Generando reporte PDF..."

        try:
            postulantes = cargar_postulantes()
            filepath = generate_postulantes_report(postulantes)
            self.last_export_path = filepath
            self.export_message = f"Reporte generado: {filepath.split('/')[-1]}"

            # Trigger download
            return rx.download(url=filepath, filename=filepath.split("/")[-1])

        except Exception as e:
            self.export_message = f"Error: {str(e)}"
        finally:
            self.exporting = False

    @rx.event
    def generate_resultados_pdf(self):
        """Generate PDF report for exam results."""
        self.exporting = True
        self.export_message = "Generando reporte de resultados..."

        try:
            # Import resultados from state
            from sistema_admisi_n_unas.states.resultados_state import ResultadosState

            # Get results data
            resultados = ResultadosState.resultados if hasattr(ResultadosState, 'resultados') else []

            if not resultados:
                # Load from CSV
                from sistema_admisi_n_unas.utils.csv_loader import cargar_resultados
                resultados = cargar_resultados()

            filepath = generate_resultados_report(resultados)
            self.last_export_path = filepath
            self.export_message = f"Reporte generado: {filepath.split('/')[-1]}"

            return rx.download(url=filepath, filename=filepath.split("/")[-1])

        except Exception as e:
            self.export_message = f"Error: {str(e)}"
        finally:
            self.exporting = False

    @rx.event
    def generate_dashboard_pdf(self, stats: Dict[str, Any]):
        """Generate PDF report for dashboard statistics."""
        self.exporting = True
        self.export_message = "Generando estadísticas..."

        try:
            filepath = generate_stats_report(stats)
            self.last_export_path = filepath
            self.export_message = f"Reporte generado: {filepath.split('/')[-1]}"

            return rx.download(url=filepath, filename=filepath.split("/")[-1])

        except Exception as e:
            self.export_message = f"Error: {str(e)}"
        finally:
            self.exporting = False

    @rx.event
    def export_filtered_csv(self, postulantes: List[Dict], filters: Dict = None):
        """Export filtered postulants to CSV."""
        self.exporting = True
        self.export_message = "Exportando datos filtrados..."

        try:
            if not postulantes:
                self.exporting = False
                self.export_message = "No hay datos para exportar"
                return

            filepath = export_to_csv(postulantes, "postulantes_filtrados")
            self.last_export_path = filepath
            self.export_message = f"Exportación exitosa"

            return rx.download(url=filepath, filename=filepath.split("/")[-1])

        except Exception as e:
            self.export_message = f"Error: {str(e)}"
        finally:
            self.exporting = False