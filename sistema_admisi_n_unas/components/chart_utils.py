import reflex as rx

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 2px 6px rgba(0, 0, 0, 0.05)",
        "fontFamily": "Inter, sans-serif",
        "fontSize": "0.875rem",
        "fontWeight": "500",
        "padding": "0.375rem 0.625rem",
    },
    "item_style": {
        "display": "flex",
        "paddingTop": "2px",
    },
    "label_style": {
        "color": "#003366",
        "fontWeight": "600",
        "marginBottom": "4px",
    },
    "separator": ": ",
}


def chart_legend(color: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            class_name="w-3 h-3 inline-block mr-2 rounded-full",
            style={"backgroundColor": color},
        ),
        rx.el.span(
            label,
            class_name="text-sm font-medium text-gray-600",
        ),
        class_name="flex items-center",
    )