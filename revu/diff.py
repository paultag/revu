

def line_to_file(fd, index):
    index = index - 1

    lines = list(fd.readlines())  # This would otherwise be implicit with
    # reversed(), writing a reverse file iterator would be neato.

    def readup(lines, index):
        for i in range(index, -1, -1):
            yield (i, lines[i])

    count = 0
    diff_count = -1

    _return_lines = []
    for (i, line) in readup(lines, index):
        if line.startswith("@@"):
            diff_count = count

        if line.startswith("+++ "):
            _, path = (x.strip() for x in line.split(" ", 1))
            return (path, diff_count, list(reversed(_return_lines)))

        _return_lines.append(line)
        count += 1
    else:
        raise ValueError("Badd diff line!")
