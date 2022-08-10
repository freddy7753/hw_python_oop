from typing import Dict, Type, List, NoReturn
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return ('Тип тренировки: {training_type}; '
                'Длительность: {duration:.3f} ч.; '
                'Дистанция: {distance:.3f} км; '
                'Ср. скорость: {speed:.3f} км/ч; '
                'Потрачено ккал: {calories:.3f}.').format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration_h)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите метод get_spent_calories'
                                  f'{type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER_FOR_MEAN_SPEED: int = 18
    COEFF_FOR_CORRECTING_IN_RUN: int = 20

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_FOR_MEAN_SPEED * self.get_mean_speed()
                - self.COEFF_FOR_CORRECTING_IN_RUN)
                * self.weight_kg / self.M_IN_KM * self.duration_h
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER_COEFF_TO_WEIGHT_WLK: float = 0.035
    SECOND_MULTIPLIER_COEFF_FOR_WLK: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_COEFF_TO_WEIGHT_WLK * self.weight_kg
                + (self.get_mean_speed()**2
                   // self.height_cm)
                * self.SECOND_MULTIPLIER_COEFF_FOR_WLK * self.weight_kg)
                * (self.duration_h * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CORRECT_FOR_MEAN_SPEED_IN_SM: float = 1.1
    MULTIPLIER_FOR_MEAN_SPEED_AND_WEIGHT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool_m * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CORRECT_FOR_MEAN_SPEED_IN_SM)
                * self.MULTIPLIER_FOR_MEAN_SPEED_AND_WEIGHT * self.weight_kg)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trayning_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    if workout_type not in trayning_type:
        raise ValueError(f'Получен неизвестный тип тренировки: {workout_type}.'
                         f' Введите: {trayning_type.keys()}')

    return trayning_type[workout_type](*data)


def main(training: Training) -> NoReturn:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
