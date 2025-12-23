# Lidar Obstacle Approximation

Полная инструкция по установке и запуску проекта визуализации данных Lidar из Webots с алгоритмом аппроксимации примитивов в Docker/ROS2 контейнере.

+ [Требования](#требования)
+ [Установка](#установка)
+ [Быстрый старт](#быстрый-старт)


### Требования (host)

- **ОС**: Linux
- **Docker**: docker + docker-compose
- **Webots**: актуальная версия + указать путь к .venv с загруженным numpy 

### Установка webots (опционально).
Мы приводим демонстрацию работы протокола через webots, на деле это может быть что угодно, ведь данные в докер принимаются по TCP.

Рекомендуется установка webots через apt, так как при установке через snap используется built-in питон, а нам для передачи данных нужен numpy.
```bash
apt install webots
```

Создайте где-нибудь venv и установите туда numpy, путь к исполняемому файлу этой venv нужно указать в настройках webots
### Установка Docker (если нет)

Весь ROS-пакет живёт в докере и получает данные по TCP.

```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin
```

### Проверка Docker

```bash
docker --version
docker compose version
```

---

## Установка пакета

### 1) Распаковать архив

```bash
cd ~
tar xzf lidar_full_sources.tar.gz
cd lidar_full_sources
ls -la
```

Должны быть папки __lidar_project__ и __ros2_lidar_docker__, в них находится контроллер и тестовый мир для webots и файлы для докера с  пакетом.

### 2) Установка пакета.

Соберём и поднимем докер.
```bash
cd ~/lidar_full_sources/ros2_lidar_docker
docker compose build
docker compose up -d
```

Соберём ROS2-пакет внутри контейнера:

```bash
cd ~/lidar_full_sources/ros2_lidar_docker
docker compose exec ros2 bash
```
внутри контейнера:
```bash
cd /home/ros/ws
colcon build
source install/local_setup.bash
```


## Быстрый старт

### Структура запуска
Так как ROS-пакет имеет структуру нод, которые между собой взаимодействуют, а webots проще держать не в докере, потребуется 3 терминала
```
Терминал 1: Запуск Webots (опционально)
Терминал 2: TCP → ROS2 bridge
Терминал 3: Алгоритм + визуализация
```

### Запуск Webots (Терминал 1)

Здесь можно просто запустить нужный нам мир.

```bash
cd ~/lidar_full_sources/lidar_project
webots worlds/lidar_world.wbt
```

Убедитесь, что у робота выбран контроллер `lidar_socket_sender` (Properties → Controller)

### TCP-ROS2 мост (Терминал 2)

```bash
cd ~/lidar_full_sources/ros2_lidar_docker
docker compose exec ros2 bash
```
```bash
source /home/ros/ws/install/local_setup.bash
ros2 run lidar_bridge lidar_socket_bridge
```

В случае успеха напишет:
```
[INFO] [...] [lidar_socket_bridge]: Listening TCP on 0.0.0.0:5005
[INFO] [...] [lidar_socket_bridge]: Waiting for Webots connection

```

### Алгоритм + визуализация (Терминал 3)

```bash
cd ~/lidar_full_sources/ros2_lidar_docker
docker compose exec ros2 bash
```

```bash
source /home/ros/ws/install/local_setup.bash
ros2 run lidar_bridge lidar_algo_visualizer
```

Должно открыться окно matplotlib, где в дальнейшем будут фигуры (аппроксимация отрезками и окружностями) и точки (показателями LiDAR).

### Шаг 4: Запуск симуляции

Нажмите Play в Webots


### Вы лучше всех!!!