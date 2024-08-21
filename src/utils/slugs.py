from django.utils import timezone
from django.utils.text import slugify


def generate_unique_slug(instance, text=''):
    model = instance.__class__
    slugify_text = slugify(text)

    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    new_slug = f'{slugify_text}-{current_datetime}'

    # Ensure the generated slug is unique
    while model.objects.filter(slug=new_slug).exclude(pk=instance.pk).exists():
        current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
        new_slug = f'{slugify_text}-{current_datetime}'

    return new_slug
