"""
Task1.

Реализуйте функцию, которая конвертирует число (без знака) из десятичной системы исчисления 
в любую другую. Ваша функция должна иметь следующий прототип:
String itoBase(unsigned int nb, String base); nb – это подаваемое число, base – система исчисления.
На пример, «01» - двоичная, «012» - троичная, «0123456789abcdef» - шеснадцатиричная, «котики»
- система исчисления в котиках.

Дополнительно*: перегрузите функцию, чтобы она могла конвертировать число из любой системы 
исчисления в любую другую:
String itoBase(String nb, String baseSrc, String baseDst);

Для проверки задания, напишите метод main, который принимает необходимые значения из 
аргументов командной строки, и выводит результат на экран. При некорректном вводе 
аргументов должен выводится usage.

"""
import string
import sys


# NOTE: Для проверки задания, напишите метод main.. Чтобы написать метод main, вместо функции был определен класс
class NumConverter:
    """Number converter from any number system to any other."""

    def __init__(self, cmd_args: list) -> None:
        """Initialize a new NumConverter instance with sys.argv."""
        self._args = cmd_args[1:]

    def main(self) -> str:
        """
        Takes the required values from the command line arguments and display
        the result to the screen.
        If the arguments are entered incorrectly, an error and 
        usage hint are displayed. Elif entered correctly, it converts
        according to the specified parameters.

        """
        return self._validate() or self._convert_number_to_base(*self._args)

    def _convert_number_to_base(self, num: str, base: str, dst: str=None) -> str:
        """Convert base10-num to n-base or convert n-base-num to n-base."""
        if dst is None:
            return self._decimal_to_any_base(int(num), int(base))
        
        return self._decimal_to_any_base(
            self._any_base_to_decimal(num, int(base)), 
            int(dst)
        )

    def _decimal_to_any_base(self, decimal: int, base: int) -> str:
        """Convert a decimal number to any other number system."""
        alphanum: str = string.digits + string.ascii_lowercase
        other_base: str = ''

        while decimal:
            other_base = alphanum[int(decimal % base)] + other_base
            decimal //= base

        if not other_base: other_base = '0'
        
        print(other_base)
        return other_base

    def _any_base_to_decimal(self, num: str, base: int) -> int:
        """Convert from any other number system to a decimal number."""
        return int(num, base)

    def _get_usage_errors(self, err: str) -> str:
        """Get the corresponding error and usage hint by key."""
        usage = '\nUsage: Enter num and to-base or num, num-base and to-base'
        return {
            'MISSING': 'Missing required arguments! ' + usage,
            'STR_ERR': 'Expected numbers only! ' + usage,
            'TOO_MANY': 'Too many arguments! ' + usage,
        }[err]

    def _validate(self) -> bool:
        """Validate entered data."""
        if len(self._args) < 2:
            print(self._get_usage_errors('MISSING'))
            return True
        elif 2 <= len(self._args) <= 3:
            if not all([arg.isdigit() for arg in self._args[-2:]]):
                print(self._get_usage_errors('STR_ERR'))
                return True
        elif len(self._args) > 3:
            print(self._get_usage_errors('TOO_MANY'))
            return True
        return False

converter = NumConverter(sys.argv)
converter.main()
