# locklib
Some extend features connected with locks

Далее будет немного сумбурное описание алгоритма работы алгоритма выдачи уникальных чисел с помощью дерева.

2 базовых алгоритма:
1. Выдача чисел.
2. Запрос нод.

Оба алгоритма должны уметь выполняться параллельно, не мешая друг другу.


## Выдача чисел

Существует 3 типа нод дерева: листья, срединные ноды, корень. У каждого из них свой алгоритм. Также есть обертка, итого 4 типа объектов.

Алгоритм листьев:

1. Если текущее число меньше или равно пределу выданного интервала, выдать его, после чего инкрементировать текущее число.
2. Если текущее число выходит за пределы интервала, запросить новый подинтервал, передав в родительскую ноду размер ожидаемого интервала, и получив в ответ новую стартовую позицию. Установить в качестве текущего числа данное число, а в качестве предела интервала - данное число + ширину запрошенного интервала. После чего полученное число нужно вернуть, а счетчик инкрементировать.

Алгоритм срединных нод:

1. Если запрошенный интервал меньше имеющегося (то есть текущее число + запрошенная ширина интервала - меньше максимального числа) - возвращаем текущее число, после чего инкрементим его запрошенной шириной интервала.
2. Если запрошенный интервал превышает имеющуюся ширину (то есть текущее число + длина интервала - больше максимального числа), запрашиваем новый старт, передавая ноде-родителю свою ширину интервалов.

Алгоритм корня дерева:

1. Если запрошенный интервал в пределах доступного - возвращаем текущее число и имплементируем текущее число по аналогии со срединной нодой.
2. В противном случае - сдвигаем свой интервал.


## Запрос ноды

1. Если запрошенная нода есть в словаре - возвращаем ее.
2. Если нет:
2.1. Блокируем обертку на добавление новых нод.
2.2. Проверяем, заполнена ли иерархия нод ниже.
2.2.1. Если не заполнена:
2.2.1.1. Находим ноду, от которой нужно достроить ветку.
2.2.1.2. Строим ветку нужной длины, с листом в конце.
2.2.1.3. Встраиваем новую ветку в нужную ноду.
2.2.1.4. Возвращаем лист.
2.2.2. Если заполнена:
2.2.2.1. Создаем новую рутовую ноду.
2.2.2.2. Создаем ветку мидлов, равную по длине высоте текущей корневой ноде.
2.2.2.3. Вставляем в конец лист.
2.2.2.4. Объединяем ветку.
2.2.2.5. Блокируем текущий корень.
2.2.2.6. Снимаем с корня флаг корня и меняем родителя у корня на новую корневую ноду.
2.2.2.7. В обертке заменяем указатель корня на новый.
2.2.2.8. Возвращаем лист.
2.3. Снимаем блокировку с обертки.
