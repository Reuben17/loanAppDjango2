from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LoanDetail
from .serializers import LoanDetailSerializer
import pandas
import pickle

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    apiUrls={
    'List of Loans':'/list',
    'Individual Loan':'/individual/<str:pk>',
    'Update Loan':'/update/<str:pk>'
    }
    return Response(apiUrls)

#class LoanDetailApi(viewsets.ModelViewSet):
 #   queryset = LoanDetail.objects.all()
  #  serializer_class = LoanDetailSerializer

#class UserDetailApi(viewsets.ModelViewSet):
 #   queryset = NewUser.objects.all()
  #  serializer_class = UserLoanSerializer

# Displays all Loans
@api_view(['GET'])
def loanList(request):
    clients = LoanDetail.objects.all()
    serializer = LoanDetailSerializer(clients, many =True)
    return Response(serializer.data)

# Creates Loans
@api_view(['POST'])
def loanCreate(request):
    serializer = LoanDetailSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True): 
       clientAccountNo=serializer.validated_data.get('clientAccountNo')
       newCreditCustomer=serializer.validated_data.get('newCreditCustomer')
       age=serializer.validated_data.get('age')
       gender=serializer.validated_data.get('gender')
       amount=serializer.validated_data.get('amount')
       interest=serializer.validated_data.get('interest')
       loanDuration=serializer.validated_data.get('loanDuration')
       monthlyPayment=serializer.validated_data.get('monthlyPayment')
       education=serializer.validated_data.get('education')
       maritalStatus=serializer.validated_data.get('maritalStatus')
       employmentStatus=serializer.validated_data.get('employmentStatus')
       employmentDurationCurrentEmployer=serializer.validated_data.get('employmentDurationCurrentEmployer')
       incomeTotal=serializer.validated_data.get('incomeTotal')
       debtToIncomeRatio=serializer.validated_data.get('debtToIncomeRatio')
       lossGivenDefault=serializer.validated_data.get('lossGivenDefault')
       creditScore=serializer.validated_data.get('creditScore')
       noOfPreviousLoansBeforeLoan=serializer.validated_data.get('noOfPreviousLoansBeforeLoan')
       amountOfPreviousLoansBeforeLoan=serializer.validated_data.get('amountOfPreviousLoansBeforeLoan')
       noOfPreviousEarlyRepaymentsBeforeLoan=serializer.validated_data.get('noOfPreviousEarlyRepaymentsBeforeLoan')

       data = {
        "newCreditCustomer":[newCreditCustomer],
        "age":[age],
        "gender":[gender],
        "amount": [amount],
        "interest": [interest],
        "loanDuration":[loanDuration],
        "monthlyPayment":[monthlyPayment],
        "education":[education],
        "maritalStatus":[maritalStatus],
        "employmentStatus":[employmentStatus],
        "employmentDurationCurrentEmployer":[employmentDurationCurrentEmployer],
        "incomeTotal":[incomeTotal],
        "debtToIncomeRatio":[debtToIncomeRatio],
        "lossGivenDefault":[lossGivenDefault],
        "creditScore":[creditScore],
        "noOfPreviousLoansBeforeLoan":[noOfPreviousLoansBeforeLoan],
        "amountOfPreviousLoansBeforeLoan":[amountOfPreviousLoansBeforeLoan],
        "noOfPreviousEarlyRepaymentsBeforeLoan":[noOfPreviousEarlyRepaymentsBeforeLoan],
        }

    df = pandas.DataFrame(data)
    def condition(x):
     if x ==0:
      return 'Male'
     elif x==1:
      return 'Female'
     else:
      return 'Undefined'
    df['genderNominal'] =df['gender'].apply(condition)
    df.drop('gender',inplace = True,axis=1)

    def condition(x):
     if x ==-1:
        return 'Married'
     elif x==1:
        return 'Married'
     elif x==2:
        return "Cohabitant"
     elif x==3:
        return 'Single'
     elif x==4:
        return 'Divorced'
     else:
        return 'Widow'
    df['maritalStatusNominal'] =df['maritalStatus'].apply(condition)
    df.drop('maritalStatus',inplace = True,axis=1)

    def condition(x):
     if x =='TrialPeriod' or x=='Other':
       return 1
     elif x=='UpTo1Year':
        return 2
     elif x=='UpTo2Years':
        return 3
     elif x=='UpTo3Years':
        return 4
     elif x=='UpTo4Years':
        return 5
     elif x=='UpTo5Years':
        return 6
     else:
        return 7
    df['employmentDurationCurrentEmployerOrdinal'] =df['employmentDurationCurrentEmployer'].apply(condition)
    df.drop('employmentDurationCurrentEmployer',inplace = True,axis=1)

    categoricalNominal_features =[]
    categoricalNominal_features_list =['newCreditCustomer','genderNominal','maritalStatusNominal']
    categoricalNominal_features.extend(categoricalNominal_features_list)

    categoricalOrdinal_features =[]
    categoricalOrdinal_features_list =['education','employmentStatus','employmentDurationCurrentEmployerOrdinal']
    categoricalOrdinal_features.extend(categoricalOrdinal_features_list)
 
    numerical_features =[]
    numerical_features_list =['age','amount','interest','loanDuration','monthlyPayment','incomeTotal','debtToIncomeRatio','lossGivenDefault','creditScore','noOfPreviousLoansBeforeLoan','amountOfPreviousLoansBeforeLoan','noOfPreviousEarlyRepaymentsBeforeLoan']
    numerical_features.extend(numerical_features_list)

    df['newCreditCustomer'] = df['newCreditCustomer'].astype(object) 
    list1 = ['True','False']
    list2=['Female','Male','Undefined']
    list3 =['Cohabitant','Divorced','Married','Single','Widow']
    df_nominal_credit=pandas.get_dummies(df[['newCreditCustomer']].astype(pandas.CategoricalDtype(categories=list1)))
    df_nominal_gender=pandas.get_dummies(df[['genderNominal']].astype(pandas.CategoricalDtype(categories=list2)))
    df_nominal_marriage=pandas.get_dummies(df[['maritalStatusNominal']].astype(pandas.CategoricalDtype(categories=list3)))
    #+['newCreditCustomer_False', 'newCreditCustomer_True','genderNominal_Female','genderNominal_Male','genderNominal_Undefined','maritalStatusNominal_Cohabitant]','maritalStatusNominal_Divorced','maritalStatusNominal_Married','maritalStatusNominal_Single','maritalStatusNominal_Widow'])
    df_nominal = pandas.concat([df_nominal_credit,df_nominal_gender,df_nominal_marriage],axis=1)
   

    for feature in categoricalOrdinal_features:
        df[feature]=df[feature].astype('category').cat.codes

    df_ordinal=df[categoricalOrdinal_features]

    new_dataset=pandas.concat([df_nominal,df_ordinal,df[numerical_features]],axis=1)
   
    with open('C:\\Users\\reubenmbalanya\Desktop\loanAppDjango2\\backend\scale_fit','rb') as f:
     scale_fit = pickle.load(f)

    X=new_dataset.to_numpy()
    scaled_data= scale_fit.transform(X)
   
    with open('C:\\Users\\reubenmbalanya\Desktop\loanAppDjango2\\backend\logisticRegressionLoanModel','rb') as f:
     model = pickle.load(f)

    prediction = model.predict(scaled_data)
    print("Prediction:",prediction[0])

    if prediction[0]==1:
     verdict= "Ineligible"
    else:
     verdict ="Eligible"

    

    serializer.save(clientAccountNo=clientAccountNo,newCreditCustomer=newCreditCustomer,age=age,gender=gender,
    amount=amount,interest=interest,loanDuration=loanDuration,monthlyPayment=monthlyPayment,education=education,
    maritalStatus=maritalStatus,employmentStatus=employmentStatus,employmentDurationCurrentEmployer=employmentDurationCurrentEmployer,
    incomeTotal=incomeTotal,debtToIncomeRatio=debtToIncomeRatio,lossGivenDefault=lossGivenDefault,
    creditScore=creditScore,noOfPreviousLoansBeforeLoan=noOfPreviousLoansBeforeLoan,
    amountOfPreviousLoansBeforeLoan=amountOfPreviousLoansBeforeLoan,
    noOfPreviousEarlyRepaymentsBeforeLoan=noOfPreviousEarlyRepaymentsBeforeLoan	,
    verdict=verdict)
    
    print('Loan Inserted')

    return Response(serializer.data)
