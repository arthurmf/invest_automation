from __future__ import unicode_literals

from django.db import models

class ReportTypes(models.Model):
    nome_report = models.CharField(max_length=250)

class ExecutionDashboard(models.Model):
    nome_rotina = models.CharField(max_length=250)
    report_type = models.ForeignKey(ReportTypes, on_delete=models.PROTECT)
    descricao_rotina = models.CharField(max_length=1000)
    nome_execucao_rotina = models.CharField(max_length=250)
    passo_a_passo_execucao = models.CharField(max_length=1000)

class ExecutionLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    execution = models.ForeignKey(ExecutionDashboard, on_delete=models.PROTECT)

class Global_Variables(models.Model):
    variable_name = models.CharField(max_length=90)
    variable_value = models.CharField(max_length=90)


