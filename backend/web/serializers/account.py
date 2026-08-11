from rest_framework import serializers


class CredentialsSerializer(serializers.Serializer):
    """Shared username/password validation for login and registration.

    Keeping syntactic validation in a Serializer lets Views focus on business rules
    such as authentication and duplicate-user checks.
    """

    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        write_only=True,
        allow_blank=False,
        trim_whitespace=False,
        min_length=6,
        max_length=128,
    )


def validation_response_data(serializer):
    """Keep the current beginner-facing `result` field while exposing field errors."""
    first_message = '请求参数不合法'
    for messages in serializer.errors.values():
        if messages:
            first_message = str(messages[0])
            break

    return {
        'result': first_message,
        'code': 'VALIDATION_ERROR',
        'errors': serializer.errors,
    }
