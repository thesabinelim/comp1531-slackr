#Given a User by their user ID, set their permissions to new permissions described by permission_id
from error import AccessError
u_id_list = [1234567,5242579,4201337,9876543]
permission_list = [1,2,3]
def admin_userpermission_change(token, u_id, permission_id):
    vaild_u_id = False
    if u_id in u_id_list:
        vaild_u_id = True
    
    if vaild_u_id == False:
        raise ValueError("Invaild u_id")
    
    vaild_permission_id = False
    
    if permission_id in permission_list:
        vaild_permission_id = True
    
    if vaild_permission_id == False:
        raise ValueError("Invaild permission_id")
    
    authorised_user_permission = token%10
    
    if authorised_user_permission == 3:
        raise AccessError
    else:
        token = token - authorised_user_permission + permission_id
        return token

