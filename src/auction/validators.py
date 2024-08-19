from django.core.exceptions import ValidationError


def validate_file_size(file):
    MAX_SIZE_KB = 1300

    if file.size > MAX_SIZE_KB * 1024:
        raise ValidationError(f'File can not be larger than {MAX_SIZE_KB}KB.')
