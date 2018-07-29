# Django core
from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.users.models import User
from apps.social.models import VKAuth

from . import vkapi

class DialogManager():
    def create_dialog(self, user_vk_id):
        # Найти пользователя , собрать дефолтные задачи, выставить стэйт
        try:
            vk_auth = VKAuth.objects.get(uid=user_vk_id)
            user = vk_auth.user
            dialog = self.create(user=user, state='NEED_NEXT_BOT_STATE')
            return dialog
        except VKAuth.DoesNotExist:
            # TODO сделать нормально
            new_user = User.objects.create_user(email='test@email.ru')

            # TODO получить данные пользователя от  vk по  vk_id

            vk_auth = VKAuth.objects.create(
                uid=user_vk_id,
                user=new_user
            )
            vk_auth.save()
            dialog = self.create(user=new_user, state='NEED_NEXT_BOT_STATE')
            return dialog

        except Exception:
            # TODO посмотреть исключения
            raise ValueError('User with id {} not found'.format(user_vk_id))


class Dialog(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    objects = DialogManager()

    STATES = (
        ('DEFAULT_BOT_STATE', 'Wait for any command'),
        ('NEED_NEXT_BOT_STATE', 'Wait for answer the question "Need the next block?"'),
        ('WAIT_ANSWER_BOT_STATE', 'Wait for current block answer'),
    )

    state = models.CharField(choices=STATES, max_length=128)

    blocks_ids = ArrayField(
        models.IntegerField(),
        verbose_name='Массив из id блоков',
        blank=True,
        default=[]
    )

    current_block_pointer = models.IntegerField('block pointer', default=0)

    @property
    def current_block_id(self):
        return self.current_block_pointer

    def update_pointer(self):
        """Перемещает указатель на следующую задачу в списке"""
        if self.current_block_pointer < self.blocks_ids.count() - 1:
            self.current_block_pointer += 1