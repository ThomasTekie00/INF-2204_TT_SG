import statistics

file_names = ["run_1.txt", "run_2.txt", "run_3.txt", "run_4.txt", "run_5.txt"]
data = []

for idx, fn in enumerate(file_names):
    with open(fn, "r") as f:
        data.append([])
        raw = f.read()
        file_lines = raw.splitlines()[12::]
        header = file_lines[0]
        value_index = header.index("hit")
        d = [l[value_index::].split() for l in file_lines[2::]]
        for fw in d:
            data[idx] += fw
        for i, entry in enumerate(data[idx]):
            data[idx][i] = float(entry.replace("%", ""))

output = []
for idx in range(len(data[0])):
    output.append(round(statistics.stdev([data[x][idx] for x in range(len(file_names))]), 3))


out_string = ""
for i in range(len(output)):
    if i > 0 and i % 3 == 0:
        out_string += "\n"

    op = str(output[i])
    op += (" " * (10 - len(op)))
    out_string += f"{op}"

print(out_string)