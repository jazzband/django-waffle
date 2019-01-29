from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from waffle import get_waffle_flag_model


@receiver(m2m_changed, sender=get_waffle_flag_model().users.through)
@receiver(m2m_changed, sender=get_waffle_flag_model().groups.through)
def flag_membership_changed(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_remove'):
        instance.flush()
