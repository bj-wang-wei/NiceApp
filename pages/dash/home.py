from nicegui import ui
import echart.line as line
import echart.bar as bar
import echart.waterfall as waterfall
import echart.pie as pie


async def show():
    with ui.grid(columns=18).classes("w-full h-full"):
        with ui.card().classes(
            "items-center col-span-4 row-span-2 bg-gradient-to-r from-violet-500 to-fuchsia-500 shadow-0 border"
        ):
            ui.label("Avg First Replay Time").classes("text-xl")
            with ui.row():
                ui.label("30").classes("text-3xl")
                ui.label("h").classes("text-xl mt-2")
                ui.label("15").classes("text-3xl")
                ui.label("min").classes("text-xl mt-2")

        with ui.card().classes(
            "items-center col-span-4 row-span-2 bg-gradient-to-r from-sky-500 to-indigo-500  shadow-0 border"
        ):
            ui.label("Avg First Replay Time").classes("text-xl")
            with ui.row():
                ui.label("30").classes("text-3xl")
                ui.label("h").classes("text-xl mt-2")
                ui.label("15").classes("text-3xl")
                ui.label("min").classes("text-xl mt-2")

        with ui.column().classes("row-span-2 col-span-4 "):
            with ui.card().classes(
                "items-center w-full h-12 bg-gradient-to-r from-green-600 to-teal-600 shadow-0 border"
            ):
                with ui.row().classes("w-11/12"):
                    ui.icon("textsms").classes("text-2xl")
                    ui.label("Messages").classes("-mt-1 text-xl")
                    ui.space()
                    with ui.badge(color="orange-800").classes("-mt-2"):
                        ui.label("20%").classes("text-lg")
            with ui.card().classes(
                "items-center w-full h-12 bg-gradient-to-r from-green-600 to-teal-600 shadow-0 border"
            ):
                with ui.row().classes("w-11/12"):
                    ui.icon("email").classes("text-2xl")
                    ui.label("Emails").classes("-mt-1 text-xl")
                    ui.space()
                    with ui.badge(color="teal-800").classes("-mt-2"):
                        ui.label("+33%").classes("text-lg")

        with ui.card().classes(
            "items-center col-span-6 row-span-3 h-96  shadow-0 border"
        ):
            series_data = [
                {
                    "type": "line",
                    "name": "Email",
                    "data": [120, 132, 101, 134, 90, 230, 210],
                },
                {
                    "type": "line",
                    "name": "Union Ads",
                    "data": [220, 182, 191, 234, 290, 330, 310],
                },
                {
                    "type": "line",
                    "name": "Video Ads",
                    "data": [150, 232, 201, 154, 190, 330, 410],
                },
                {
                    "type": "line",
                    "name": "Direct",
                    "data": [320, 332, 301, 334, 390, 330, 320],
                },
                {
                    "type": "line",
                    "name": "Search Engine",
                    "data": [820, 932, 901, 934, 1290, 1330, 1320],
                },
            ]
            xAxis_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            ui.echart(
                options=line.options(
                    xAxis_data=xAxis_data,
                    series_data=series_data,
                )
            ).classes("h-full")

        with ui.card().classes(
            "items-center col-span-12 row-span-4 h-[400px] shadow-0 border"
        ):
            series_data = [
                {
                    "type": "bar",
                    "name": "Evaporation",
                    "data": [
                        2.0,
                        4.9,
                        7.0,
                        23.2,
                        25.6,
                        76.7,
                        135.6,
                        162.2,
                        32.6,
                        20.0,
                        6.4,
                        3.3,
                    ],
                },
                {
                    "type": "bar",
                    "name": "Precipitation",
                    "data": [
                        2.6,
                        5.9,
                        9.0,
                        26.4,
                        28.7,
                        70.7,
                        175.6,
                        182.2,
                        48.7,
                        18.8,
                        6.0,
                        2.3,
                    ],
                },
                {
                    "type": "line",
                    "name": "Temperature",
                    "yAxisIndex": 1,
                    "data": [
                        2.0,
                        2.2,
                        3.3,
                        4.5,
                        6.3,
                        10.2,
                        20.3,
                        23.4,
                        23.0,
                        16.5,
                        12.0,
                        6.2,
                    ],
                },
            ]
            xAxis_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            yAxis_name = ["Precipitation", "Temperature"]
            ui.echart(
                options=bar.options(
                    xAxis_data=xAxis_data,
                    yAxis_name=yAxis_name,
                    series_data=series_data,
                )
            ).classes("h-full")

        with ui.card().classes("items-center col-span-6 row-span-4 shadow-0 border"):
            xAxis_data = [
                "Total",
                "Rent",
                "Utilities",
                "Transportation",
                "Meals",
                "Other",
            ]
            series_data = [
                {
                    "name": "",
                    "type": "bar",
                    "stack": "Total",
                    "itemStyle": {
                        "borderColor": "transparent",
                        "color": "transparent",
                    },
                    "emphasis": {
                        "itemStyle": {
                            "borderColor": "transparent",
                            "color": "transparent",
                        }
                    },
                    "data": [0, 1700, 1400, 1200, 300, 0],
                },
                {
                    "name": "Life Cost",
                    "type": "bar",
                    "stack": "Total",
                    "label": {"show": True, "position": "inside"},
                    "data": [2900, 1200, 300, 200, 900, 300],
                },
            ]
            ui.echart(
                options=waterfall.options(
                    xAxis_data=xAxis_data, series_data=series_data
                )
            ).classes("h-full")

        with ui.card().classes("items-center col-span-6 h-[310px] shadow-0 border"):
            series_data = [
                {
                    "name": "Access From",
                    "type": "pie",
                    "radius": "50%",
                    "data": [
                        {"value": 1048, "name": "Search Engine"},
                        {"value": 735, "name": "Direct"},
                        {"value": 580, "name": "Email"},
                        {"value": 484, "name": "Union Ads"},
                        {"value": 300, "name": "Video Ads"},
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                    "label": {"show": False, "position": "outside", "color": "grey"},
                }
            ]

            ui.echart(options=pie.options(series_data=series_data)).classes("h-full")

        with ui.card().classes("items-center col-span-6 h-[310px] shadow-0 border"):
            series_data = [
                {
                    "name": "Access From",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "label": {"show": False, "position": "inside", "color": "grey"},
                    "data": [
                        {"value": 1048, "name": "Search Engine"},
                        {"value": 735, "name": "Direct"},
                        {"value": 580, "name": "Email"},
                        {"value": 484, "name": "Union Ads"},
                        {"value": 300, "name": "Video Ads"},
                    ],
                }
            ]

            ui.echart(options=pie.options(series_data=series_data)).classes("h-full")
