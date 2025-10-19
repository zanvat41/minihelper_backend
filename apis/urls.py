from django.urls import path

from .views import weather, menu, image, service, test

urlpatterns=[
    path('weather', weather.WeatherView.as_view()),
    path('menu', menu.get_menu),
    path('image', image.ImageView.as_view()),
    path('image/list', image.ImageListView.as_view()),
    path('stock', service.stock),
    path('constellation', service.constellation),
    path('jokes', service.jokes),
    path('test', test.test)
]
