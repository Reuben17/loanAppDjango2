from django.db import models
# Create your models here.

class LoanDetail(models.Model):
    clientAccountNo=models.IntegerField()
    newCreditCustomer=models.CharField(max_length=100)
    age=models.IntegerField()
    gender = models.IntegerField()
    amount=models.FloatField(blank=True)
    interest = models.FloatField(blank =True)
    loanDuration=models.IntegerField(blank=True)
    monthlyPayment=models.FloatField(blank=True)
    education=models.IntegerField()
    maritalStatus=models.IntegerField()
    employmentStatus=models.IntegerField()
    employmentDurationCurrentEmployer = models.CharField(max_length=100)
    incomeTotal=models.IntegerField()
    debtToIncomeRatio =models.FloatField()
    lossGivenDefault=models.FloatField(blank =True)
    creditScore = models.FloatField()
    noOfPreviousLoansBeforeLoan = models.IntegerField()
    amountOfPreviousLoansBeforeLoan = models.IntegerField()
    noOfPreviousEarlyRepaymentsBeforeLoan = models.IntegerField()
    verdict=models.CharField(max_length =100,blank =True)

    


   