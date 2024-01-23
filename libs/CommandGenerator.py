import re

RE_BRACKET_NEEDS_LSTRIP = re.compile(r'\s+([(\[{])')
RE_BRACKET_NEEDS_RSTRIP = re.compile(r'([)\]}])\s+')
RE_RELATION = re.compile(r'\s*([<>:!=]=|=|<|>)\s*')
RE_FORMULA_AN = re.compile(r'^a\s*\(\s*n\s*\)\s*=\s*', flags=re.IGNORECASE)
RE_FORMULA_GF = re.compile(r'^g\.f\.\s*:?\s*', flags=re.IGNORECASE)
RE_FORMULA_EGF = re.compile(r'^e\.g\.f\.\s*:?\s*', flags=re.IGNORECASE)
RE_FORMULA_DGF = re.compile(
    r'^d(?:\.|irichlet)\s*g\.f\.\s*:?\s*', flags=re.IGNORECASE)
RE_AUTHOR_DATE_IN_THE_END = re.compile(
    r'-\s*_(?P<author>(?:[A-Za-z.\-]+?\s*)+?)_,?\s*(?P<date>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d+)')


class CommandGenerator:
    def __init__(self, _id: str, seq_detail: dict) -> None:
        if int(_id.removeprefix('A')) != seq_detail['number']:
            raise RuntimeError(
                f"ID match error. ID input = {_id}, ID in seq_detail = {seq_detail['number']}")

        self.id: str = _id
        self.offset: str = seq_detail.get('offset', '')
        self.name: str = seq_detail.get('name', '')

        __data: list[int] = [int(i) for i in seq_detail['data'].split(',')]
        self.cnt0: int = __data.index(
            next(filter(lambda x: x > 0, __data), __data[-1]))
        if __data[self.cnt0] == 0:
            self.cnt0 = len(__data)
        __data = __data[self.cnt0:]
        if __data:
            self.cnt1: int = __data.index(
                next(filter(lambda x: x > 1, __data), __data[-1]))
            if __data[self.cnt1] == 1:
                self.cnt1 = len(__data)
            self.data: list[int] = __data[self.cnt1:]
        else:
            self.cnt1: int = 0
            self.data: list[int] = []

        self.formula: list[str] = []
        self.formula_an: list[str] = []
        self.formula_gf: list[str] = []
        self.formula_egf: list[str] = []
        self.formula_dgf: list[str] = []

        for now_formula in [i.strip() for i in seq_detail['formula']]:
            now_formula = re.sub(RE_AUTHOR_DATE_IN_THE_END, '', now_formula)
            if re.search(RE_FORMULA_AN, now_formula):
                self.formula_an.append(re.sub(RE_FORMULA_AN, '', now_formula))
                continue
            if re.search(RE_FORMULA_GF, now_formula):
                self.formula_gf.append(re.sub(RE_FORMULA_GF, '', now_formula))
                continue
            if re.search(RE_FORMULA_EGF, now_formula):
                self.formula_egf.append(
                    re.sub(RE_FORMULA_EGF, '', now_formula))
                continue
            if re.search(RE_FORMULA_DGF, now_formula):
                self.formula_dgf.append(
                    re.sub(RE_FORMULA_DGF, '', now_formula))
                continue
            self.formula.append(now_formula)

    def __lt__(self, rhs) -> bool:
        if self.data != rhs.data:
            return self.data < rhs.data
        if self.cnt1 != rhs.cnt1:
            return self.cnt1 < rhs.cnt1
        if self.cnt0 != rhs.cnt0:
            return self.cnt0 < rhs.cnt0
        return self.id < rhs.id

    @staticmethod
    def __plain_text(formula: str) -> str:
        def __f(__s: str) -> str:
            return ''.join(rf'\{ch}' if ch in r'#$%{}_&' else r'\;' if ch == ' ' else ch for ch in __s.strip())

        formula = re.sub(RE_BRACKET_NEEDS_LSTRIP,
                         lambda x: x.group(1), formula)
        formula = re.sub(RE_BRACKET_NEEDS_RSTRIP,
                         lambda x: x.group(1), formula)
        formula = re.sub(RE_RELATION, lambda x: f' {x.group(1)} ', formula)

        return ' '.join(filter(lambda x: x, r' \^{} '.join(r' \~{} '.join(
            r' \(\backslash\) '.join(rf' \seqsplit{{{__f(part3)}}} ' for part3 in part2.split('\\')) for part2 in
            part1.split('~')) for part1 in formula.split('^')).split()))

    def __seq_data(self) -> str:
        result: str = rf"\{{{str(self.cnt0) if self.cnt0 else ''},{str(self.cnt1) if self.cnt1 else ''}\}}" if self.cnt0 or self.cnt1 else ''
        __data: list[int] = self.data
        __cnt: int = 0
        while __data:
            if len(__data) < 2 or __data[0] != __data[1]:
                result += f',{__data[0]}'
                __data = __data[1:]
                __cnt += 1
                if __cnt >= 10:
                    break

                if __data:
                    continue
                else:
                    break

            __idx: int = __data.index(
                next(filter(lambda x: x != __data[0], __data), __data[-1]))
            if not __idx:
                __idx = len(__data)

            result += f',{__data[0]}:{__idx}' if __idx > 1 else f',{__data[0]}'
            __data = __data[__idx:]
            __cnt += 1
            if __cnt >= 10:
                break

        return rf"\seqsplit{{{result.strip(',')}}}"

    def str_tex(self) -> str:
        return ' '.join([rf'\textbf{{{self.id}}}\index{{{self.id}}}' + (rf'\(\langle {self.offset}\rangle\)' if self.offset else ''),
                         rf'{{\ttfamily {self.__seq_data()}}}',
                         rf'\textit{{{self.__plain_text(self.name)}}}'] +
                        [rf'\(\ddagger\) {self.__plain_text(i)}' for i in self.formula_an] +
                        [rf'\(\flat\) {self.__plain_text(i)}' for i in self.formula_gf] +
                        [rf'\(\natural\) {self.__plain_text(i)}' for i in self.formula_egf] +
                        [rf'\(\diamond\) {self.__plain_text(i)}' for i in self.formula_dgf] +
                        [rf'\(\dagger\) {self.__plain_text(i)}' for i in self.formula] +
                        [rf'\href{{\oeis {self.id}/}}{{\P}}'])
