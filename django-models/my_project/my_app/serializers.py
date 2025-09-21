from rest_framework import serializers
from .models import Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__' #includes model fields
        extra_fields = ['days_since_created']

    def get_days_since_created(self, obj):
        if Book.created_at:
            delta = date.today() - obj.created_at.date()
            return delta.days
        return None







