ymaps.ready(['polylabel.create']).then(function() {
    var map = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 2,
        controls: [],
    }, {
        minZoom: 1,
        restrictMapArea: [
            [84.773376, -170.340798],
            [-75.651333, -173.658007],
        ],
    });

    map.events.add('click', function(e) {
        if (!map.balloon.isOpen()) {
            var coords = e.get('coords');
            addBalloon(coords)

        } else {
            map.balloon.close();
        }
    });

    function addBalloon(coords) {
        ymaps.geocode(coords).then(function(res) {
            var firstGeoObject = res.geoObjects.get(0);
            let address = firstGeoObject.getAddressLine()

            openBalloon(coords, address)
        });
    }

    function openBalloon(coords, address) {
        map.balloon.open(coords, {
            contentHeader: address,
            contentBody: '<p>Координаты щелчка: ' + [
                coords[0].toPrecision(6),
                coords[1].toPrecision(6)
            ].join(', ') + '</p>',
            contentFooter: '<sup>Щелкните еще раз</sup>'
        });
    }

    // ЗАЛИВКА РЕГИОНОВ
    var objectManager = new ymaps.ObjectManager();
    // Загрузим регионы.
    ymaps.borders.load('BY', {
        lang: 'ru',
        quality: 2
    }).then(function(result) {
        var options = {
            // Стандартный вид текста будет темный с белой обводкой.
            labelDefaults: 'dark',
            // Макет подписи.
            labelLayout: textLayouts.label,
            // Цвет заливки.
            fillColor: 'rgba(27, 125, 190, 0.7)',
            // Цвет обводки.
            strokeColor: 'rgba(255, 255, 255, 0.8)',
            // Отключим показ всплывающей подсказки при наведении на полигон.
            openHintOnHover: false,
            // Размер текста подписей зависит от масштаба.
            // На уровнях зума 3-6 размер текста равен 12, а на уровнях зума 7-18 равен 14.
            labelTextSize: { '3_6': 12, '7_18': 14 },
            cursor: 'pointer',
            labelDotCursor: 'pointer',
            // Допустимая погрешность в расчете вместимости подписи в полигон.
            labelPermissibleInaccuracyOfVisibility: 4
        };
        // Добавляем полигоны в менеджер объектов.
        objectManager.add(result.features.map(function(feature) {
            feature.id = feature.properties.iso3166;
            // В свойство regionName запишем название региона.
            feature.properties.regionName = feature.properties.iso3166;
            // Присваиваем регионам опции, нужные для модуля подписей полигонов.
            feature.options = options;
            return feature;
        }));
        map.geoObjects.add(objectManager);
    });
});