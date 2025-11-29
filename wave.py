from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import (RangeSlider, Slider,
                                RadioButtons, CheckButtons,
                                TextBox)


def coordinate(amplitude, frequency, phi, betta, x):
    """Координата точки от времени"""
    A = amplitude * np.exp(-betta * x)
    omega = ((2 * np.pi * frequency) ** 2 - betta ** 2) ** (1 / 2)
    phase = omega * x + phi
    s = A * np.sin(phase)
    return s

def velocity(amplitude, frequency, phi, betta, x):
    """Скорость точки от времени"""
    A = amplitude * np.exp(-betta * x)
    omega = ((2 * np.pi * frequency) ** 2 - betta ** 2) ** (1 / 2)
    phase = omega * x + phi
    v = A * (omega * np.cos(phase) - betta * np.sin(phase))
    return v

def acceleration(amplitude, frequency, phi, betta, x):
    """Скорость точки от времени"""
    A = amplitude * np.exp(-betta * x)
    omega = ((2 * np.pi * frequency) ** 2 - betta ** 2) ** (1 / 2)
    phase = omega * x + phi
    a = A * np.sin(phase) * (betta ** 2 - omega ** 2)
    return a

def kinetic(m, v):
    """Кинетическая энергия точки"""
    K = m * v ** 2 / 2
    return K

def potencial(m, omega, s):
    """Потенциальная энергия точки"""
    k = omega ** 2 * m
    P = k * s ** 2 / 2
    return P

def cicle_omega(frequency, betta):
    """Циклическая частота колебаний"""
    omega = ((2 * np.pi * frequency) ** 2 - betta ** 2) ** (1 / 2)
    return omega

def energy(K, P):
    """Циклическая частота колебаний"""
    E = K + P
    return E

def updateGraph():
    """!!! Функция для обновления графика"""
    global slider_amplitude
    global slider_frequency
    global slider_phi
    global slider_betta
    global slider_x_range
    global slider_y_range
    global graph_axes
    global x_min
    global x_max
    global y_min
    global y_max
    # global radiobuttons_color
    # global checkbuttons_grid

    # Словарь соответсвий текста и стиля линии
    # colors = {"Красный": "r", "Синий": "b", "Зеленый": "g"}

    # Используем атрибут val, чтобы получить значение слайдеров
    amplitude = slider_amplitude.val
    frequency = slider_frequency.val
    phi = slider_phi.val
    betta = slider_betta.val

    # Получаем значение интервала
    x_min, x_max = slider_x_range.val
    y_min, y_max = slider_y_range.val

    x = np.arange(x_min, x_max, 0.001)

    s = coordinate(amplitude, frequency, phi, betta, x)
    v = velocity(amplitude, frequency, phi, betta, x)
    a = acceleration(amplitude, frequency, phi, betta, x)
    K = kinetic(mass, v)
    omega = cicle_omega(frequency, betta)
    P = potencial(mass, omega, s)
    E = energy(K, P)

    # Выберем стиль линии по выбранному значению радиокнопок
    # style = colors[radiobuttons_color.value_selected]

    graph_axes.clear()

    # Настройка осей
    graph_axes.set_xlabel('X')
    graph_axes.set_ylabel('Y')
    graph_axes.set_xlim(x_min, x_max)
    graph_axes.set_ylim(y_min, y_max)
    graph_axes.grid()

    # Отриссовка функций c проверкой условия нажатой кнопки
    check_data = [0] * n
    data = [s, v, a, K, P, E]
    color_data = ['red', 'blue', 'green', 'orange', 'brown', 'black']

    for i in range(n):
        check_data[i] = check_but[i].get_status()[0]
        if check_data[i]:
            graph_axes.plot(x, data[i], c=color_data[i])

    # Определяем, нужно ли показывать сетку на графике
    # grid_visible = checkbuttons_grid.get_status()[0]
    # graph_axes.grid(grid_visible)



def onTitleChange(value: str):
    """!!! Обработчик события при изменении текста в поле ввода"""
    global graph_axes
    graph_axes.set_title(value)
    plt.draw()

def onCheckClicked(value: str):
    """Обработчик события при нажатии на флажок"""
    plt.draw()
    updateGraph()


def onRadioButtonsClicked(value: str):
    """Обработчик события при клике по RadioButtons"""
    updateGraph()


def onChangeValue(value: np.float64):
    """Обработчик события изменения значений амплитуды, частоты, начальной фазы и коэффициента затухания"""
    updateGraph()


def onChangeRange(value: Tuple[np.float64, np.float64]):
    """Обработчик события измерения значения интервала по оси X и Y"""
    updateGraph()


