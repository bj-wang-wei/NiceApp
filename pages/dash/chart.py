from nicegui import ui, events


async def show():
    with ui.grid(columns=3).classes("w-full"):
        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {"textStyle": {"color": "gray"}},
                    "series": [
                        {
                            "type": "pie",
                            "name": "Access From",
                            "radius": ["40%", "70%"],
                            "avoidLabelOverlap": False,
                            "itemStyle": {
                                "borderRadius": 10,
                                "borderColor": "#fff",
                                "borderWidth": 2,
                            },
                            "label": {"show": False, "position": "center"},
                            "emphasis": {
                                "label": {
                                    "show": True,
                                    "fontSize": 15,
                                    "fontWeight": "bold",
                                }
                            },
                            "labelLine": {"show": False},
                            "data": [
                                {"value": 1048, "name": "Search Engine"},
                                {"value": 735, "name": "Direct"},
                                {"value": 580, "name": "Email"},
                                {"value": 484, "name": "Union Ads"},
                                {"value": 300, "name": "Video Ads"},
                            ],
                        },
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {
                        "textStyle": {"color": "gray"},
                        "data": [
                            "Email",
                            "Union Ads",
                            "Video Ads",
                            "Direct",
                            "Search Engine",
                        ],
                    },
                    "grid": {
                        "left": "3%",
                        "right": "4%",
                        "bottom": "3%",
                        "containLabel": True,
                    },
                    "xAxis": {
                        "type": "category",
                        "boundaryGap": False,
                        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    },
                    "yAxis": {"type": "value"},
                    "series": [
                        {
                            "name": "Email",
                            "type": "line",
                            "stack": "Total",
                            "data": [120, 132, 101, 134, 90, 230, 210],
                        },
                        {
                            "name": "Union Ads",
                            "type": "line",
                            "stack": "Total",
                            "data": [220, 182, 191, 234, 290, 330, 310],
                        },
                        {
                            "name": "Video Ads",
                            "type": "line",
                            "stack": "Total",
                            "data": [150, 232, 201, 154, 190, 330, 410],
                        },
                        {
                            "name": "Direct",
                            "type": "line",
                            "stack": "Total",
                            "data": [320, 332, 301, 334, 390, 330, 320],
                        },
                        {
                            "name": "Search Engine",
                            "type": "line",
                            "stack": "Total",
                            "data": [820, 932, 901, 934, 1290, 1330, 1320],
                        },
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {
                        "textStyle": {"color": "gray"},
                        "data": ["Evaporation", "Precipitation", "Temperature"],
                    },
                    "xAxis": [
                        {
                            "type": "category",
                            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                            "axisPointer": {"type": "shadow"},
                        }
                    ],
                    "yAxis": [
                        {
                            "type": "value",
                            "name": "Precipitation",
                            "min": 0,
                            "max": 250,
                            "interval": 50,
                            "axisLabel": {"formatter": "{value} ml"},
                        },
                        {
                            "type": "value",
                            "name": "Temperature",
                            "min": 0,
                            "max": 25,
                            "interval": 5,
                            "axisLabel": {"formatter": "{value} °C"},
                        },
                    ],
                    "series": [
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
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "xAxis": {"type": "value"},
                    "yAxis": {"type": "category", "data": ["A", "B"], "inverse": True},
                    "legend": {"textStyle": {"color": "gray"}},
                    "series": [
                        {"type": "bar", "name": "Alpha", "data": [0.1, 0.2]},
                        {"type": "bar", "name": "Beta", "data": [0.3, 0.4]},
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {
                        "textStyle": {"color": "gray"},
                    },
                    "grid": {
                        "left": "3%",
                        "right": "4%",
                        "bottom": "3%",
                        "containLabel": True,
                    },
                    "xAxis": {
                        "type": "category",
                        "splitLine": {"show": False},
                        "data": [
                            "Total",
                            "Rent",
                            "Utilities",
                            "Transportation",
                            "Meals",
                            "Other",
                        ],
                    },
                    "yAxis": {"type": "value"},
                    "series": [
                        {
                            "name": "Placeholder",
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
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {
                        "textStyle": {"color": "gray"},
                        "data": ["A", "B", "C"],
                        "orient": "vertical",
                        "left": "left",
                    },
                    "angleAxis": {},
                    "radiusAxis": {
                        "type": "category",
                        "data": ["Mon", "Tue", "Wed", "Thu"],
                        "z": 10,
                    },
                    "polar": {},
                    "series": [
                        {
                            "type": "bar",
                            "data": [1, 2, 3, 4],
                            "coordinateSystem": "polar",
                            "name": "A",
                            "stack": "a",
                            "emphasis": {"focus": "series"},
                        },
                        {
                            "type": "bar",
                            "data": [2, 4, 6, 8],
                            "coordinateSystem": "polar",
                            "name": "B",
                            "stack": "a",
                            "emphasis": {"focus": "series"},
                        },
                        {
                            "type": "bar",
                            "data": [1, 2, 3, 4],
                            "coordinateSystem": "polar",
                            "name": "C",
                            "stack": "a",
                            "emphasis": {"focus": "series"},
                        },
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {"textStyle": {"color": "gray"}},
                    "xAxis": {},
                    "yAxis": {},
                    "series": [
                        {
                            "symbolSize": 20,
                            "data": [
                                [10.0, 8.04],
                                [8.07, 6.95],
                                [13.0, 7.58],
                                [9.05, 8.81],
                                [11.0, 8.33],
                                [14.0, 7.66],
                                [13.4, 6.81],
                                [10.0, 6.33],
                                [14.0, 8.96],
                                [12.5, 6.82],
                                [9.15, 7.2],
                                [11.5, 7.2],
                                [3.03, 4.23],
                                [12.2, 7.83],
                                [2.02, 4.47],
                                [1.05, 3.33],
                                [4.05, 4.96],
                                [6.03, 7.24],
                                [12.0, 6.26],
                                [12.0, 8.84],
                                [7.08, 5.82],
                                [5.02, 5.68],
                            ],
                            "type": "scatter",
                        }
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "legend": {
                        "textStyle": {"color": "gray"},
                        "orient": "vertical",
                        "left": "left",
                        "data": ["Prod A", "Prod B", "Prod C", "Prod D", "Prod E"],
                    },
                    "series": [
                        {
                            "name": "Funnel",
                            "type": "funnel",
                            "width": "40%",
                            "height": "45%",
                            "left": "5%",
                            "top": "50%",
                            "funnelAlign": "right",
                            "data": [
                                {"value": 60, "name": "Prod C"},
                                {"value": 30, "name": "Prod D"},
                                {"value": 10, "name": "Prod E"},
                                {"value": 80, "name": "Prod B"},
                                {"value": 100, "name": "Prod A"},
                            ],
                        },
                        {
                            "name": "Pyramid",
                            "type": "funnel",
                            "width": "40%",
                            "height": "45%",
                            "left": "5%",
                            "top": "5%",
                            "sort": "ascending",
                            "funnelAlign": "right",
                            "data": [
                                {"value": 60, "name": "Prod C"},
                                {"value": 30, "name": "Prod D"},
                                {"value": 10, "name": "Prod E"},
                                {"value": 80, "name": "Prod B"},
                                {"value": 100, "name": "Prod A"},
                            ],
                        },
                        {
                            "name": "Funnel",
                            "type": "funnel",
                            "width": "40%",
                            "height": "45%",
                            "left": "55%",
                            "top": "5%",
                            "funnelAlign": "left",
                            "data": [
                                {"value": 60, "name": "Prod C"},
                                {"value": 30, "name": "Prod D"},
                                {"value": 10, "name": "Prod E"},
                                {"value": 80, "name": "Prod B"},
                                {"value": 100, "name": "Prod A"},
                            ],
                        },
                        {
                            "name": "Pyramid",
                            "type": "funnel",
                            "width": "40%",
                            "height": "45%",
                            "left": "55%",
                            "top": "50%",
                            "sort": "ascending",
                            "funnelAlign": "left",
                            "data": [
                                {"value": 60, "name": "Prod C"},
                                {"value": 30, "name": "Prod D"},
                                {"value": 10, "name": "Prod E"},
                                {"value": 80, "name": "Prod B"},
                                {"value": 100, "name": "Prod A"},
                            ],
                        },
                    ],
                }
            )

        with ui.card().classes("items-center h-[calc(100vh/3-50px)] shadow-0 border"):
            ui.echart(
                {
                    "xAxis": {
                        "data": ["2017-10-24", "2017-10-25", "2017-10-26", "2017-10-27"]
                    },
                    "yAxis": {},
                    "series": [
                        {
                            "type": "candlestick",
                            "data": [
                                [20, 34, 10, 38],
                                [40, 35, 30, 50],
                                [31, 38, 33, 44],
                                [38, 15, 5, 42],
                            ],
                        }
                    ],
                }
            )
