from django.db import models

class Account(models.Model):
    
    class Meta(object):
        
        #作成されるテーブル名を指定
        db_table = 'accounts'
        #管理画面でのモデルの名称
        verbose_name = 'アカウント'
    #項目作成
<<<<<<< HEAD
    #user_id = models.Field('googleユーザーID')
    id = models.AutoField(verbose_name='アカウントID',primary_key=True,editable=False,max_length=6,blank=False, null=False)
    last_name = models.CharField(verbose_name='姓',max_length=25,blank=False, null=False)
    first_name = models.CharField(verbose_name='名',max_length=25,blank=False, null=False)
    password = models.SlugField(verbose_name='パスワード',max_length=20,blank=False, null=False)	
    is_administrator = models.BooleanField(verbose_name='管理権限',default=False,blank=False, null=False)
    is_approval = models.BooleanField(verbose_name='承認',default=False,blank=False, null=False)
=======
    id = models.AutoField('アカウントID',primary_key=True,editable=False,max_length=6,blank=False, null=False)
    last_name = models.CharField('姓',max_length=25,blank=False, null=False)
    first_name = models.CharField('名',max_length=25,blank=False, null=False)
    password = models.CharField('パスワード',max_length=20,blank=False, null=False)	
    is_administrator = models.BooleanField('管理権限',default=False,blank=False, null=False)
    is_approval = models.BooleanField('承認',default=False,blank=False, null=False)
>>>>>>> cdfc4468242ea5dc51967c87ebcf517cf12c4631
    create_at = models.DateTimeField(verbose_name="作成日時",auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時",auto_now=True)
    def __str__(self):
        
        return str(self.id)