if __name__ == "__main__":
    # Начальные параметры графиков
    current_amplitude = 0.2
    current_frequency = 1.0
    current_phi = 0.0
    current_betta = 0.0
    betta_max = current_frequency * 2 * np.pi
    x_min = -0
    x_max = 5
    y_min = -5
    y_max = 5
    mass = 1
    g = 9.8

    # Создадим окно с графиком
    fig, graph_axes = plt.subplots(figsize=(16, 8))

    # Выделим область, которую будет занимать график
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.5)

    # Создадим слайдер для задания amplitude
    axes_slider_amplitude = plt.axes([0.3, 0.39, 0.5, 0.04])
    slider_amplitude = Slider(
        axes_slider_amplitude,
        label="A",
        valmin=0.0,
        valmax=2.0,
        valinit=current_amplitude,
        valfmt="%1.2f",
    )

    # Создадим слайдер для задания frequency
    axes_slider_frequency = plt.axes([0.3, 0.35, 0.5, 0.04])
    slider_frequency = Slider(
        axes_slider_frequency,
        label="f",
        valmin=1.0,
        valmax=100.0,
        valinit=current_frequency,
        valfmt="%1.2f",
    )

    # Создадим слайдер для задания phi
    axes_slider_phi = plt.axes([0.3, 0.31, 0.5, 0.04])
    slider_phi = Slider(
        axes_slider_phi,
        label="phi_0",
        valmin=-2 * np.pi,
        valmax=2 * np.pi,
        valinit=current_phi,
        valfmt="%1.2f",
    )

    # Создадим слайдер для задания betta
    axes_slider_betta = plt.axes([0.3, 0.27, 0.5, 0.04])
    slider_betta = Slider(
        axes_slider_betta,
        label="betta",
        valmin=0.0,
        valmax=betta_max,
        valinit=current_betta,
        valfmt="%1.2f",
    )


    # Создадим слайдер для задания интервала по оси X
    axes_slider_x_range = plt.axes([0.3, 0.23, 0.5, 0.04])
    slider_x_range = RangeSlider(
        axes_slider_x_range,
        label="x",
        valmin=-0.0,
        valmax=20.0,
        valinit=(x_min, x_max),
        valfmt="%1.2f",
    )

    # Создадим слайдер для задания интервала по оси y
    axes_slider_y_range = plt.axes([0.3, 0.19, 0.5, 0.04])
    slider_y_range = RangeSlider(
        axes_slider_y_range,
        label="y",
        valmin=-30.0,
        valmax=30.0,
        valinit=(y_min, y_max),
        valfmt="%1.2f",
    )

    # Создадим оси для переключателей
    # axes_radiobuttons = plt.axes([0.05, 0.22, 0.17, 0.2])

    # Создадим переключатель
    # radiobuttons_color = RadioButtons(
    #     axes_radiobuttons, ["Красный", "Синий", "Зеленый"]
    # )

    # Создадим оси для флажка
    # axes_checkbuttons = plt.axes([0.05, 0.15, 0.17, 0.07])
    radio_axes = [0.05, 0.39, 0.12, 0.04]
    n = 6
    check_axes = [0] * n

    for i in range(n):
        check_axes[i] = plt.axes(radio_axes)
        radio_axes[1] = radio_axes[1] - radio_axes[3]

    # axes_velocity = plt.axes(radioaxes)

    # Создадим флажок
    # checkbuttons_grid = CheckButtons(axes_checkbuttons, ["Сетка"], [True])
    name = ['Координата', 'Скорость', 'Ускорение', 'Кинетическая', 'Потенциальная', 'Полная']
    check_but = [0] * n
    for i in range(n):
        check_but[i] = CheckButtons(check_axes[i], [name[i]], [False])
    # checkbuttons_velocity = CheckButtons(check_axes[1], [name[1]], [False])

    # !!! Создадим оси для текстового поля
    # axes_textbox = plt.axes([0.4, 0.01, 0.4, 0.05])

    # !!! Создадим текстовое поле
    # textbox_title = TextBox(axes_textbox, "Заголовок")

    # Подпишемся на события при изменении значения слайдеров.
    slider_amplitude.on_changed(onChangeValue)
    slider_frequency.on_changed(onChangeValue)
    slider_phi.on_changed(onChangeValue)
    slider_betta.on_changed(onChangeValue)

    # Подпишемся на событие изменения интервала по оси X
    slider_x_range.on_changed(onChangeRange)

    # Подпишемся на событие изменения интервала по оси Y
    slider_y_range.on_changed(onChangeRange)

    # Подпишемся на событие при переключении радиокнопок
    # radiobuttons_color.on_clicked(onRadioButtonsClicked)

    # Подпишемся на событие при клике по флажку
    # checkbuttons_grid.on_clicked(onCheckClicked)
    # checkbuttons_coordinate.on_clicked(onCheckClicked)
    # checkbuttons_velocity.on_clicked(onCheckClicked)
    for i in range(n):
        check_but[i].on_clicked(onCheckClicked)



    # !!! Подпишемся на события текстового поля
    # textbox_title.on_text_change(onTitleChange)
    # textbox_title.on_submit(onTitleChange)

    updateGraph()
    plt.show()
