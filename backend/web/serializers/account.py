from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Validate the transport shape of a login request."""

    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        write_only=True,
        allow_blank=False,
        trim_whitespace=False,
        max_length=128,
    )


class RegisterSerializer(LoginSerializer):
    """Registration can enforce a stronger minimum than login transport validation."""

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
