from rest_framework import serializers
from .models import LoanDetail
from userAccounts.models import NewUser

class UserLoanSerializer(serializers.ModelSerializer):
 class Meta:
        model= NewUser
        fields = '__all__'

class LoanDetailSerializer(serializers.ModelSerializer):
 class Meta:
        model= LoanDetail
        fields = ('__all__' )
       # depth=1
       
