def options(xAxis_data:list,series_data:list):   
    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        },
        "textStyle": {"color": "gray"},
        "darkMode": True,
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
            "boundaryGap": True,
            "data": xAxis_data,
        },
        "yAxis": {"type": "value"},
        "series": series_data,
    }
