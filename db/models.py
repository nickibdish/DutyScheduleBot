from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}')>"

class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)     # год, например, 2025
    month = Column(Integer, nullable=False)      # месяц (1-12)
    day = Column(Integer, nullable=False)        # номер дня (например, 1,2,3,...)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    shift = Column(String, nullable=False)       # код смены: допустимые значения "Р", "В", "К", "О", "Д"
    
    # Связь с таблицей сотрудников: через атрибут employee можно получить объект Employee
    employee = relationship("Employee", backref="schedules")

    def __repr__(self):
        return (f"<Schedule(id={self.id}, year={self.year}, month={self.month}, day={self.day}, "
                f"employee='{self.employee.name}', shift='{self.shift}')>")
