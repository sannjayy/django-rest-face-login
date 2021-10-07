from django.core.exceptions import ValidationError

# File size validator
def file_size(value): 
    limit = 2 * 1024 * 1024 # 2MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')