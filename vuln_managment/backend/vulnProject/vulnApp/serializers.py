from rest_framework import serializers
from .models import asset, playbook, policy, ticket, User, vulnerability
from django.contrib.auth import authenticate

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = asset
        fields = ('assetid', 'cpe', 'risk', 'baseSLA', 'policyid', 'category', 'hostname', 'tags')
class VulnerabilitySerializer(serializers.ModelSerializer):
    assetid = AssetSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = vulnerability
        fields = ('vulnid', 'assetid', 'threat', 'cve', 'cpe', 'risk', 'baseSLA', 'cwe', 'mav', 'mac', 'mpr', 'mui', 'ms', 'mc', 'mi', 'ma', 'rc', 'rl', 'ecm', 'description', 'dayZero')
        extra_kwargs = {
            'cve': {'validators': []},
        }
class PlaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = playbook
        fields = ('playbookid', 'category','patchacquirement', 'patchvalidation', 'verification', 'rollout', 'notes')
class TicketSerializer(serializers.ModelSerializer):
    vulnid = VulnerabilitySerializer(required=False, read_only=True)
    playbookid = PlaybookSerializer(required=False, read_only=True)
    assets = AssetSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = ticket
        fields = ('ticketNumber', 'summary','validatedsummary', 'verifiedsummary','rolledsummary','progress', 'assignedTo', 'group', 'timeStarted', 'timeClosed', 'cve', 'vulnid', 'cvss', 'qa', 'sla', 'exposure', 'threat', 'assets', 'outcome', 'playbookid', 'acquired', 'validated', 'verified', 'rolledout', 'enscore', 'iscbase', 'temporal', 'exploitScore', 'iscmodified','impactModScore', 'impactScore', 'environmentalScore')
class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = policy
        fields = ('policyid', 'cpe', 'confidentialityreq', 'integrityreq', 'availabilityreq', 'category')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'is_staff': user.is_superuser
        }
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'is_staff')
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance