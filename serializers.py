from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer')
        read_only_fields = ['customer']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    # data_sheet = serializers.PrimaryKeyRelatedField(read_only=True)
    # data_sheet = serializers.SerializerMethodField()
    data_sheet = DataSheetSerializer(read_only=True)
    professions = ProfessionSerializer(many=True)
    document_set = DocumentSerializer(many=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'professions', 'data_sheet',
                  'active', 'status_sentence', 'num_professions', 'document_set')

    def create(self, validated_data):
        import pdb; pdb.set_trace()
        professions = validated_data['professions']
        del validated_data['professions']

        document_set = validated_data['document_set']
        del validated_data['document_set']

        customer = Customer.objects.create(**validated_data)

        for doc in document_set:
            Document.objects.create(
                dtype=doc['dtype'],
                doc_number=doc['doc_number'],
                customer_id=customer.id
            )

        for profession in professions:
            prof = Profession.objects.create(**profession)
            customer.professions.add(prof)

        customer.save()

        return customer

    def get_num_professions(self, obj):
        return obj.num_professions()
