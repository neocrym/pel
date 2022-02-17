class first(Shell):
    cmd = "echo first"


class other_first(Shell):
    cmd = "echo has the same priority as first"


class second(Shell):
    needs = [first]
    cmd = "echo second"


class third(Shell):
    needs = [first, second]
    cmd = "echo third"
