from pel.tasks import Shell


class first(Shell):
    cmd = "echo first"


class second(Shell):
    cmd = "echo second"
    src = "src1"


class third(Shell):
    cmd = "echo third"
    src = "src2"
    target = "outputs/output-file-1.txt"


class fourth(Shell):
    cmd = "echo fourth"
    src = [
        "src1",
        "src2",
        "src3",
    ]
    target = [
        "outputs/output-file-1.txt",
        "outputs/output-file-2.txt",
    ]