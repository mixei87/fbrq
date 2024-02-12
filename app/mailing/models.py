from django.db.models import Model, DateTimeField, TextField, ManyToManyField, PositiveSmallIntegerField, ForeignKey, \
    CASCADE, CharField, SlugField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from pytz import all_timezones


class PhoneCode(Model):
    phone_code = PositiveSmallIntegerField(primary_key=True,
                                           validators=[MinValueValidator(900), MaxValueValidator(999)],
                                           verbose_name="Код телефона")

    def __str__(self):
        return str(self.phone_code)

    class Meta:
        verbose_name = "Код телефона"
        verbose_name_plural = "Коды телефонов"


class Tag(Model):
    tag = SlugField(primary_key=True, verbose_name="Тэг клиента")

    def __str__(self):
        return str(self.tag)

    class Meta:
        verbose_name = "Тэг клиента"
        verbose_name_plural = "Тэги клиентов"


class Mailing(Model):
    start_time = DateTimeField(verbose_name="Дата и время запуска рассылки")
    finish_time = DateTimeField(verbose_name="Дата и время окончания рассылки")
    text_msg = TextField(verbose_name="Текст сообщения для доставки клиенту")
    filter_phone_code = ManyToManyField(PhoneCode, verbose_name="Фильтр клиентов по коду мобильного оператора",
                                        blank=True)
    filter_tag = ManyToManyField(Tag, verbose_name="Фильтр клиентов по тегу", blank=True)

    def __str__(self):
        return f'Рассылка {self.pk}: "{self.text_msg[:50]}"'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        unique_together = ('start_time', 'finish_time', 'text_msg')


class Client(Model):
    TIMEZONES = tuple(zip(all_timezones, all_timezones))

    phone = CharField(primary_key=True, max_length=11,
                      validators=[RegexValidator(
                          regex=r'^79\d{9}$', message="Номер телефона клиента в формате 79XXXXXXXXX"
                                                      "(X - цифра от 0 до 9)")], verbose_name="Номер телефона")
    phone_code = ForeignKey(PhoneCode, on_delete=CASCADE, verbose_name="Код телефона")
    tag = ForeignKey(Tag, on_delete=CASCADE, blank=True, null=True, verbose_name="Тэг клиента")
    timezone = CharField(max_length=32, choices=TIMEZONES, default='UTC', verbose_name="Часовой пояс")

    def save(self, *args, **kwargs):
        phone_code = int(self.phone[1:4])
        self.phone_code, _ = PhoneCode.objects.get_or_create(phone_code=phone_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(Model):
    STATUSES = ['SUCCESS', 'IN_PROGRESS', 'FAIL']
    STATUSES = tuple(zip(STATUSES, STATUSES))

    datetime_sent = DateTimeField(auto_now_add=True, verbose_name="Дата и время отправки")
    status = CharField(max_length=11, choices=STATUSES, default='IN_PROGRESS', verbose_name="Статус сообщения")
    mailing = ForeignKey(Mailing, on_delete=CASCADE, verbose_name="Рассылка")
    client = ForeignKey(Client, on_delete=CASCADE, verbose_name="Клиент")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
