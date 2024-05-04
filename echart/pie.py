def options(series_data:list): 
    return {
        "tooltip": {"trigger": "item"},
        "legend": {
            "orient": "vertical",
            "left": "left",
            "textStyle": {"color": "gray"},
        },
        "series": series_data,
    }
