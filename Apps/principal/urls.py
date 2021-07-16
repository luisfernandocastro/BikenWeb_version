from rest_framework import routers, urlpatterns
from Apps.principal import viewset

router = routers.SimpleRouter()

router.register('api/bicicletas',viewset.BicicletaViewset)
router.register('api/usuarios',viewset.UsersViewset,basename='User')
router.register('api/perfiles',viewset.ProfileViewset)
router.register('api/contratos',viewset.ContratoViewset)
router.register('api/categoriabike',viewset.CategoriaBikeViewset)
router.register('api/materialbike',viewset.MaterialBikeViewset)
router.register('api/registro',viewset.RegisterViewset)


urlpatterns= router.urls