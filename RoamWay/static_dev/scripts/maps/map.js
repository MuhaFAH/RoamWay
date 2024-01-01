ymaps.ready(init);

function init() {
    var map = new ymaps.Map("map", {
        center: [51.079324, -7.595964],
        zoom: 0,
        type: 'yandex#map',
    }, {
        minZoom: 1,
        restrictMapArea: [
            [85, -165],
            [-75, -166],
        ],
    });

    var objectManager = new ymaps.ObjectManager();
    // Загрузим нужные регионы. '001' - все регионы
    ymaps.borders.load('001', {
        lang: 'ru',
        quality: 1
    }).then(function(result) {
        // Очередь (порядок) раскраски регионов.
        var queue = [];
        // Создадим объект regions, где ключи это ISO код региона.
        var regions = result.features.reduce(function(acc, feature) {
            // Добавим ISO код региона в качестве feature.id для objectManager.
            var iso = feature.properties.iso3166;
            feature.id = iso;
            // Добавим опции региона по умолчанию.
            feature.options = {
                fillOpacity: 0.5,
                strokeColor: '#FFF',
                strokeOpacity: 0.5
            };
            acc[iso] = feature;
            return acc;
        }, {});

        // Функция, которая раскрашивает регион
        function paint(iso) {
            var visited = document.getElementById("visited").innerHTML.split("-")
            var desired = document.getElementById("desired").innerHTML.split("-")
            var region = regions[iso];
            // Раскрасим регион в определенный цвет
            if (visited.includes(iso)) {
                region.options.fillColor = 'rgb(0,50,200)';
            } else if (desired.includes(iso)) {
                region.options.fillColor = 'rgb(155,38,255)';
            } else {
                region.options.fillColor = 'rgba(0,0,0,1)';
            }
        }

        for (var iso in regions) {
            // Если регион не раскрашен, добавим его в очередь на раскраску.
            if (!regions[iso].options.fillColor) {
                queue.push(iso);
            }
            // Раскрасим все регионы из очереди.
            while (queue.length > 0) {
                paint(queue.shift());
            }
        }
        // Добавим регионы на карту.
        result.features = [];
        for (var reg in regions) {
            result.features.push(regions[reg]);
        }
        objectManager.add(result);
        map.geoObjects.add(objectManager);
    })

    // Событие клика по объекту
    function onObjectClick(e) {
        var coords = e.get('coords');
        // objectId – идентификатор объекта, на котором произошло событие.
        var objectId = e.get('objectId');
        var object = objectManager.objects.getById(objectId);
        openBalloon(coords, object)
    }

    // Подписываемся на событие клика по объекту.
    objectManager.objects.events.add(['click'], onObjectClick);

    // Открывает всплывающее меню (balloon)
    function openBalloon(coords, object) {
        var isoCode = object.properties.iso3166

        map.balloon.open(coords, {
            contentHeader: isoCode,
            contentBody: `
            <div class="-btn-wrapper">
                <a href="/countries/add_to_visited/${isoCode}">
                    <button class="-btn">
                        Посещена
                    </button>
                </a>
            </div>
            <div class="-btn-wrapper">
                <a href="/countries/add_to_wish_list/${isoCode}">
                    <button class="-btn">
                        Хочу посетить
                    </button>
                </a>
            </div>
            <div class="-btn-wrapper">
            <a href="/countries/remove_cntry_status/${isoCode}">
                <button class="-btn">
                    Удалить статус
                </button>
            </a>
            </div>
            `,
        });
    }

    // Чтобы балун закрывался при клике на карту
    map.events.add('click', function(e) {
        if (!map.balloon.isOpen()) {
            var coords = e.get('coords');
            addBalloon(coords)

        } else {
            map.balloon.close();
        }
    });
}