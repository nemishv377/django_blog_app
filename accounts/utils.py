def get_user_permissions(user):
  permissions = user.get_all_permissions()
  user_has_perm = {}
  for perm in permissions:
    app_label, permission_codename = perm.split('.')
    user_has_perm['user_can_'+permission_codename] = True
  
  return user_has_perm
