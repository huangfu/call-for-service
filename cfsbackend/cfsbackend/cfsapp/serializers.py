from django.contrib.auth.models import User, Group
from .models import Incident, Call, City, CallSource, CallUnit
from rest_framework import serializers

from collections import OrderedDict
from rest_framework.fields import SkipField

class NonNullSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is not None:
                represenation = field.to_representation(attribute)
                if represenation is None:
                    # Do not seralize empty objects
                    continue
                if isinstance(represenation, list) and not represenation:
                   # Do not serialize empty lists
                   continue
                ret[field.field_name] = represenation

        return ret


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('city_id', 'descr')

class CallSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CallSource
        fields = ('call_source_id', 'descr')

class CallUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CallUnit
        fields = ('call_unit_id', 'descr')

class IncidentSerializer(serializers.HyperlinkedModelSerializer):
    
    city = CitySerializer()
    
    class Meta:
        model = Incident
        read_only_fields = ('incident_id', 'case_id', 'time_filed', 'month_filed', 'week_filed', 'dow_filed', 'street_num', 'street_name', 'zip', 'city',
        	'geox', 'geoy', 'beat', 'district', 'sector', 'domestic', 'juvenile', 'gang_related', 'num_officers', 'ucr_code', 'committed')

class CallSerializer(NonNullSerializer):

    city = CitySerializer(read_only=True)
    call_source  = CallSourceSerializer(read_only=True)
    primary_unit = CallUnitSerializer(read_only=True,allow_null=False)
    first_dispatched = CallUnitSerializer(read_only=True)
    reporting_unit   = CallUnitSerializer(read_only=True,allow_null=True)

    class Meta:
        model = Call
        read_only_fields = ('call_id', 'city', 'call_source', 'primary_unit', 'first_dispatched', 'reporting_unit', 'month_received', 'week_received', 'dow_received', 'hour_received', 'case_id', 'street_num', 'street_name', 'zip', 'crossroad1', 'crossroad2', 'geox', 'geoy', 'beat', 'district', 'sector', 'business', 'priority', 'report_only', 'cancelled', 'time_received', 'time_routed', 'time_finished', 'first_unit_dispatch', 'first_unit_enroute', 'first_unit_arrive', 'first_unit_transport', 'last_unit_clear', 'time_closed', 'close_comments')

# Testing reduced payload
class CallOverviewSerializer(serializers.HyperlinkedModelSerializer):
    m = serializers.IntegerField(source='month_received')
    w = serializers.IntegerField(source='week_received')
    d = serializers.IntegerField(source='dow_received')
    h = serializers.IntegerField(source='hour_received')
    n = serializers.IntegerField(source='call_id__count')

    class Meta:
        model = Call
        read_only_fields = ('m','w','d','h','n')