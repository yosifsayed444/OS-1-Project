def generate_conclusion(rr, srtf):
    result = []

    if rr["avg_wt"] < srtf["avg_wt"]:
        result.append("RR better in waiting time")
    else:
        result.append("SRTF better in waiting time")

    if rr["avg_rt"] < srtf["avg_rt"]:
        result.append("RR better in response time")
    else:
        result.append("SRTF better in response time")

    result.append("RR is fairer due to time slicing")
    result.append("SRTF is more efficient for short jobs")

    return result