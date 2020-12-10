from __future__ import annotations

from functools import cached_property
from math import ceil, floor, sqrt
from numbers import Real
from operator import add, mul, sub
from sys import exit
from typing import Any, Callable, Dict, List, NoReturn, Optional, Tuple

Element = float
MatrixElements = List[Element]
MatrixParameters = Tuple[int, int, MatrixElements]
Choice = Tuple[str, Callable[..., Any]]
MenuOptions = Dict[str, Choice]

__all__ = ['Matrix', 'Processor']


class Matrix:
    """A class to represent a matrix as immutable object with implementation of basic operations.

    Todo:
        * BUG: __hash__ return the same result for different objects
          with the same parameters. Move initialization in __new__,
          make instances unique.
        * BUG: __row_count, __column_count should be positional_only_parameters
          see PEP-457 and PEP 570 for solution. Now, it only possible to get
          access to these parameters inside __init__ using
          _Matrix__row_count and _Matrix__column_count.
        * Add iterators rows and columns (for using in transpose)
    
    Note:
        New in version 3.8. @functools.cached_property requires
        that specify __slots__ with including __dict__ as one
        of the defined slots
    """

    __slots__ = ['__dict__', 'row_count', 'column_count', 'elements']

    def __init__(
        self,
        __row_count: Optional[int] = None,
        __column_count: Optional[int] = None,
        *,
        elements: Optional[MatrixElements] = None,
        alias: Optional[str] = '',
    ) -> None:
        """The constructor for Matrix class.

        If at least one variable from `__row_count`, `__column_count`
        or `elements` is missing, CLI will be launched to get
        all parameters from user.

        Args:
            __row_count: number of rows.
            __column_count: number of columns.
            elements: elements of matrix as a list of numbers.
            alias: matrix alias used on CLI when getting other matrix
                parameters from user.

        Raises:
            ValueError: if number of elements calculated as
                a multiplication `__row_count` and `__column_count` is
                not equal to the number of elements in the variable
                `elements`.

        """
        if __row_count is None or __column_count is None or elements is None:
            (
                __row_count,
                __column_count,
                elements,
            ) = self._read_matrix_parameters_from_input(alias)
        if len(elements) != (__row_count * __column_count):
            raise ValueError
        self.row_count: int
        self.column_count: int
        self.elements: MatrixElements
        super(Matrix, self).__setattr__('row_count', __row_count)
        super(Matrix, self).__setattr__('column_count', __column_count)
        super(Matrix, self).__setattr__('elements', elements)

    def __setattr__(self, key: str, value: Any) -> NoReturn:
        raise AttributeError(f"'{type(self)}' is immutable. You cannot assign to {key}")

    def __str__(self) -> str:
        elements_str: List[str] = list(map(self._round_and_str, self.elements))
        elements_len: List[int] = list(map(len, elements_str))
        columns_width: List[int] = [
            max(elements_len[c :: self.column_count]) for c in range(self.column_count)
        ]
        result: List[str] = list()
        for r in range(self.row_count):
            result.append(
                ' '.join(
                    f"{elements_str[r * self.column_count + c]: >{columns_width[c]}}"
                    for c in range(self.column_count)
                )
            )
        return '\n'.join(result)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(row_count='{self.row_count}'"
            f", column_count='{self.column_count}'"
            f", elements='{self.elements}')"
        )

    def __hash__(self) -> int:
        return hash((self.row_count, self.column_count, self.elements))

    def __add__(self, other: Any) -> Matrix:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        if self.row_count != other.row_count or self.column_count != other.column_count:
            raise ValueError
        elements: MatrixElements
        elements = list(
            self.round(add(*pair)) for pair in zip(self.elements, other.elements)
        )
        return Matrix(self.row_count, self.column_count, elements=elements)

    def __sub__(self, other: Any) -> Matrix:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        if self.row_count != other.row_count or self.column_count != other.column_count:
            raise ValueError
        elements: MatrixElements
        elements = list(
            self.round(sub(*pair)) for pair in zip(self.elements, other.elements)
        )
        return Matrix(self.row_count, self.column_count, elements=elements)

    def __mul__(self, other: Any) -> Matrix:
        if isinstance(other, Real):
            return Matrix(
                self.row_count,
                self.column_count,
                elements=list(e * other for e in self.elements),
            )
        elif isinstance(other, type(self)):
            if self.column_count != other.row_count:
                raise ValueError
            elements = list()
            self_row: MatrixElements
            other_column: MatrixElements
            for r in range(self.row_count):
                for c in range(other.column_count):
                    elements.append(
                        sum(
                            self.round(mul(*pair))
                            for pair in zip(self.row(r), other.column(c))
                        )
                    )
            return Matrix(self.row_count, other.column_count, elements=elements)
        else:
            raise NotImplementedError

    def __truediv__(self, other: Any) -> Matrix:
        if not isinstance(other, Real):
            raise NotImplementedError
        return Matrix(
            self.row_count,
            self.column_count,
            elements=list(self.round(e / other) for e in self.elements),
        )

    @staticmethod
    def round(x: float) -> float:
        """Save number as `int` if fractional part is zero

        Requirement of Stage 7
        """
        return int(x) if x % 1 < 0.000001 else x

    @staticmethod
    def _round_and_str(x: Any, scale: int = 2) -> str:
        """Convert element in accordance with requirements of project (Stage 7)"""
        multitude: int = 10 ** scale
        if isinstance(x, float):
            if x > 0:
                return str(floor(round(x, scale + 1) * multitude) / multitude)
            else:
                return str(ceil(round(x, scale + 1) * multitude) / multitude)
        return str(x)

    @staticmethod
    def _read_matrix_parameters_from_input(
        alias: Optional[str] = '',
    ) -> MatrixParameters:
        print(
            "Enter size of", f" {alias} " if alias else " ", "matrix:", sep='', end=' '
        )
        row_count, column_count = map(int, input().split(' ', 1))
        elements: MatrixElements = list()
        row: MatrixElements
        print("Enter", f" {alias} " if alias else " ", "matrix:", sep='')
        for _ in range(row_count):
            row = [float(x) if '.' in x else int(x) for x in input().split()]
            if len(row) != column_count:
                raise ValueError
            elements.extend(row)
        return row_count, column_count, elements

    @staticmethod
    def _submatrix(*, square_matrix: MatrixElements, i: int, j: int) -> MatrixElements:
        """Return square submatrix formed by deleting the `i`th row and `j`th column.

        Note:
            All arguments are keyword-only arguments.

            `i` and `j` are 0-based indexes that less than `size` of matrix

        Args:
            square_matrix: square matrix as a list of numbers.
            i: row number.
            j: column number.

        Returns:
            The square submatrix as a list of numbers.

        Raises:
            IndexError: if `i` or `j` less than zero or
                `i` or `j` greater than or equal to `size`

        """
        size: int = int(sqrt(len(square_matrix)))
        if 0 <= i < size and 0 <= j < size:
            elements: MatrixElements = list()
            for r in range(size):
                if r != i:
                    row = square_matrix[r * size : r * size + size :]
                    # skip element in `j` column
                    elements.extend(row[:j] + row[j + 1 :])
            return elements
        else:
            raise IndexError

    @classmethod
    def cofactor(cls, *, square_matrix: MatrixElements, i: int, j: int) -> float:
        return (-1) ** (i + j) * cls._determinant(
            square_matrix=cls._submatrix(square_matrix=square_matrix, i=i, j=j)
        )

    @cached_property
    def inverse(self) -> Matrix:
        if self.determinant:
            return self.adjoint().transpose() / self.determinant
        else:
            raise AttributeError

    def adjoint(self) -> Matrix:
        elements: MatrixElements = list(
            self.cofactor(square_matrix=self.elements, i=r, j=c)
            for r in range(self.row_count)
            for c in range(self.column_count)
        )
        return Matrix(self.row_count, self.column_count, elements=elements)

    @classmethod
    def _determinant(cls, *, square_matrix: MatrixElements) -> float:
        """Return determinant that computed from a square matrix using the Laplace expansion.

        Todo:
            * BUG: if matrix(1, 1)
        Args:
            square_matrix: square matrix as a list of numbers.
                It's keyword-only argument.

        Returns:
            The scalar value.

        """
        size: int = int(sqrt(len(square_matrix)))
        if size != 2:
            return sum(
                cls.cofactor(square_matrix=square_matrix, i=0, j=j) * square_matrix[j]
                for j in range(size)
                # skip `zero` elements
                if square_matrix[j]
            )
        else:
            return (
                square_matrix[0] * square_matrix[3]
                - square_matrix[1] * square_matrix[2]
            )

    @cached_property
    def dimensions(self) -> Tuple[int, int]:
        """Return dimensions of matrix as tuple of number of rows and number of columns"""
        return self.row_count, self.column_count

    @cached_property
    def determinant(self) -> float:
        """Return determinant (scalar value) of matrix"""
        if self.elements and self.row_count == self.column_count:
            if len(self.elements) == 1:
                return self.elements[0]
            return self._determinant(square_matrix=self.elements)
        else:
            raise AttributeError(
                f"Matrix({self.row_count}, {self.column_count}) has no attribute 'determinant'"
            )

    def row(self, n: int = 0) -> MatrixElements:
        """Return `n`-row of matrix.

        Args:
            n: row number from 0 to number of rows - 1.

        Returns:
            row as a list of elements.

        Raises:
            IndexError: if `n` less than zero or greater than or equal to
                number of rows.

        """
        if 0 <= n < self.row_count:
            return self.elements[
                n * self.column_count : n * self.column_count + self.column_count :
            ]
        else:
            raise IndexError

    def column(self, n: int = 0) -> MatrixElements:
        """Return `n`-column of matrix.

        Args:
            n: column number from 0 to number of columns - 1.

        Returns:
            column as a list of elements.

        Raises:
            IndexError: if `n` less than zero or greater than or equal to
                number of columns.

        """
        if 0 <= n < self.column_count:
            return self.elements[n :: self.column_count]
        else:
            raise IndexError

    def transpose(self, *, kind: str = "main diagonal") -> Matrix:
        transpose_kinds: Dict[str, Callable[..., Matrix]] = {
            "main diagonal": self.transpose_at_main_diagonal,
            "side diagonal": self.transpose_at_side_diagonal,
            "vertical line": self.transpose_at_vertical_line,
            "horizontal line": self.transpose_at_horizontal_line,
        }
        if kind in transpose_kinds:
            return transpose_kinds[kind]()
        else:
            raise NotImplementedError

    def transpose_at_main_diagonal(self) -> Matrix:
        elements: MatrixElements = list()
        for c in range(self.column_count):
            elements.extend(self.column(c))
        return Matrix(self.column_count, self.row_count, elements=elements)

    def transpose_at_side_diagonal(self) -> Matrix:
        elements: MatrixElements = list()
        for c in reversed(range(self.column_count)):
            elements.extend(reversed(self.column(c)))
        return Matrix(self.column_count, self.row_count, elements=elements)

    def transpose_at_vertical_line(self) -> Matrix:
        elements: MatrixElements = list()
        for r in range(self.row_count):
            elements.extend(reversed(self.row(r)))
        return Matrix(self.row_count, self.column_count, elements=elements)

    def transpose_at_horizontal_line(self) -> Matrix:
        elements: MatrixElements = list()
        for r in reversed(range(self.row_count)):
            elements.extend(self.row(r))
        return Matrix(self.row_count, self.column_count, elements=elements)


