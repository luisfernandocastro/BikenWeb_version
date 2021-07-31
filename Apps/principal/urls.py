from rest_framework import routers, urlpatterns
from Apps.principal import viewset

router = routers.DefaultRouter()

router.register('bicicletas',viewset.BicicletaViewset)
router.register('usuarios',viewset.UsersViewset,basename='User')
router.register('perfiles',viewset.ProfileViewset)
router.register('contratos',viewset.ContratoViewset)
router.register('categoriabike',viewset.CategoriaBikeViewset)
router.register('materialbike',viewset.MaterialBikeViewset)
router.register('registro',viewset.RegisterViewset)

router.register('catalogo',viewset.CatalogoViewset)


urlpatterns= router.urls