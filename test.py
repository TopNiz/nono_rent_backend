from nono_rent_backend.models.tenant import Tenant

try:
    t = Tenant.model_validate(
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "notanemail",
            "phone": "0123456789",
            "address": "123 Rue de la Paix, Paris",
        }
    )
    print("Created successfully", t)
except Exception as e:
    print("Exception", type(e), e)
