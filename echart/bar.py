def options(xAxis_data:list,yAxis_name:list,series_data:list): 
    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "crossStyle": {"color": "#6a7985"}},
        },
        "textStyle": {"color": "gray"},
        "legend": {
            "textStyle": {"color": "gray"},
        },
        "xAxis": [
            {
                "type": "category",
                "data": xAxis_data,
                "axisPointer": {"type": "shadow"},
            }
        ],
        "yAxis": [
            {
                "type": "value",
                "name": yAxis_name[0],
                "min": 0,
                "max": 250,
                "interval": 50,
                "axisLabel": {"formatter": "{value} ml"},
            },
            {
                "type": "value",
                "name": yAxis_name[1],
                "min": 0,
                "max": 25,
                "interval": 5,
                "axisLabel": {"formatter": "{value} °C"},
            },
        ],
        "series": series_data,
    }
