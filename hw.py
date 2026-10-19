import csv
from collections import defaultdict


INPUT_FILE  = 'Corp_Summary.csv'
OUTPUT_FILE = 'report.csv'


def read_file(path):
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        return list(reader)


def report_hierarchy(rows):
    # print(rows[0])
    data = rows[1:]
    deps_com = defaultdict(set)
    for s in data:
        deps_com[s[1]].add(s[2])

    for i,dep in enumerate(sorted(deps_com), start=1):
        print(f'{i}. {dep}: ')
        for j,team in enumerate(sorted(deps_com[dep]), start=1):
            print(f'{j}) {team}')
        print()



def report_summary(rows):
    data = rows[1:]
    stat_deps = defaultdict(list)
    for s in data:
        dep = s[1]
        sal = int(s[5])
        stat_deps[dep].append(sal)

    for i,dep in enumerate(sorted(stat_deps), start=1):
        sals = stat_deps[dep]
        print(f'{i}. {dep}:\n'
              f'1) people = {len(sals)}\n'
              f'2) min = {min(sals)}\n'
              f'3) max = {max(sals)}\n'
              f'4) avg = {sum(sals) / len(sals):.2f}\n\n')


def report_summary_csv(rows):
    data = rows[1:]
    stat_deps = defaultdict(list)
    for s in data:
        dep = s[1]
        sal = int(s[5])
        stat_deps[dep].append(sal)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Департамент", "people", "min", "max", "avg"])
        for dep in sorted(stat_deps):
            sals = stat_deps[dep]
            n = len(sals)
            writer.writerow([dep, n, min(sals), max(sals),
                             round(sum(sals)/n, 2)])
    print(f"Done, recorded in {OUTPUT_FILE}")


def main(variant):
    rows = read_file(INPUT_FILE)
    if variant == 1:
        report_hierarchy(rows)
    elif variant == 2:
        report_summary(rows)
    elif variant == 3:
        report_summary_csv(rows)
    else:
        print('')

if __name__ == '__main__':
    for i in range(1, 4):
        main(i)

