def print_report(name, rr, srtf, conclusion):
    print(f"\n=== {name} ===")

    print("\nRR:")
    print(rr)

    print("\nSRTF:")
    print(srtf)

    print("\nConclusion:")
    for c in conclusion:
        print("-", c)