
import datetime
import re

"""

"""


class ArgumentValidator:
    """
    Holds the functions that validate the arguments
        of rest paths
    """

    # =============================== REST.py =========================================

    @staticmethod
    def _validate(data, validation):
        """
        Validates that data received on rest path
            follow the expected arguments

        :param data: data to validate
        :type data: dict
        :param validation: list of tuples with KEY of mandatory fields
            EXPECTEDTYPES for those filds and if that field is mandatory
        :type validation: list
        :return: all errors presents on arguments
        :rtype: list
        """
        errors = []
        for key, expectedType, mandatory in validation:
            try:
                value = data[key] # some values have value null that's why I didn't use get(key, default)
            except KeyError:
                if mandatory:
                    errors.append("Missing key \"" + key + "\"")
                continue

            if value == None:
                if mandatory:
                    errors.append("Value \"" + key + "\" can't be null")
                continue

            if not isinstance(value, expectedType):
                if isinstance(value, str):
                    if  (expectedType == int and re.match(r"^[-+]?\d+$", value)) \
                            or (expectedType == float and re.match(r"^[-+]?\d+(\.\d+)?$", value)):
                        continue
                elif isinstance(value, int) and expectedType == float:
                    continue

                errors.append("Value \"" + key + "\" is type "
                              + type(value).__name__ + " but "
                              + expectedType.__name__ + " was expected")

        return errors

    @staticmethod
    def signupAndUpdateProfile(isClient, isUpdateProfile, data):
        if isClient:
            fields = [
                    ("password", str, False),
                    ("name", str, True),
                    ("email", str, True),
                    ("health_number", int, True),
                    ("birth_date", str, False),
                    ("weight", float, False),
                    ("height", float, False),
                    ("additional_info", str, False)]

            if isUpdateProfile:
                fields.append(("new_password", str, False))
            else:
                fields.append(("username", str, True))

            result =  ArgumentValidator._validate(
                data, fields
            )

            birth_date = data.get("birth_date")
            if birth_date and isinstance(birth_date, str):
                if not re.match(r"^\d{1,2}-\d{1,2}-\d{4}$", birth_date):
                    result.append("Invalid date format. Should follow dd-mm-yyyy.")
                else:
                    try:
                        day, month, year = birth_date.split("-")
                        datetime.date(int(year), int(month), int(day))
                    except ValueError:
                        result.append("Invalid date.")

            return result

        fields = [
                ("password", str, True),
                ("name", str, True),
                ("email", str, True),
                ("company", str, False),
                ("specialities", str, False)]

        if isUpdateProfile:
            fields.append(("new_password", str, False))
        else:
            fields.append(("username", str, True))

        return ArgumentValidator._validate(
            data, fields
        )

    @staticmethod
    def signup(data):
        userType = data.get("type")
        if not userType:
            return ["Missing \"type\" parameter"]

        userType = userType.lower()

        if userType not in ["client", "medic"]:
            return ["Type can only be \"client\" or \"medic\""]

        return ArgumentValidator.signupAndUpdateProfile(userType == "client", False, data)

    @staticmethod
    def signin(data):
        return ArgumentValidator._validate(
            data, [
                ("username", str, True),
                ("password", str, True)
            ]
        )

    @staticmethod
    def _addAndUpdateDevice(isAdd, data):
        """
        Use to validate arguments for both addDevice and updateDevice

        :param isAdd: true if it's to validate addDevice fields,
            or false if it's to validate updateDevice
        :type isAdd: bool
        :param data: data to validate
        :type data: dict
        :return: list of errors
        :rtype: list
        """
        fields = [
            ("authentication_fields", dict, True),
            ("latitude", float, False),
            ("longitude", float, False)
        ]

        if isAdd:
            fields.append(("type", str, True))
        else:
            fields.append(("id", int, True))

        result = ArgumentValidator._validate(data, fields)

        auth_fields = data.get("authentication_fields")

        if auth_fields and isinstance(auth_fields, dict):
            for value in auth_fields.values():
                if not isinstance(value, str):
                    result.append("Authentication fields have to be strings.")
                    break

        return result

    @staticmethod
    def addDevice(data):
        return ArgumentValidator._addAndUpdateDevice(True, data)

    @staticmethod
    def updateDevice(data):
        return ArgumentValidator._addAndUpdateDevice(False, data)

    @staticmethod
    def deleteDevice(data):
        return ArgumentValidator._validate(
            data, [
                ("id", int, True)
            ]
        )

    @staticmethod
    def getData(data):
        result = ArgumentValidator._validate(
            data, [
                ("start", int, False),
                ("end", int, False),
                ("interval", str, False),
                ("patient", str, False),
            ]
        )

        interval = data.get("interval")
        if interval and isinstance(interval, str) and not re.match(r"^\d+(ns|u|ms|s|m|h|d|w)$", interval):
            result.append("Inteval argument must follow the regex \"^\d+(ns|u|ms|s|m|h|d|w)$\"")

        return result

    # =============================== Processor.py =========================================

    @staticmethod
    def uploadPermissions(userType, data):
        if userType == "client":
            results = ArgumentValidator._validate(data, [
                ("username", str, True),
                ("duration", int, True)
            ])

            if len(results) == 0 and int(data["duration"]) <= 0:
                return ["Send a duration higher than 0"]

            return results
        elif userType == "medic":
            results_username = ArgumentValidator._validate(data, [
                ("username", str, True),
                ("health_number", int, False),
                ("duration", int, True)
            ])
            results_health_number = ArgumentValidator._validate(data, [
                ("username", str, False),
                ("health_number", int, True),
                ("duration", int, True)
            ])
            if len(results_username) > 0 and len(results_health_number) > 0:
                return ["Missing arguments. " +
                       "Requires keys (health_number:int, duration:int) " +
                       "or (username:str, duration:int)"]

            if int(data["duration"]) <= 0:
                return ["Send a duration higher than 0"]

            results_both = ArgumentValidator._validate(data, [
                ("username", str, True),
                ("health_number", int, True),
            ])
            if len(results_both) == 0:
                return ["Send only health number or patient username"]

            return []
