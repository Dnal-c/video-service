# video-service

Данный сервис предназначен для поиска видео

В качестве БД используется ElasticSearch. Для поиска используется knn query по векторным полям  
В индексе есть три поля dense_vector:

- description_ru_vector: Вектор описания видео, сгенерированного ML моделью
- voice_vector: Вектор озвучки
- tags_vector: Вектор ручного описания

Поиск осуществляется по этим трем полям с весами:

- description_ru_vector: 1
- voice_vector: 0.35
- tags_vector: 0.85

Значения весов были эмпирически выведены и являются наилучшей(неплохой) комбинацией для релевантного поиска  
Сервис имеет API настройки данных весов

Также сервис выставляет API автокомлита текстового запроса