def options(xAxis_data:list,series_data:list): 
    return {
        # "tooltip": {
        #     "trigger": "axis",
        #     "axisPointer": {"type": "cross", "crossStyle": {"color": "#6a7985"}},
        # },
        "textStyle": {"color": "gray"},
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
            "data":xAxis_data,
        },
        "yAxis": {"type": "value"},
        "series": series_data,
    }
