import pytest

from app.switchboard import Switchboard, InvalidCallFormatException
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_active_calls_should_return_zero() -> None:  # возможно этот тест уже лишний, добавил для обработки крайнего случая
    switchboard = Switchboard()
    assert switchboard.get_active_calls_count() == 0


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_register_call_counts_calls_between_local_and_foreign_users_should_return_zero() -> None:  # тоже ради крайнего случая
    switchboard = Switchboard()

    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+73123456789,6,Alex Doe,+742012345678"
    )

    assert switchboard.get_cross_border_calls_count() == 0


def test_register_call_with_incorrect_format_of_raw_call_should_raise_exception() -> None:
    switchboard = Switchboard()
    with pytest.raises(InvalidCallFormatException, match="Format of raw input is incorrect. Expected 6 field, got 0"):
        switchboard.register_call("")
    with pytest.raises(InvalidCallFormatException, match="Format of raw input is incorrect. Expected 6 field, got 3"):
        switchboard.register_call("123,123,123")


def test_register_call_with_incorrect_userid_in_raw_call_should_raise_exception() -> None:
    switchboard = Switchboard()
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of caller_id or receiver_id"):
        switchboard.register_call(
            "ERROR,Jane Doe,+33123456789,TEST,Alex Doe,+442012345678"
        )
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of caller_id or receiver_id"):
        switchboard.register_call(
            "123,Jane Doe,+33123456789,NO,Alex Doe,+442012345678"
        )
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of caller_id or receiver_id"):
        switchboard.register_call(
            "NO,Jane Doe,+33123456789,234,Alex Doe,+442012345678"
        )


def test_register_call_phone_number_doesnt_start_with_plus_should_raise_exception() -> None:
    switchboard = Switchboard()
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of phone number"):
        switchboard.register_call(
            "1,Ivan Ivanov,79990000000,2,John Smith,15551234567"
        )
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of phone number"):
        switchboard.register_call(
            "1,Ivan Ivanov,+59990000000,2,John Smith,15551234567"
        )
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of phone number"):
        switchboard.register_call(
            "1,Ivan Ivanov,59990000000,2,John Smith,+15551234567"
        )


def test_register_call_phone_number_contains_letters_should_raise_exception() -> None:
    switchboard = Switchboard()
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of phone number"):
        switchboard.register_call(
            "1,Ivan Ivanov,+7AAA5404000,2,John Smith,+7BBB51234567"
        )
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of phone number"):
        switchboard.register_call(
            "1,Ivan Ivanov,+7AAA5404000,2,John Smith,+77651234567"
        )
    with pytest.raises(InvalidCallFormatException, match="Incorrect format of phone number"):
        switchboard.register_call(
            "1,Ivan Ivanov,+76545404000,2,John Smith,+7BBB51234567"
        )
