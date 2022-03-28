from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _

from waffle.models import AbstractUserFlag, CACHE_EMPTY
from waffle.utils import get_setting, keyfmt, get_cache

cache = get_cache()


class Company(models.Model):
    name = models.CharField(
        max_length=100,
    )


class CompanyUser(AbstractBaseUser):
    company = models.ForeignKey(
        Company,
        on_delete=CASCADE
    )

    username = models.CharField(
        max_length=100,
    )


class CompanyAwareFlag(AbstractUserFlag):
    FLAG_COMPANIES_CACHE_KEY = 'FLAG_COMPANIES_CACHE_KEY'
    FLAG_COMPANIES_CACHE_KEY_DEFAULT = 'flag:%s:companies'

    companies = models.ManyToManyField(
        Company,
        blank=True,
        help_text=_('Activate this flag for these companies.'),
    )

    def get_flush_keys(self, flush_keys=None):
        flush_keys = super(CompanyAwareFlag, self).get_flush_keys(flush_keys)
        companies_cache_key = get_setting(CompanyAwareFlag.FLAG_COMPANIES_CACHE_KEY,
                                          CompanyAwareFlag.FLAG_COMPANIES_CACHE_KEY_DEFAULT)
        flush_keys.append(keyfmt(companies_cache_key, self.name))
        return flush_keys

    def is_active_for_user(self, user):
        is_active = super(CompanyAwareFlag, self).is_active_for_user(user)
        if is_active:
            return is_active

        if getattr(user, 'company_id', None):
            company_ids = self._get_company_ids()
            if user.company_id in company_ids:
                return True

    def _get_company_ids(self):
        cache_key = keyfmt(
            get_setting(CompanyAwareFlag.FLAG_COMPANIES_CACHE_KEY, CompanyAwareFlag.FLAG_COMPANIES_CACHE_KEY_DEFAULT),
            self.name
        )
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return set()
        if cached:
            return cached

        company_ids = set(self.companies.all().values_list('pk', flat=True))
        if not company_ids:
            cache.add(cache_key, CACHE_EMPTY)
            return set()

        cache.add(cache_key, company_ids)
        return company_ids
