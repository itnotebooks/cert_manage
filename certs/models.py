import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User


# Create your models here.
class Certs(models.Model):
    '''
    证书
    '''
    CERT_METHOD_CHOICES = (
        (0, _('域名')),
        (1, _('证书')),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=45, verbose_name=_("名称"), null=False)

    # 通用名称
    domain = models.CharField(max_length=128, verbose_name=_("通用名称"), null=True)
    # 备用名称
    orther_domain = models.TextField(max_length=4096, null=True, blank=True, verbose_name=_("备用名称"))
    organization_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Organization Name"))

    serial_number = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Serial number"))
    issued_by = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Issued By'))

    # 证书类型
    cert_type = models.CharField(max_length=4, null=True, blank=True, verbose_name=_("证书类型"))

    # 在线解析，还是离线解析
    method = models.BooleanField(default=0, choices=CERT_METHOD_CHOICES, verbose_name=_("Cert Detection Approach"))

    # 通过域名，在线解析
    domain_url = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("域名"))

    # 通过证书文件离线解析
    crt_file = models.TextField(null=True, blank=True, verbose_name=_("Crt File"))
    key_file = models.TextField(null=True, blank=True, verbose_name=_("Key File"))

    # 起至日期
    notbefore = models.CharField(max_length=24, null=True, blank=True, verbose_name=_('Not Before'))
    notafter = models.CharField(max_length=24, null=True, blank=True, verbose_name=_('Not After'))

    # 剩余天数
    remain_days = models.IntegerField(null=True, blank=True, verbose_name=_('Remaining Days'))

    users = models.ManyToManyField(User, verbose_name=_("Contact"))
    # 创建时间
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
    # 描述
    comment = models.TextField(max_length=128, null=True, blank=True, verbose_name=_('Comment'))

    def __str__(self):
        return self.name

    @property
    def get_method(self):
        return self.get_method_display

    @property
    def get_contact(self):
        contact_lisst = [user.name for user in self.users.all()]
        return ','.join(contact_lisst)

    @property
    def get_user_info(self):
        user_info = []
        for u in self.users.all():
            info = {'name': u.name,
                    'phone': u.phone,
                    'email': u.email
                    }
            user_info.append(info)
        return user_info

    class Meta:
        db_table = "certs"
