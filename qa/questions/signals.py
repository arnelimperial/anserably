# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils.text import slugify
# from qa.questions.models import Answer
# # from qa.core.utils import generate_random_string


# @receiver(pre_save, sender=Answer)
# def add_slug_to_answer(sender, instance, *args, **kwargs):
#     if instance and not instance.slug:
#         slug = slugify(instance.body)
#         random_string = generate_random_string()
#         instance.slug = slug + "-" + random_string



