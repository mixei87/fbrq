from django.db.models import Model, DateTimeField, TextField, ManyToManyField, PositiveSmallIntegerField, ForeignKey, \
    CASCADE, UniqueConstraint, CharField, PositiveBigIntegerField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from pytz import all_timezones


class PhoneCode(Model):
    code = PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(900), MaxValueValidator(999)])


class Tag(Model):
    tag = CharField(max_length=50)


class Mailing(Model):
    start_time = DateTimeField("Дата и время запуска рассылки")
    text_msg = TextField("Текст сообщения для доставки клиенту")
    filter_phone_code = ManyToManyField(PhoneCode, through='PhoneCodeMailing', through_fields=('mailing', 'phone_code'),
                                        verbose_name="Фильтр клиентов по коду мобильного оператора")
    filter_tag = ManyToManyField(Tag, through='TagMailing', through_fields=('mailing', 'tag'),
                                 verbose_name="Фильтр клиентов по тегу")
    finish_time = DateTimeField("Дата и время окончания рассылки")


class PhoneCodeMailing(Model):
    mailing = ForeignKey(Mailing, on_delete=CASCADE)
    phone_code = ForeignKey(PhoneCode, on_delete=CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=['phone_code', 'mailing'], name='unique_phone_code_mailing')]


class TagMailing(Model):
    mailing = ForeignKey(Mailing, on_delete=CASCADE)
    tag = ForeignKey(Tag, on_delete=CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=['tag', 'mailing'], name='unique_tag_mailing')]


class Client(Model):
    TIMEZONES = tuple(zip(all_timezones, all_timezones))

    phone = PositiveBigIntegerField(validators=[RegexValidator(regex=r'^79\d{9}$',
                                                               message="Номер телефона клиента в формате 79XXXXXXXXX"
                                                                       "(X - цифра от 0 до 9)")])
    phone_code = ForeignKey(PhoneCode, on_delete=CASCADE)
    tag = ForeignKey(Tag, on_delete=CASCADE)
    timezone = CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Message(Model):
    STATUSES = ['SUCCESS', 'IN_PROGRESS', 'FAIL']
    STATUSES = tuple(zip(STATUSES, STATUSES))

    datetime_sent = DateTimeField(auto_now_add=True)
    status = CharField(max_length=11, choices=STATUSES, default='IN_PROGRESS')
    mailing = ForeignKey(Mailing, on_delete=CASCADE)
    client = ForeignKey(Client, on_delete=CASCADE)
