REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING':
    False,
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework_simplejwt.authentication.JWTAuthentication', ),
    'DEFAULT_SCHEMA_CLASS':
    'drf_spectacular.openapi.AutoSchema',

    # For global pagination
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 2
}
