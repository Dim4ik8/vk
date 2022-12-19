# Публикуем комиксы ВКонтакте
Скрипт автоматизирует публикацию случайных комиксов с сайта [XKCD](https://xkcd.com/) в группе ВКонтакте.

## Как установить
Для запуска скрипта необходим Python 3 и выше версии.
Чтобы парсер работал корректно необходимо установить виртуальное окружение:
```python
python -m venv venv

```
и активировать его командами:
- для Windows:
```python
./venv/Scripts/activate.ps1
```
- для Linux:
```python
source venv/bin/activate
```
Далее важно установить зависимости (необходимые для работы скрипта бибилиотеки):
```python
pip install -r requirements.txt
```
Запуск проекта осуществляется командой:
```python
python main.py
```
Для корректной работы скрипта необходимо получить Токен для работы с API ВКонтакте. Инструкцию можно прочитать [здесь](https://vk.com/dev/implicit_flow_user). 

## Переменные окружения
Чтобы настроить работу программы под конкретные задачи, необходиом организовать создание переменных окружения. В основном каталоге скрипта нужно создать файл с именем **.env** и записать в него значения двух переменных с именами VK_TOKEN и GROUP_ID_VK в кавычках как показано на примере ниже:
```angular2html
VK_TOKEN='vk1uehh&gfkb:KBFGg773ljHVgvljsfuh'
GROUP_ID_VK='75849494'
```
- Про VK_TOKEN написано в предыдущем абзаце 
- GROUP_ID_VK - это id сообщества VK, в котором будут публиковаться комиксы. Его также можно скопировать из адресной строки браузера при входе в сообщество.
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для 
веб-разработчиков [dvmn.org](https://dvmn.org/).