class Processor:
    def __init__(self) -> None:
        self.menu_options: MenuOptions = {
            '1': ("Add matrices", self._addition),
            '2': ("Multiply matrix by a constant", self._multiplication_by_number),
            '3': ("Multiply matrices", self._matrix_by_matrix_multiplication),
            '4': ("Transpose matrix", self._transpose_matrix),
            '5': ("Calculate a determinant", self._calculate_determinant),
            '6': ("Inverse matrix", self._inverse_matrix),
            '0': ("Exit", exit),
        }

    @staticmethod
    def _make_choice(options: MenuOptions) -> Choice:
        print(*(f"{num}. {value[0]}" for num, value in options.items()), sep='\n')
        option: str = ''
        while option not in options:
            option = input("Your choice: ")
        return options[option]

    @staticmethod
    def _print_result(result: Any) -> None:
        print("The result is:", str(result), "", sep='\n')

    def _addition(self) -> None:
        # Stage #1: Addition
        matrix_a: Matrix = Matrix(alias='first')
        matrix_b: Matrix = Matrix(alias='second')
        matrix: Matrix = matrix_a + matrix_b
        if matrix:
            self._print_result(matrix)

    def _multiplication_by_number(self) -> None:
        # Stage 2: Multiplication by number
        matrix: Matrix = Matrix()
        constant: str = input("Enter constant: ")
        number: float = float(constant) if '.' in constant else int(constant)
        self._print_result(matrix * number)

    def _matrix_by_matrix_multiplication(self) -> None:
        # Stage 3: Matrix by matrix multiplication
        matrix_a: Matrix = Matrix(alias='first')
        matrix_b: Matrix = Matrix(alias='second')
        self._print_result(matrix_a * matrix_b)

    def _transpose_matrix(self) -> None:
        # Stage 4: Transpose
        transpose_options: Dict[str, str] = {
            '1': "Main diagonal",
            '2': "Side diagonal",
            '3': "Vertical line",
            '4': "Horizontal line",
        }
        print(
            *(
                f"{num}. {description}"
                for num, description in transpose_options.items()
            ),
            sep='\n',
        )
        option: str = ''
        while option not in transpose_options:
            option = input("Your choice: ")
        matrix: Matrix = Matrix().transpose(kind=transpose_options[option].lower())
        self._print_result(matrix)

    def _calculate_determinant(self) -> None:
        # Stage 5: Determined!
        matrix: Matrix = Matrix()
        self._print_result(matrix.determinant)

    def _inverse_matrix(self) -> None:
        # Stage 6: Inverse matrix
        matrix: Matrix = Matrix()
        self._print_result(matrix.inverse)

    def cli(self) -> None:
        while True:
            choice: Choice = self._make_choice(self.menu_options)
            try:
                choice[1]()
            except (
                AttributeError,
                IndexError,
                NotImplementedError,
                TypeError,
                ValueError,
            ):
                print("The operation cannot be performed.\n")


if __name__ == '__main__':
    processor: Processor = Processor()
    processor.cli()
