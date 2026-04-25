def generate_conclusion(
    waiting,
    response,
    fairness,
    short_job,
    quantum
):

    return (
        "Final Conclusion:\n"
        + waiting + "\n"
        + response + "\n"
        + fairness + "\n"
        + short_job + "\n"
        + quantum
    )