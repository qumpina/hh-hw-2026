from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser

LOCAL_PHONE_PREFIX = "+7"


class InvalidCallFormatException(Exception):
    """Raised when the call string format is invalid."""
    pass


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self.cross_border_calls: int = 0
        self._active_calls: list[ActiveCall] = []

    def create_user(self, user_id: int, fullname: str, phone: str) -> User:
        if phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(user_id, fullname, phone)
        else:
            return ForeignUser(user_id, fullname, phone)

    def validate_phone_number(self, phone_number: str) -> None:
        if phone_number.startswith("+") and phone_number[1:].isdigit():
            return
        else:
            raise InvalidCallFormatException("Incorrect format of phone number")

    def validate_user_name(self, name: str) -> None:
        name=name.split()
        if len(name)==2 and name[0].isalpha() and name[1].isalpha():
            return
        else:
            raise InvalidCallFormatException("Incorrect format of user name")

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        user_info = raw_call.split(",")
        if len(user_info) != 6:
            if raw_call.count(",") == 0:
                raise InvalidCallFormatException("Format of raw input is incorrect. Expected 6 field, got 0")
            raise InvalidCallFormatException(
                f"Format of raw input is incorrect. Expected 6 field, got {len(user_info)}"
            )

        try:
            caller_id = int(user_info[0])
            caller_name = user_info[1]
            caller_phone = user_info[2]
            self.validate_user_name(caller_name)
            self.validate_phone_number(caller_phone)
            caller = self.create_user(caller_id, caller_name, caller_phone)

            receiver_id = int(user_info[3])
            receiver_name = user_info[4]
            receiver_phone = user_info[5]
            self.validate_user_name(receiver_name)
            self.validate_phone_number(receiver_phone)
            receiver = self.create_user(receiver_id, receiver_name, receiver_phone)
        except ValueError:
            raise InvalidCallFormatException(f"Incorrect format of caller_id or receiver_id")

        active_call = ActiveCall(caller, receiver)
        self._active_calls.append(active_call)
        if active_call.is_cross_border:
            self.cross_border_calls += 1
        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self.cross_border_calls
