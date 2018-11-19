from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework_bulk import BulkSerializerMixin

from .models import (
    DocumentationLink, Infraction,
    Member, OffTopicChannelName,
    Role, SnakeFact,
    SnakeIdiom, SnakeName,
    SpecialSnake, Tag
)


class DocumentationLinkSerializer(ModelSerializer):
    class Meta:
        model = DocumentationLink
        fields = (
            'id', 'inserted_at', 'expires_at', 'active', 'user', 'actor', 'type', 'reason', 'hidden'
        )


class InfractionSerializer(ModelSerializer):
    class Meta:
        model = Infraction
        fields = ('package', 'base_url', 'inventory_url')


class OffTopicChannelNameSerializer(ModelSerializer):
    class Meta:
        model = OffTopicChannelName
        fields = ('name',)

    def to_representation(self, obj):
        return obj.name


class SnakeFactSerializer(ModelSerializer):
    class Meta:
        model = SnakeFact
        fields = ('fact',)


class SnakeIdiomSerializer(ModelSerializer):
    class Meta:
        model = SnakeIdiom
        fields = ('idiom',)


class SnakeNameSerializer(ModelSerializer):
    class Meta:
        model = SnakeName
        fields = ('name', 'scientific')


class SpecialSnakeSerializer(ModelSerializer):
    class Meta:
        model = SpecialSnake
        fields = ('name', 'images', 'info')


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'colour', 'permissions')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'embed')


class MemberSerializer(BulkSerializerMixin, ModelSerializer):
    roles = PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())

    class Meta:
        model = Member
        fields = ('id', 'avatar_hash', 'name', 'discriminator', 'roles')
        depth = 1
