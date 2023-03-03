from enum import Enum
from abc import *
import datetime


class Role(Enum):
    CEO = 0
    CFO = 1
    CIO = 2


class Department(Enum):
    ACCOUNTING = 0
    FINANCE = 1
    HR = 2
    R_AND_D = 3
    MACHINING = 4


class InvalidRoleException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDepartmentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Employee(ABC):
    """Employee is an abstract class that holds common information about all employees.  We will be
    making heavy use of properties in this project, as is reflected in this code."""
    CURRENT_ID = 1
    IMAGE_PLACEHOLDER = './images/placeholder.png'

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.image = Employee.IMAGE_PLACEHOLDER
        self.id_number = Employee.CURRENT_ID
        Employee.CURRENT_ID += 1

    def __str__(self):
        return str(self.id_number) + ":" + self.name

    def __repr__(self):
        return self.name, self.email, self.image

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name == '':
            raise ValueError('Name cannot be blank.')
        elif not isinstance(name, str):
            raise ValueError('Name needs to be a string.')
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email == '':
            raise ValueError('Email cannot be blank.')
        elif not isinstance(email, str):
            raise ValueError('Email needs to be a string.')
        elif '@acme-machining.com' not in email:
            raise ValueError('Email needs to end with @acme-machining.com')
        self._email = email

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if image == '':
            raise ValueError('Image path cannot be blank.')
        elif not isinstance(image, str):
            raise ValueError('Image needs to be a string.')
        self._image = image

    @property
    def id(self):
        return self.id_number

    @abstractmethod
    def calc_pay(self) -> float:
        """This function calculates the weekly pay for the current
        employee for our pay report."""
        pass


class Salaried(Employee):
    """A Salaried Employee is one who has a yearly salary."""
    def __init__(self, name, email, yearly):
        super().__init__(name, email)
        self.yearly = yearly

    @property
    def yearly(self):
        return self._yearly

    @yearly.setter
    def yearly(self, yearly):
        if yearly < 0 or yearly < 50000:
            raise ValueError('Yearly cannot be less than zero or less than 50000.')
        if not isinstance(yearly, float):
            raise ValueError('Yearly needs to be an float.')
        self._yearly = yearly

    def calc_pay(self) -> float:
        return self.yearly / 52.0

    def __repr__(self):
        return str(super().__repr__()) + ", " + str(self.yearly)


class Hourly(Employee):
    """An Hourly Employee adds an hourly wage."""
    def __init__(self, name, email, hourly):
        super().__init__(name, email)
        self.hourly = hourly

    @property
    def hourly(self):
        return self._hourly

    @hourly.setter
    def hourly(self, hourly):
        if hourly < 15 or hourly > 99.99:
            raise ValueError('Hourly needs to be between 15 and 99.99.')
        elif not isinstance(hourly, (int, float)):
            raise ValueError('Hourly needs to be either an integer or a float.')
        self._hourly = hourly

    def calc_pay(self) -> float:
        return self.hourly * 40

    def __repr__(self):
        return str(super().__repr__()) + ', ' + str(self.hourly)


class Executive(Salaried):
    """An Executive is a Salaried Employee with no additional information held."""
    def __init__(self, name, email, salary, role):
        super().__init__(name, email, salary)
        self.role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        if role not in Role:
            raise InvalidRoleException('Role needs to be a valid role.')
        self._role = role

    def __repr__(self):
        return str(super().__repr__()) + ',' + str(self.role)


class Manager(Salaried):
    """A Manager is a Salaried Employee with no additional information held.  May want to add
    a department, etc. for increased scope."""
    def __init__(self, name, email, salary, department):
        super().__init__(name, email, salary)
        self.department = department

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, department):
        if department not in Department:
            raise InvalidDepartmentException('Department needs to be a valid department.')
        self._department = department


class Permanent(Hourly):
    """Hourly Employees may be Permanent.  A Permanent Hourly Employee has a hired date."""
    def __init__(self, name, email, hourly, hired_date):
        super().__init__(name, email, hourly)
        self.hired_date = hired_date

    @property
    def hired_date(self):
        return self._hired_date

    @hired_date.setter
    def hired_date(self, hired_date):
        self._hired_date = datetime.datetime.strptime(str(hired_date), '%Y-%m-%d')

    def __repr__(self):
        return str(super().__repr__()) + ', ' + str(self.hired_date)


class Temporary(Hourly):
    """A Temp Employee is paid hourly but has a date they can no longer work past."""
    def __init__(self, name, email, hourly, last_day):
        super().__init__(name, email, hourly)
        self.last_day = last_day

    @property
    def last_day(self):
        return self._last_day

    @last_day.setter
    def last_day(self, last_day):
        self._last_day = datetime.datetime.strptime(str(last_day), '%Y-%m-%d')

    def __repr__(self):
        return str(super().__repr__()) + ', ' + str(self.last_day)
