from accounts.models import LECUser

def account_types(request):
    return {'AccountTypes': LECUser.AccountTypes}
