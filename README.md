Горчаков Роман Владимирович. Вариант 2
# Лабораторная работа 4.6. Классы данных в Python

Класс данных – класс, который (в основном) хранит данные, хотя на самом деле, нет никаких ограничений. Он разработан при помощи декоратора @dataclass. Класс данных имеет уже реализованный базовый функционал. Например, вы можете создать экземпляр, выводить и сравнивать существующие классы данных, сразу без лишнего кода. По умолчанию, классы данных реализует метод .__repr__(), чтобы предоставить хорошее строковое представление, а также метод .__eq__(), который в состоянии выполнять базовые сравнения объектов.

Декоратор @dataclass делает класс – классом данных, прямо над определением класса. Под строкой class Position:, вы просто афишируете список полей, которые вы хотите в своем классе данных. Нотация «:», которая используется для полей, использует новую функцию в Python 3.6, под названием типизация переменных. Вы также можете создать классы данных аналогично тому, как создаются названные кортежи.

Фактически, добавление какого-либо типа является обязательным при определении полей в вашем классе данных. Без типизации, поле не будет частью класса данных. Однако, если вы не хотите добавлять лишние типы в ваш класс данных, используйте Any из пакета typing. Хотя вам нужно добавить тип при вводе в какой-нибудь форме при использовании классов данных, эти типы не запускаются во время выполнения.

До этого вы видели некоторые основные возможности класса данных: он предоставляет более удобные методы, при этом вы все еще можете вносить значения по умолчанию и другие методы. Теперь вы узнаете о более продвинутых возможностях, такие как параметры декоратора @dataclass и функция field(). Вместе, они могут дать вам больше контроля над ситуацией при создании класса данных.

Определитель field() используется для кастомизации каждого поля или класса данных индивидуально. Вы увидите несколько примеров ниже. Для примера, рассмотрим поддерживаемые field() параметры:
* default: Значение поля по умолчанию;
* default_factory: Функция, которая возвращает начальное значение поля;
* init: использует поле в методе .init() (True по умолчанию);
* repr: Использует поле repr объекта (True по умолчанию);
* compare: Включает поле в сравнениях (True по умолчанию);
* hash: Включает поле при подсчете hash() (По умолчанию используется то же, что и при сравнении);
* metadata: Сопоставление с информацией о поле.

В целом, объект Python имеет две разные строки представления:
* repr(obj) определен obj.repr() и должен возвращать приемлемое для разработчика представление об объекте. При возможности, это должен быть код, который воссоздает объект. Классы данных могут это;
* str(obj) определен obj.str() и может возвращать приемлемое для разработчика представление об объекте. Классы данных не реализуют метод .str(), так что Python вернется назад к методу .repr().

Декоратор @dataclass имеет две формы. До сих пор мы видели простую форму, где @dataclass определен без круглых скобок и параметров. Однако, вы также можете задать параметры @dataclass в круглых скобках. Поддерживаются следующие параметры:
* init: Вносит метод .__init__() (True по умолчанию);
* repr: Вносит метод .__repr__() (True по умолчанию);
* eq: Вносит метод .__eq__() (True по умолчанию);
* order: Вносит методы упорядочивания (False по умолчанию);
* unsafe_hash: Выполняет внесение метода .__hash__() (False по умолчанию);
* frozen: если True, присвоение к полям вызывает ошибку (False по умолчанию).

Чтобы сделать класс данных неизменяемым, установите frozen=True при создании. В замороженном классе данных вы не можете менять значения для полей после их создания. Имейте ввиду, что если ваш класс данных содержит изменяемые поля, они все еще могут изменяться. Если параметр имеет значение по умолчанию, все следующие параметры должны также иметь значение по умолчанию. Иными словами, если поле в базовом классе имеет значение по умолчанию, то все новые внесённые поля которые были унаследованы, должны также иметь значения по умолчанию. Начиная с базового класса, поля упорядочены в том порядке, в котором они изначально были определены. Если поле переопределено в подкласс, его порядок не меняется.

Слоты можно использовать, чтобы ускорить классы и использовать меньше памяти. Классы данных не имеют явного синтаксиса для работы со слотами, однако обычный способ создания слотов для классов данных работает. По сути своей, слоты определяются при помощи .__slots__ , чтобы внести список переменных в класс. Переменные или атрибуты не присутствуют в .__slots__ могут не определиться. Более того, класс слотов может не иметь значений по умолчанию. Преимущество внесения таких ограничений в том, что определенные оптимизации могут быть выполнены. Например, класс слотов занимает меньше памяти, что можно измерить, используя Pympler.