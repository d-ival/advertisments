from django.contrib.auth.models import User
from rest_framework import serializers, validators

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context['view'].action == 'create':
            status = data.get('status', 'DRAFT')
        else:
            status = data.get('status')

        open_status = (AdvertisementStatusChoices.OPEN, AdvertisementStatusChoices.DRAFT)
        if status not in open_status:
            # в результате выполнения запроса количество открытых объявлений не изменится
            return data

        user = self.context['request'].user
        active_items = user.advertisements.filter(status__in=open_status)

        if len(active_items) >= 10:
            error_msg = f"Для пользователя {user} достигнуто максимальное число открытых объявлений: 10. " \
                        f"Чтобы разблокировать возможность создания новых объявлений необходимо перевести минимум " \
                        f"одно объявление в статус {AdvertisementStatusChoices.CLOSED}"
            raise validators.ValidationError(error_msg)

        return data
